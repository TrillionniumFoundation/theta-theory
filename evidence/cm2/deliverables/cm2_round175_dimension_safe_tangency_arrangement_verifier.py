#!/usr/bin/env python3
"""Independent verifier for the Round175 tangency arrangement.

The Round175 producer is byte-pinned but never imported or executed.  This
verifier reconstructs all 22 Round172 parents from their dyadic atlas paths,
replays the 192-bit root and outgoing-seam geometry, rebuilds the complete
expected certificate, and rejects re-signed semantic mutations.
"""

from __future__ import annotations

import argparse
import copy
from dataclasses import dataclass
from fractions import Fraction as Q
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import tempfile
from typing import Any, Callable

import flint
from flint import arb

import cm2_gate3_candidate_first_hit_cert as base
import cm2_gate3_eight_cell_symmetry_atlas_cert as atlas


HERE = Path(__file__).resolve().parent
PRODUCER = HERE / "cm2_round175_dimension_safe_tangency_arrangement.py"
CERTIFICATE = (
    HERE / "cm2_round175_dimension_safe_tangency_arrangement_certificate.json"
)
OUTPUT = (
    HERE / "cm2_round175_dimension_safe_tangency_arrangement_verification.json"
)
CERTIFICATE_SCHEMA = "cm2.round175.dimension-safe-tangency-arrangement.v1"
VERIFICATION_SCHEMA = (
    "cm2.round175.dimension-safe-tangency-arrangement.verification.v1"
)
MAX_INPUT_BYTES = 16 * 1024 * 1024
FROZEN_OWNER = "W[1,0]"
FROZEN_OUTGOING = "W"
CHARTS = ("W:E", "W:N", "W:S")
MAX_EXCEPTION_BASE_DEPTH = 8
BRACKET_STEPS = 24

ATLAS_SOURCE = "cm2_gate3_eight_cell_symmetry_atlas_cert.py"
BASE_SOURCE = "cm2_gate3_candidate_first_hit_cert.py"
GE_SOURCE = "cm2_gate3_ge_interval_atlas_cert.py"
OWNERSHIP = "cm2-gate3-chart-seam-quotient-manifest-2026-07-15.json"
R172_PRODUCER = (
    "cm2_round172_dimension_safe_tangency_parent_"
    "frozen_owner_absence_pruning.py"
)
R172_CERT = (
    "cm2_round172_dimension_safe_tangency_parent_"
    "frozen_owner_absence_pruning_certificate.json"
)
R172_VERIFIER = (
    "cm2_round172_dimension_safe_tangency_parent_"
    "frozen_owner_absence_pruning_verifier.py"
)
R172_VER = (
    "cm2_round172_dimension_safe_tangency_parent_"
    "frozen_owner_absence_pruning_verification.json"
)

PINS: dict[str, str] = {
    ATLAS_SOURCE:
        "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    BASE_SOURCE:
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    GE_SOURCE:
        "ab120f85a263f3cb0697d8a40bc9ed2bf12b361aa7c54940c214b6fd85b17e2b",
    OWNERSHIP:
        "1fb40060336f04f28a7cac19a70abdd3692ced272825b2f1f6b6ae005f00518b",
    R172_PRODUCER:
        "81f147cf6106d7436df282de106fc47e793e8f97a43282b35719e28182e07980",
    R172_CERT:
        "3185188c476a64d3e732674fa724ce9a49afe84c61abab448f746a5a3555b66c",
    R172_VERIFIER:
        "066f84d1517338774a8fc8132bd61006cabedbe7674129a433016fc16ddcad99",
    R172_VER:
        "d095ecdd1b59a6577f96f0317f8a30122e8cd3f6baf73ed550c5d227ed1811c3",
}

EXPECTED_PRODUCER_SHA256 = (
    "16122dcc7c39b140d45139a01bac6d6f41d7cbb60da2499ecc50fbeac2766355"
)
EXPECTED_CERTIFICATE_SHA256 = (
    "a2a69b3d4559fadb647d8f9ea6a06ef4c1625647965423cdb25f53fa08d2deee"
)
EXPECTED_CERTIFICATE_RESULT_SHA256 = (
    "827d6f674dd4a5291bf08f5ffd65b31187faa1c9fe977e1b7e7da10cd1166d72"
)
R172_RESULT = "a436b4a82b1e8d5c617fe576e0e4e76b6f6f38ad8ac3eda4ddde544c2769a776"
R172_VER_RESULT = "aa0fb2c28176cf46b058506658a21070679e0a91a4f94ed65245fb378e088603"

EXPECTED_FULLY_EXCLUDED_KEYS = (
    "W:E:01.12.1111010",
    "W:E:01.13.0101010",
    "W:E:03.07.01100",
    "W:E:04.08.10011",
    "W:E:06.02.1010101",
    "W:E:06.03.0000101",
)
EXPECTED_CROSS_SOURCE_SEAM_KEYS = (
    "W:E:00.15.0000000",
    "W:E:07.00.1111111",
)

REPLAY_CANDIDATE_IDS = {
    chart_id: tuple(base.candidate_ids(chart_id))
    for chart_id in CHARTS
}
REPLAY_TARGETS = {
    target.target_id: target for target in base.TARGETS
}


class VerificationError(RuntimeError):
    """Fail-closed Round175 verification error."""


@dataclass(frozen=True)
class BaseCell:
    t0: Q
    t1: Q
    s0: Q
    s1: Q
    depth: int
    path: str


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def digest(value: Any) -> str:
    return sha256_bytes(canonical_bytes(value))


def require(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


def closed_row(payload: dict[str, Any]) -> dict[str, Any]:
    row = copy.deepcopy(payload)
    row["row_sha256"] = digest(row)
    return row


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON key:{key}")
        result[key] = value
    return result


def reject_noninteger_number(value: str) -> None:
    raise VerificationError(f"non-integer JSON number:{value}")


def validate_json_tree(value: Any, path: str = "$") -> None:
    require(
        type(value) in {dict, list, str, int, bool, type(None)},
        f"JSON type:{path}",
    )
    if type(value) is dict:
        for key, child in value.items():
            require(type(key) is str and "\x00" not in key, f"key:{path}")
            require(
                not any(0xD800 <= ord(char) <= 0xDFFF for char in key),
                f"surrogate key:{path}",
            )
            validate_json_tree(child, f"{path}.{key}")
    elif type(value) is list:
        for index, child in enumerate(value):
            validate_json_tree(child, f"{path}[{index}]")
    elif type(value) is str:
        require("\x00" not in value, f"NUL string:{path}")
        require(
            not any(0xD800 <= ord(char) <= 0xDFFF for char in value),
            f"surrogate string:{path}",
        )


def read_regular(path: Path, expected_sha256: str | None = None) -> bytes:
    st = path.lstat()
    require(stat.S_ISREG(st.st_mode), f"not regular:{path.name}")
    require(not path.is_symlink(), f"symlink:{path.name}")
    require(st.st_nlink == 1, f"multiply linked:{path.name}")
    require(st.st_size <= MAX_INPUT_BYTES, f"oversized:{path.name}")
    data = path.read_bytes()
    if expected_sha256 is not None:
        require(sha256_bytes(data) == expected_sha256, f"pin:{path.name}")
    return data


def parse_envelope(
    data: bytes,
    *,
    label: str,
    expected_schema: str | None = None,
    require_canonical: bool,
) -> dict[str, Any]:
    require(not data.startswith(b"\xef\xbb\xbf"), f"BOM:{label}")
    require(b"\x00" not in data, f"raw NUL:{label}")
    try:
        value = json.loads(
            data.decode("utf-8", "strict"),
            object_pairs_hook=reject_duplicate_keys,
            parse_float=reject_noninteger_number,
            parse_constant=reject_noninteger_number,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise VerificationError(f"invalid JSON:{label}:{exc}") from exc
    validate_json_tree(value)
    require(type(value) is dict, f"top object:{label}")
    require(
        set(value) == {"schema", "result", "result_sha256"},
        f"envelope keys:{label}",
    )
    if expected_schema is not None:
        require(value["schema"] == expected_schema, f"schema:{label}")
    require(
        value["result_sha256"] == digest(value["result"]),
        f"result digest:{label}",
    )
    if require_canonical:
        require(
            data == canonical_bytes(value) + b"\n",
            f"canonical single-newline bytes:{label}",
        )
    return value


def load_pinned(name: str) -> dict[str, Any]:
    return parse_envelope(
        read_regular(HERE / name, PINS[name]),
        label=name,
        require_canonical=False,
    )


def independently_validate_chain() -> tuple[dict[str, Any], dict[str, Any]]:
    require(
        Path(atlas.__file__).resolve() == (HERE / ATLAS_SOURCE).resolve()
        and Path(base.__file__).resolve() == (HERE / BASE_SOURCE).resolve()
        and Path(atlas.ge.__file__).resolve() == (HERE / GE_SOURCE).resolve(),
        "module identities",
    )
    require(
        flint.__version__ == "0.9.0" and atlas.ctx.prec == 192,
        "python-flint environment",
    )
    read_regular(PRODUCER, EXPECTED_PRODUCER_SHA256)
    for name in (
        ATLAS_SOURCE,
        BASE_SOURCE,
        GE_SOURCE,
        R172_PRODUCER,
        R172_VERIFIER,
    ):
        read_regular(HERE / name, PINS[name])
    ownership = json.loads(
        canonical_bytes(
            json.loads(
                read_regular(HERE / OWNERSHIP, PINS[OWNERSHIP])
                    .decode("utf-8", "strict"),
                object_pairs_hook=reject_duplicate_keys,
                parse_float=reject_noninteger_number,
                parse_constant=reject_noninteger_number,
            )
        )
    )
    validate_json_tree(ownership)
    require(
        ownership["schema"] == "cm2.gate3.chart-seam-quotient.manifest.v1"
        and ownership["verdict"]["eight_chart_seam_ownership"] == "CERTIFIED"
        and ownership["verdict"]["rectangular_bulk_seam_quotient"]
        == "CERTIFIED"
        and ownership["result"]["scope_limits"][
            "ownership_rule_applies_to_analytic_strata"
        ] is True
        and ownership["result"]["scope_limits"][
            "all_eight_chart_seams_have_unique_owner"
        ] is True
        and ownership["result"]["unique_half_open_owner_rule"][
            "diagonal_tie"
        ] == "E or W owns; N or S excludes",
        "analytic seam ownership",
    )
    r172 = load_pinned(R172_CERT)
    v172 = load_pinned(R172_VER)
    require(
        r172["schema"]
        == (
            "cm2.round172.dimension-safe-tangency-parent-"
            "frozen-owner-absence-pruning.v1"
        )
        and r172["result_sha256"] == R172_RESULT,
        "Round172 certificate",
    )
    vr = v172["result"]
    require(
        v172["result_sha256"] == R172_VER_RESULT
        and vr["status"] == "PASS"
        and vr["certificate_result_sha256"] == R172_RESULT
        and vr["producer_sha256"] == PINS[R172_PRODUCER]
        and vr["verifier_sha256"] == PINS[R172_VERIFIER]
        and vr["independence_contract"][
            "source_W_atlas_independently_replayed_at_192_bits"
        ] is True
        and vr["independence_contract"][
            "all_32_tangency_parents_reconstructed"
        ] is True
        and vr["independence_contract"][
            "full_expected_canonical_equality"
        ] is True
        and vr["semantic_mutation_attack_suite"]["all_rejected"] is True
        and vr["strict_json_attack_suite"]["all_rejected"] is True
        and vr["path_safety_attack_suite"]["all_rejected"] is True,
        "Round172 verification",
    )
    composition = r172["result"]["Round168_to_Round172_composition"]
    require(
        composition["refined_source_W_record_count"] == 76832
        and composition["combined_whole_record_excluded"] == 73172
        and composition["Round172_conservative_live"] == 3660
        and composition["live_components"]
        == {
            "Round165_seam_live_composites": 504,
            "Round166_owner_active_multi": 2616,
            "original_stage_one_match": 518,
            "remaining_tangency_parent_composites": 22,
        }
        and composition["conservation_identity"] == "73172+3660=76832",
        "Round172 composition",
    )
    return r172, ownership


def decode_parent_box(key: str) -> tuple[str, atlas.AtlasBox]:
    parts = key.split(":")
    require(len(parts) == 3, f"parent key:{key}")
    chart_id = f"{parts[0]}:{parts[1]}"
    encoded_path = parts[2]
    reflected = encoded_path.startswith("H.")
    direct_path = encoded_path[2:] if reflected else encoded_path
    pieces = direct_path.split(".")
    require(len(pieces) == 3, f"atlas path:{key}")
    i, j = int(pieces[0]), int(pieces[1])
    bits = pieces[2]
    require(
        chart_id in CHARTS
        and 0 <= i < atlas.INITIAL_T
        and 0 <= j < atlas.INITIAL_P
        and set(bits) <= {"0", "1"},
        f"atlas path registry:{key}",
    )
    t0 = atlas.T_LOWER + (
        atlas.T_UPPER - atlas.T_LOWER
    ) * Q(i, atlas.INITIAL_T)
    t1 = atlas.T_LOWER + (
        atlas.T_UPPER - atlas.T_LOWER
    ) * Q(i + 1, atlas.INITIAL_T)
    p0 = atlas.P_LOWER + (
        atlas.P_UPPER - atlas.P_LOWER
    ) * Q(j, atlas.INITIAL_P)
    p1 = atlas.P_LOWER + (
        atlas.P_UPPER - atlas.P_LOWER
    ) * Q(j + 1, atlas.INITIAL_P)
    box = atlas.AtlasBox(
        t0,
        t1,
        p0,
        p1,
        atlas.S_LOWER,
        atlas.S_UPPER,
        0,
        f"{i:02d}.{j:02d}.",
    )
    for bit in bits:
        box = atlas.ge.split(box)[int(bit)]
    if reflected:
        box = atlas.AtlasBox(
            box.t0,
            box.t1,
            -box.p1,
            -box.p0,
            box.s0,
            box.s1,
            box.depth,
            "H." + box.path,
        )
    require(box.path == encoded_path, f"decoded path:{key}")
    return chart_id, box


def replay_records(
    chart_id: str,
    box: atlas.AtlasBox,
) -> list[atlas.RootRecord]:
    qx, qy, ux, uy, s, _cp = atlas.geometry(chart_id, box)
    rows: list[atlas.RootRecord] = []
    for target_id in REPLAY_CANDIDATE_IDS[chart_id]:
        target = REPLAY_TARGETS[target_id]
        center_x, center_y = base.target_center(target, s)
        dx, dy = center_x - qx, center_y - qy
        ell = ux * dx + uy * dy
        transverse = -uy * dx + ux * dy
        radius = base.arbq(base.RADIUS[target.obstacle])
        discriminant = radius * radius - transverse * transverse
        if bool(discriminant < 0):
            rows.append(atlas.RootRecord(
                target_id,
                "no_real_intersection",
                ell,
                discriminant,
                None,
                None,
                transverse,
            ))
            continue
        if not bool(discriminant > 0):
            rows.append(atlas.RootRecord(
                target_id,
                "unresolved_discriminant",
                ell,
                discriminant,
                None,
                None,
                transverse,
            ))
            continue
        radical = discriminant.sqrt()
        near, far = ell - radical, ell + radical
        if bool(far < 0):
            classification = "intersection_behind"
        elif bool(near > 0):
            classification = "strict_future_root"
        else:
            classification = "unresolved_root_sign"
        rows.append(atlas.RootRecord(
            target_id,
            classification,
            ell,
            discriminant,
            near,
            far,
            transverse,
        ))
    return rows


def fixed_p_box(
    box: atlas.AtlasBox,
    p: Q,
    *,
    t0: Q | None = None,
    t1: Q | None = None,
    s0: Q | None = None,
    s1: Q | None = None,
) -> atlas.AtlasBox:
    return atlas.AtlasBox(
        box.t0 if t0 is None else t0,
        box.t1 if t1 is None else t1,
        p,
        p,
        box.s0 if s0 is None else s0,
        box.s1 if s1 is None else s1,
        box.depth,
        box.path,
    )


def target_delta(
    chart_id: str,
    box: atlas.AtlasBox,
    target_id: str,
) -> Any:
    return next(
        row.discriminant for row in replay_records(chart_id, box)
        if row.target_id == target_id
    )


def seam_value_and_derivative(
    chart_id: str,
    box: atlas.AtlasBox,
    seam: str,
) -> tuple[Any, Any]:
    qx, qy, ux, uy, s, cp = atlas.geometry(chart_id, box)
    radius = base.arbq(base.RADIUS["W"])
    half = base.arbq(Q(1, 2))
    nx = (qx - (half + s)) / radius
    ny = (qy - half) / radius
    inv_sqrt_two = 1 / arb(2).sqrt()
    mx = -inv_sqrt_two
    my = inv_sqrt_two if seam == "NW" else -inv_sqrt_two
    dx = arb(1) + radius * mx - radius * nx
    dy = radius * my - radius * ny
    h_value = ux * dy - uy * dx
    p = base.arb_interval(box.p0, box.p1)
    dux = -(p / cp) * nx - ny
    duy = -(p / cp) * ny + nx
    derivative = dux * dy - duy * dx
    return h_value, derivative


def strict_sign(value: Any) -> str:
    if bool(value < 0):
        return "STRICT_NEGATIVE"
    if bool(value > 0):
        return "STRICT_POSITIVE"
    return "UNRESOLVED"


def source_chart_domain(box: atlas.AtlasBox, chart_id: str) -> dict[str, Any]:
    maximum_abs = max(abs(box.t0), abs(box.t1))
    minimum_abs = min(abs(box.t0), abs(box.t1))
    if box.t0 <= 0 <= box.t1:
        minimum_abs = Q(0)
    if 2 * maximum_abs * maximum_abs < 1:
        return {
            "classification": "STRICT_PHYSICAL_CHART_INTERIOR",
            "physical_chart_equation": "2*t^2<1",
            "source_chart_seam_present": False,
            "guard_outside_positive_volume_present": False,
            "guard_outside_exterior_exclusion_credit": 0,
        }
    require(
        2 * minimum_abs * minimum_abs < 1
        and 2 * maximum_abs * maximum_abs > 1
        and chart_id == "W:E",
        "supported source seam crossing",
    )
    return {
        "classification": "PHYSICAL_CHART_SEAM_AND_GUARD_OUTSIDE_COMPOSITE",
        "physical_chart_equation": "2*t^2=1",
        "source_chart_seam_present": True,
        "source_chart_seam_dimension": 2,
        "source_chart_seam_half_open_owner": "E",
        "physical_E_interior_positive_volume_present": True,
        "guard_outside_positive_volume_present": True,
        "guard_outside_disposition":
            "NEIGHBOR_CHART_RECOORDINATION_REQUIRED_NOT_EXTERIOR",
        "guard_outside_exterior_exclusion_credit": 0,
        "source_seam_intersection_strata": {
            "source_seam_intersect_Delta_nominal_dimension": 1,
            "source_seam_intersect_H_nominal_dimension": 1,
            "Delta_intersect_H_intersect_source_seam":
                "EMPTY_WHEN_DELTA_H_SEPARATION_APPLIES",
            "integer_exclusion_credit": 0,
        },
    }


def point_box(
    parent: atlas.AtlasBox,
    t: Q,
    p: Q,
    s: Q,
) -> atlas.AtlasBox:
    return atlas.AtlasBox(
        t,
        t,
        p,
        p,
        s,
        s,
        parent.depth,
        parent.path + ".round175-independent-point",
    )


def first_hit(chart_id: str, point: atlas.AtlasBox) -> atlas.Leaf:
    original = atlas.records
    atlas.records = replay_records
    try:
        return atlas.classify_box(chart_id, point)
    finally:
        atlas.records = original


def edge_adaptive_grid(lower: Q, upper: Q) -> list[Q]:
    fractions: list[Q] = [Q(1, 2)]
    for exponent in range(2, 16):
        denominator = 2 ** exponent
        fractions.extend((
            Q(1, denominator),
            Q(denominator - 1, denominator),
        ))
    fractions.extend(Q(index, 32) for index in range(1, 32))
    return [
        lower + (upper - lower) * fraction
        for fraction in sorted(set(fractions))
    ]


def strict_point_witness(
    chart_id: str,
    parent: atlas.AtlasBox,
    tangency_target: str,
    want_live: bool,
) -> dict[str, Any]:
    for t in edge_adaptive_grid(parent.t0, parent.t1):
        if 2 * t * t >= 1:
            continue
        for p in edge_adaptive_grid(parent.p0, parent.p1):
            point = point_box(parent, t, p, Q(0))
            records = replay_records(chart_id, point)
            frozen = next(
                row for row in records if row.target_id == FROZEN_OWNER
            )
            target = next(
                row for row in records if row.target_id == tangency_target
            )
            nw, _ = seam_value_and_derivative(chart_id, point, "NW")
            sw, _ = seam_value_and_derivative(chart_id, point, "SW")
            if want_live:
                if not (
                    frozen.classification == "strict_future_root"
                    and bool(nw > 0)
                    and bool(sw < 0)
                ):
                    continue
                leaf = first_hit(chart_id, point)
                if not (
                    leaf.classification == "unique_first"
                    and leaf.owner_target == FROZEN_OWNER
                ):
                    continue
                disposition = "STRICT_FROZEN_W_FIRST_OUTGOING_W_LIVE"
            elif tangency_target == FROZEN_OWNER:
                if not (
                    frozen.classification == "no_real_intersection"
                    and bool(frozen.discriminant < 0)
                ):
                    continue
                leaf = first_hit(chart_id, point)
                disposition = "STRICT_FROZEN_OWNER_ABSENT_MISMATCH"
            else:
                if target.classification != "strict_future_root":
                    continue
                leaf = first_hit(chart_id, point)
                if not (
                    leaf.classification == "unique_first"
                    and leaf.owner_target == tangency_target
                ):
                    continue
                disposition = "STRICT_MISMATCH_TARGET_FIRST"
            return {
                "point": {"t": str(t), "p": str(p), "s": "0"},
                "source_physical_chart_interior": True,
                "classification": disposition,
                "first_hit_classification": leaf.classification,
                "first_owner": leaf.owner_target,
                "frozen_owner_record": frozen.classification,
                "frozen_owner_discriminant_sign":
                    strict_sign(frozen.discriminant),
                "tangency_target_record": target.classification,
                "H_NW_sign": strict_sign(nw),
                "H_SW_sign": strict_sign(sw),
            }
    raise VerificationError(
        f"strict {'live' if want_live else 'mismatch'} witness:"
        f"{chart_id}:{parent.path}"
    )


def base_cell_box(
    parent: atlas.AtlasBox,
    cell: BaseCell,
    p: Q,
) -> atlas.AtlasBox:
    return fixed_p_box(
        parent,
        p,
        t0=cell.t0,
        t1=cell.t1,
        s0=cell.s0,
        s1=cell.s1,
    )


def split_base_cell(cell: BaseCell) -> tuple[BaseCell, BaseCell]:
    if cell.t1 - cell.t0 >= cell.s1 - cell.s0:
        middle = (cell.t0 + cell.t1) / 2
        return (
            BaseCell(
                cell.t0,
                middle,
                cell.s0,
                cell.s1,
                cell.depth + 1,
                cell.path + "0",
            ),
            BaseCell(
                middle,
                cell.t1,
                cell.s0,
                cell.s1,
                cell.depth + 1,
                cell.path + "1",
            ),
        )
    middle = (cell.s0 + cell.s1) / 2
    return (
        BaseCell(
            cell.t0,
            cell.t1,
            cell.s0,
            middle,
            cell.depth + 1,
            cell.path + "0",
        ),
        BaseCell(
            cell.t0,
            cell.t1,
            middle,
            cell.s1,
            cell.depth + 1,
            cell.path + "1",
        ),
    )


def bracket_graph(
    function: Callable[[BaseCell, Q], Any],
    cell: BaseCell,
    p0: Q,
    p1: Q,
) -> tuple[Q, Q] | None:
    sign0 = strict_sign(function(cell, p0))
    sign1 = strict_sign(function(cell, p1))
    if "UNRESOLVED" in (sign0, sign1) or sign0 == sign1:
        return None
    for _step in range(BRACKET_STEPS):
        middle = (p0 + p1) / 2
        middle_sign = strict_sign(function(cell, middle))
        if middle_sign == "UNRESOLVED":
            break
        if middle_sign == sign0:
            p0, sign0 = middle, middle_sign
        else:
            p1, sign1 = middle, middle_sign
    return p0, p1


def exception_graph_separation(
    chart_id: str,
    parent: atlas.AtlasBox,
    tangency_target: str,
    seam: str,
) -> list[dict[str, Any]]:
    pending = [
        BaseCell(parent.t0, parent.t1, parent.s0, parent.s1, 0, "")
    ]
    terminal: list[dict[str, Any]] = []

    def delta_function(cell: BaseCell, p: Q) -> Any:
        return target_delta(
            chart_id,
            base_cell_box(parent, cell, p),
            tangency_target,
        )

    def h_function(cell: BaseCell, p: Q) -> Any:
        return seam_value_and_derivative(
            chart_id,
            base_cell_box(parent, cell, p),
            seam,
        )[0]

    while pending:
        cell = pending.pop()
        delta_bracket = bracket_graph(
            delta_function,
            cell,
            parent.p0,
            parent.p1,
        )
        h_bracket = bracket_graph(
            h_function,
            cell,
            parent.p0,
            parent.p1,
        )
        relation: str | None = None
        if delta_bracket is not None and h_bracket is not None:
            if h_bracket[1] < delta_bracket[0]:
                relation = "H_GRAPH_STRICTLY_BELOW_DELTA_GRAPH"
            elif delta_bracket[1] < h_bracket[0]:
                relation = "DELTA_GRAPH_STRICTLY_BELOW_H_GRAPH"
        if relation is None:
            require(
                cell.depth < MAX_EXCEPTION_BASE_DEPTH,
                "exception graph separation depth",
            )
            pending.extend(split_base_cell(cell))
            continue
        expected = (
            "H_GRAPH_STRICTLY_BELOW_DELTA_GRAPH"
            if chart_id == "W:N"
            else "DELTA_GRAPH_STRICTLY_BELOW_H_GRAPH"
        )
        require(relation == expected, "exception graph order")
        terminal.append(closed_row({
            "base_cell_path": cell.path,
            "base_cell_depth": cell.depth,
            "t": [str(cell.t0), str(cell.t1)],
            "s": [str(cell.s0), str(cell.s1)],
            "delta_graph_p_bracket": [
                str(delta_bracket[0]),
                str(delta_bracket[1]),
            ],
            "H_graph_p_bracket": [
                str(h_bracket[0]),
                str(h_bracket[1]),
            ],
            "strict_graph_order": relation,
            "H_graph_lies_in_mismatch_target_Delta_negative_side": True,
            "Delta_intersect_H": "EMPTY_ON_BASE_CELL",
        }))
    terminal.sort(key=lambda row: row["base_cell_path"])
    area = sum(
        (Q(row["t"][1]) - Q(row["t"][0]))
        * (Q(row["s"][1]) - Q(row["s"][0]))
        for row in terminal
    )
    require(
        area == (parent.t1 - parent.t0) * (parent.s1 - parent.s0),
        "exception base partition area",
    )
    return terminal


def parent_arrangement(upstream_row: dict[str, Any]) -> dict[str, Any]:
    key = upstream_row["ambient_leaf_key"]
    chart_id, parent = decode_parent_box(key)
    tangency_target = upstream_row["Round164_tangency_target"]
    records = replay_records(chart_id, parent)
    tangency_record = next(
        row for row in records if row.target_id == tangency_target
    )
    require(
        atlas.physical_tangency_graph(
            chart_id,
            parent,
            tangency_record,
            records,
        ),
        f"physical tangency graph:{key}",
    )
    domain = source_chart_domain(parent, chart_id)
    nw, nw_derivative = seam_value_and_derivative(chart_id, parent, "NW")
    sw, sw_derivative = seam_value_and_derivative(chart_id, parent, "SW")
    nw_sign, sw_sign = strict_sign(nw), strict_sign(sw)
    owner_graph = tangency_target == FROZEN_OWNER
    if sw_sign == "STRICT_NEGATIVE":
        relevant_seam, adjacent_chart = "H_NW", "N"
        relevant_value, relevant_derivative = nw, nw_derivative
        mismatch_sign, live_sign = "STRICT_NEGATIVE", "STRICT_POSITIVE"
        compatible_guard = "H_SW_STRICT_NEGATIVE"
    elif nw_sign == "STRICT_POSITIVE":
        relevant_seam, adjacent_chart = "H_SW", "S"
        relevant_value, relevant_derivative = sw, sw_derivative
        mismatch_sign, live_sign = "STRICT_POSITIVE", "STRICT_NEGATIVE"
        compatible_guard = "H_NW_STRICT_POSITIVE"
    else:
        raise VerificationError(f"outgoing guard:{key}")
    require(
        strict_sign(relevant_derivative) == "STRICT_NEGATIVE",
        f"strict H derivative:{key}",
    )
    relevant_sign = strict_sign(relevant_value)
    exception_cells: list[dict[str, Any]] = []
    if owner_graph and relevant_sign == mismatch_sign:
        require(
            domain["classification"] == "STRICT_PHYSICAL_CHART_INTERIOR",
            f"full exclusion inside physical chart:{key}",
        )
        classification = "FULLY_EXCLUDED"
        live_witness = None
        mismatch_witness = None
        delta_h = {
            "status": "EMPTY_NO_H_ZERO_IN_PARENT",
            "nominal_dimension_if_nonempty": 1,
            "integer_credit": 0,
        }
        h_graph = {
            "present": False,
            "reason": f"{relevant_seam} is {relevant_sign} on whole parent",
        }
    else:
        require(relevant_sign == "UNRESOLVED", f"mixed seam interval:{key}")
        classification = "MIXED_COMPOSITE"
        live_witness = strict_point_witness(
            chart_id,
            parent,
            tangency_target,
            True,
        )
        mismatch_witness = strict_point_witness(
            chart_id,
            parent,
            tangency_target,
            False,
        )
        h_graph = {
            "present": True,
            "kind": "UNIQUE_MONOTONE_CLIPPED_P_GRAPH",
            "equation": f"{relevant_seam}=0",
            "dimension": 2,
            "strict_p_derivative_sign": "STRICT_NEGATIVE",
            "half_open_owner": "W",
            "adjacent_excluded_chart": adjacent_chart,
            "boundary_clipping_or_grazing_nominal_dimension": 1,
            "boundary_component_count_fully_isolated": False,
            "boundary_integer_credit": 0,
        }
        if owner_graph:
            delta_h = {
                "status": "EMPTY_CERTIFIED",
                "nominal_dimension_if_nonempty": 1,
                "proof": (
                    "on H=0 the diagonal-contact chord has "
                    "|dot(D,m)|>1/sqrt(2)-2R_W>19/50, so Delta_W>0"
                ),
                "inverse_sqrt_two_rational_lower_bound": "7/10",
                "diagonal_contact_chord_dot_abs_lower_bound": "19/50",
                "H_graph_lies_strictly_in_Delta_positive_W_first_side":
                    True,
                "integer_credit": 0,
            }
        else:
            seam = "NW" if relevant_seam == "H_NW" else "SW"
            exception_cells = exception_graph_separation(
                chart_id,
                parent,
                tangency_target,
                seam,
            )
            delta_h = {
                "status": "EMPTY_CERTIFIED_BY_ADAPTIVE_GRAPH_BRACKETS",
                "nominal_dimension_if_nonempty": 1,
                "terminal_base_cell_count": len(exception_cells),
                "maximum_extra_base_depth_used": max(
                    row["base_cell_depth"] for row in exception_cells
                ),
                "all_terminal_base_cells_sha256": digest(exception_cells),
                "all_terminal_base_cells": exception_cells,
                "H_graph_lies_strictly_in_mismatch_target_Delta_negative_side":
                    True,
                "integer_credit": 0,
            }
    arrangement = {
        "ambient_leaf_key": key,
        "chart_id": chart_id,
        "atlas_path": parent.path,
        "parent_box": {
            "t": [str(parent.t0), str(parent.t1)],
            "p": [str(parent.p0), str(parent.p1)],
            "s": [str(parent.s0), str(parent.s1)],
            "ambient_dimension": 3,
        },
        "Round172_resolution": upstream_row["resolution"],
        "tangency_target": tangency_target,
        "tangency_target_is_frozen_owner": owner_graph,
        "source_chart_domain": domain,
        "delta_arrangement": {
            "equation": f"Delta[{tangency_target}]=0",
            "strictly_monotone_p_graph": True,
            "delta_negative_open_side_dimension": 3,
            "delta_zero_graph_dimension": 2,
            "delta_positive_open_side_dimension": 3,
            "delta_zero_half_open_owner": (
                "W" if owner_graph else "MISMATCH_TARGET"
            ),
            "owner_graph_orientation": (
                {
                    "Delta_negative": "FROZEN_OWNER_ABSENT_MISMATCH",
                    "Delta_zero": "W_OWNED_TANGENCY_GRAPH",
                    "Delta_positive": "W_FIRST_SIDE",
                }
                if owner_graph
                else {
                    "Delta_negative":
                        "MISMATCH_TARGET_ABSENT_CONTAINS_FROZEN_W_LIVE_REGION",
                    "Delta_zero": "MISMATCH_TARGET_TANGENCY_GRAPH",
                    "Delta_positive": "MISMATCH_TARGET_FIRST_SIDE",
                }
            ),
        },
        "outgoing_arrangement": {
            "relevant_seam": relevant_seam,
            "adjacent_mismatch_chart": adjacent_chart,
            "compatible_guard": compatible_guard,
            "whole_parent_relevant_H_sign": relevant_sign,
            "mismatch_H_sign": mismatch_sign,
            "W_live_H_sign": live_sign,
            "H_graph": h_graph,
            "Delta_intersect_H": delta_h,
        },
        "strict_live_open_witness": live_witness,
        "strict_mismatch_open_witness": mismatch_witness,
        "classification": classification,
        "whole_parent_new_integer_exclusion":
            classification == "FULLY_EXCLUDED",
        "conservative_live_composite":
            classification == "MIXED_COMPOSITE",
        "analytic_internal_strata_added_to_integer_record_count": False,
        "guard_outside_or_residual_integer_credit": 0,
    }
    return closed_row(arrangement)


def audit_fully_excluded_row(row: dict[str, Any]) -> dict[str, Any]:
    delta = row["delta_arrangement"]
    outgoing = row["outgoing_arrangement"]
    require(
        row["ambient_leaf_key"] in EXPECTED_FULLY_EXCLUDED_KEYS
        and row["tangency_target_is_frozen_owner"] is True
        and row["tangency_target"] == FROZEN_OWNER
        and row["source_chart_domain"]
        == {
            "classification": "STRICT_PHYSICAL_CHART_INTERIOR",
            "physical_chart_equation": "2*t^2<1",
            "source_chart_seam_present": False,
            "guard_outside_positive_volume_present": False,
            "guard_outside_exterior_exclusion_credit": 0,
        }
        and delta["delta_negative_open_side_dimension"] == 3
        and delta["delta_zero_graph_dimension"] == 2
        and delta["delta_positive_open_side_dimension"] == 3
        and delta["delta_zero_half_open_owner"] == "W"
        and delta["owner_graph_orientation"]
        == {
            "Delta_negative": "FROZEN_OWNER_ABSENT_MISMATCH",
            "Delta_zero": "W_OWNED_TANGENCY_GRAPH",
            "Delta_positive": "W_FIRST_SIDE",
        }
        and outgoing["whole_parent_relevant_H_sign"]
        == outgoing["mismatch_H_sign"]
        and outgoing["whole_parent_relevant_H_sign"]
        in {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
        and outgoing["H_graph"]["present"] is False
        and outgoing["Delta_intersect_H"]["status"]
        == "EMPTY_NO_H_ZERO_IN_PARENT"
        and row["strict_live_open_witness"] is None
        and row["strict_mismatch_open_witness"] is None
        and row["whole_parent_new_integer_exclusion"] is True
        and row["guard_outside_or_residual_integer_credit"] == 0,
        f"complete credited strata:{row['ambient_leaf_key']}",
    )
    return {
        "ambient_leaf_key": row["ambient_leaf_key"],
        "physical_source_chart_strata": "STRICT_INTERIOR_ONLY",
        "Delta_negative_stratum": "MISMATCH_BY_FROZEN_OWNER_ABSENCE",
        "Delta_zero_stratum": "MISMATCH_BY_W_OWNED_TANGENCY_PLUS_H_SIGN",
        "Delta_positive_stratum": "MISMATCH_BY_W_FIRST_PLUS_H_SIGN",
        "relevant_H_zero_stratum": "EMPTY_ON_PARENT",
        "source_chart_seam_stratum": "EMPTY_ON_PARENT",
        "guard_outside_stratum": "EMPTY_ON_PARENT",
        "all_physical_strata_mismatch": True,
        "row_sha256": row["row_sha256"],
    }


def independently_reconstruct_result(
    producer_sha256: str,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    r172, _ownership = independently_validate_chain()
    upstream_rows = [
        row for row in r172["result"]["independent_192_bit_atlas_replay"][
            "all_32_parent_rows"
        ]
        if row["remaining_live_composite"]
    ]
    require(len(upstream_rows) == 22, "Round172 remaining parents")
    rows = [parent_arrangement(row) for row in upstream_rows]
    rows.sort(key=lambda row: row["ambient_leaf_key"])
    fully_excluded = [
        row for row in rows if row["classification"] == "FULLY_EXCLUDED"
    ]
    fully_live = [
        row for row in rows if row["classification"] == "FULLY_LIVE"
    ]
    mixed = [
        row for row in rows if row["classification"] == "MIXED_COMPOSITE"
    ]
    excluded_keys = tuple(
        row["ambient_leaf_key"] for row in fully_excluded
    )
    cross_keys = tuple(
        row["ambient_leaf_key"] for row in rows
        if row["source_chart_domain"]["classification"]
        == "PHYSICAL_CHART_SEAM_AND_GUARD_OUTSIDE_COMPOSITE"
    )
    require(excluded_keys == EXPECTED_FULLY_EXCLUDED_KEYS, "exact six closures")
    require(
        cross_keys == EXPECTED_CROSS_SOURCE_SEAM_KEYS,
        "exact source guard crossings",
    )
    require(
        (
            len(rows),
            len(fully_excluded),
            len(fully_live),
            len(mixed),
        ) == (22, 6, 0, 16),
        "22/6/0/16 parent census",
    )
    audits = [audit_fully_excluded_row(row) for row in fully_excluded]
    require(
        all(
            row["strict_live_open_witness"] is not None
            and row["strict_mismatch_open_witness"] is not None
            and row["whole_parent_new_integer_exclusion"] is False
            and row["conservative_live_composite"] is True
            and row["outgoing_arrangement"]["H_graph"]["present"] is True
            and row["outgoing_arrangement"]["H_graph"]["dimension"] == 2
            and row["outgoing_arrangement"]["H_graph"][
                "strict_p_derivative_sign"
            ] == "STRICT_NEGATIVE"
            and row["outgoing_arrangement"]["H_graph"][
                "half_open_owner"
            ] == "W"
            and row["outgoing_arrangement"]["Delta_intersect_H"][
                "integer_credit"
            ] == 0
            and row["analytic_internal_strata_added_to_integer_record_count"]
            is False
            and row["guard_outside_or_residual_integer_credit"] == 0
            for row in mixed
        ),
        "all mixed open witnesses and noncredit",
    )
    exception_rows = [
        row for row in rows
        if not row["tangency_target_is_frozen_owner"]
    ]
    require(
        len(exception_rows) == 2
        and all(
            row["classification"] == "MIXED_COMPOSITE"
            and row["delta_arrangement"]["owner_graph_orientation"]
            == {
                "Delta_negative":
                    "MISMATCH_TARGET_ABSENT_CONTAINS_FROZEN_W_LIVE_REGION",
                "Delta_zero": "MISMATCH_TARGET_TANGENCY_GRAPH",
                "Delta_positive": "MISMATCH_TARGET_FIRST_SIDE",
            }
            and row["outgoing_arrangement"]["Delta_intersect_H"]["status"]
            == "EMPTY_CERTIFIED_BY_ADAPTIVE_GRAPH_BRACKETS"
            and row["outgoing_arrangement"]["Delta_intersect_H"][
                "terminal_base_cell_count"
            ] == 18
            and row["outgoing_arrangement"]["Delta_intersect_H"][
                "maximum_extra_base_depth_used"
            ] == 6
            and row["outgoing_arrangement"]["Delta_intersect_H"][
                "H_graph_lies_strictly_in_mismatch_target_Delta_negative_side"
            ] is True
            for row in exception_rows
        ),
        "two exception arrangements",
    )
    cross_rows = [
        row for row in rows
        if row["ambient_leaf_key"] in EXPECTED_CROSS_SOURCE_SEAM_KEYS
    ]
    require(
        all(
            row["classification"] == "MIXED_COMPOSITE"
            and row["source_chart_domain"][
                "physical_chart_equation"
            ] == "2*t^2=1"
            and row["source_chart_domain"][
                "source_chart_seam_dimension"
            ] == 2
            and row["source_chart_domain"][
                "source_chart_seam_half_open_owner"
            ] == "E"
            and row["source_chart_domain"][
                "guard_outside_positive_volume_present"
            ] is True
            and row["source_chart_domain"][
                "guard_outside_disposition"
            ] == "NEIGHBOR_CHART_RECOORDINATION_REQUIRED_NOT_EXTERIOR"
            and row["source_chart_domain"][
                "guard_outside_exterior_exclusion_credit"
            ] == 0
            for row in cross_rows
        ),
        "source seam versus rational guard",
    )
    prior_excluded = 73172
    new_excluded = 6
    combined_excluded = prior_excluded + new_excluded
    live_components = {
        "original_stage_one_match": 518,
        "Round165_seam_live_composites": 504,
        "Round175_remaining_mixed_tangency_composites": 16,
        "Round166_owner_active_multi": 2616,
    }
    live_total = sum(live_components.values())
    require(
        combined_excluded == 73178
        and live_total == 3654
        and combined_excluded + live_total == 76832,
        "Round175 conservation",
    )
    result = {
        "status": (
            "CERTIFIED_6_ADDITIONAL_WHOLE_TANGENCY_PARENT_EXCLUSIONS_"
            "WITH_16_EXACT_RESIDUAL_ARRANGEMENTS__D02_STILL_BLOCKED"
        ),
        "frozen_prefix": {
            "source_obstacle": "W",
            "collision_index": 1,
            "required_owner": FROZEN_OWNER,
            "required_outgoing_chart": FROZEN_OUTGOING,
            "stage_one_only": True,
        },
        "parent_arrangement_census": {
            "input_Round172_tangency_composites": 22,
            "fully_excluded_parent_count": len(fully_excluded),
            "fully_live_parent_count": len(fully_live),
            "mixed_composite_parent_count": len(mixed),
            "whole_parent_closure_count": len(fully_excluded),
            "exact_residual_arrangement_count": len(mixed),
            "frozen_owner_tangency_parent_count": 20,
            "mismatch_tangency_exception_parent_count": 2,
            "physical_source_chart_cross_seam_parent_count":
                len(cross_keys),
            "all_22_parent_rows_sha256": digest(rows),
            "all_22_parent_rows": rows,
        },
        "new_whole_parent_exclusion_credit": {
            "new_whole_parent_exclusion_count": new_excluded,
            "exact_parent_keys": list(excluded_keys),
            "exact_parent_keys_sha256": digest(list(excluded_keys)),
            "all_strata_mismatch_required": True,
            "all_six_strictly_inside_physical_source_chart": True,
            "credit_from_2D_graph_or_guard_slice": 0,
            "credited_parent_rows_sha256": digest(fully_excluded),
        },
        "residual_arrangement_ledger": {
            "mixed_parent_count": len(mixed),
            "mixed_parent_keys": [
                row["ambient_leaf_key"] for row in mixed
            ],
            "mixed_parent_keys_sha256": digest([
                row["ambient_leaf_key"] for row in mixed
            ]),
            "all_have_strict_live_and_mismatch_open_witnesses": True,
            "analytic_strata_not_added_to_integer_record_count": True,
            "source_chart_cross_seam_keys": list(cross_keys),
            "source_chart_cross_seam_keys_sha256": digest(list(cross_keys)),
            "source_chart_seam_equation": "2*t^2=1",
            "atlas_rational_guard_band": "[-177/250,177/250]",
            "guard_outside_is_chart_domain_rejection_not_exterior_exclusion":
                True,
            "guard_outside_integer_exclusion_credit": 0,
            "physical_diagonal_half_open_owner_rule":
                "E or W owns; N or S excludes",
            "all_live_H_seams_half_open_owned_by_W": True,
        },
        "Round172_to_Round175_composition": {
            "refined_source_W_record_count": 76832,
            "Round172_whole_record_excluded": prior_excluded,
            "Round175_new_whole_parent_excluded": new_excluded,
            "combined_whole_record_excluded": combined_excluded,
            "new_credit_disjoint_from_Round172_credit": True,
            "Round172_conservative_live": 3660,
            "Round175_conservative_live": live_total,
            "live_components": live_components,
            "conservation_identity": "73178+3654=76832",
            "refined_total_unchanged": True,
        },
        "dimension_safe_noncredit": {
            "Delta_zero_graph_whole_parent_credit": 0,
            "outgoing_H_zero_seam_whole_parent_credit": 0,
            "Delta_intersect_H_or_boundary_corner_integer_credit": 0,
            "source_chart_guard_outside_exterior_exclusion_credit": 0,
            "sixteen_mixed_internal_mismatch_strata_whole_parent_credit": 0,
            "Round165_typed_collar_mismatch_side_whole_record_credit": 0,
            "Round166_deep_refinement_profile_whole_record_credit": 0,
        },
        "scope": {
            "every_integer_credit_requires_all_physical_strata_mismatch":
                True,
            "physical_chart_seam_distinguished_from_rational_guard_band":
                True,
            "cross_seam_positive_volume_tubes_remain_residual": True,
            "not_later_frozen_prefix_resolution": True,
            "not_exterior_sheet_exhaustion": True,
            "not_D02_closure": True,
        },
        "strict_nonpromotion": {
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate": (
            "isolate the boundary-clipping and source-chart cross-seam "
            "residual strata in all 16 mixed tangency composites, continue "
            "later frozen-prefix processing only on certified live strata, "
            "continue the 224 whole-W rectangles, and resolve the 2,616 "
            "owner-active multi parents"
        ),
        "provenance": {
            "schema": CERTIFICATE_SCHEMA,
            "producer_sha256": producer_sha256,
            "dependency_sha256": dict(sorted(PINS.items())),
            "python_flint_version": flint.__version__,
            "arb_context_precision_bits": atlas.ctx.prec,
            "Round172_producer_or_verifier_imported_or_executed": False,
            "parent_boxes_reconstructed_from_pinned_dyadic_paths": True,
            "older_round_files_modified": False,
        },
    }
    return result, audits


def exact_key_tree(actual: Any, expected: Any, path: str = "$") -> None:
    require(type(actual) is type(expected), f"type:{path}")
    if type(expected) is dict:
        require(set(actual) == set(expected), f"keys:{path}")
        for key in expected:
            exact_key_tree(actual[key], expected[key], f"{path}.{key}")
    elif type(expected) is list:
        require(len(actual) == len(expected), f"length:{path}")
        for index, (left, right) in enumerate(zip(actual, expected)):
            exact_key_tree(left, right, f"{path}[{index}]")


def validate_certificate_document(
    document: dict[str, Any],
    expected_document: dict[str, Any],
) -> None:
    exact_key_tree(document, expected_document)
    require(document["schema"] == CERTIFICATE_SCHEMA, "certificate schema")
    require(
        document["result_sha256"] == digest(document["result"]),
        "certificate result digest",
    )
    require(
        document["result_sha256"] == EXPECTED_CERTIFICATE_RESULT_SHA256,
        "frozen certificate result",
    )
    require(
        canonical_bytes(document) == canonical_bytes(expected_document),
        "full expected canonical equality",
    )


def set_path(document: dict[str, Any], path: tuple[Any, ...], value: Any) -> None:
    node: Any = document
    for component in path[:-1]:
        node = node[component]
    node[path[-1]] = value


def delete_path(document: dict[str, Any], path: tuple[Any, ...]) -> None:
    node: Any = document
    for component in path[:-1]:
        node = node[component]
    if type(node) is list:
        del node[path[-1]]
    else:
        del node[path[-1]]


def resigned(
    document: dict[str, Any],
    mutate: Callable[[dict[str, Any]], None],
) -> dict[str, Any]:
    candidate = copy.deepcopy(document)
    mutate(candidate)
    candidate["result_sha256"] = digest(candidate["result"])
    return candidate


def semantic_attacks(
    document: dict[str, Any],
    expected_document: dict[str, Any],
) -> dict[str, Any]:
    rows = document["result"]["parent_arrangement_census"][
        "all_22_parent_rows"
    ]
    excluded_indices = [
        index for index, row in enumerate(rows)
        if row["classification"] == "FULLY_EXCLUDED"
    ]
    mixed_indices = [
        index for index, row in enumerate(rows)
        if row["classification"] == "MIXED_COMPOSITE"
    ]
    exception_index = next(
        index for index, row in enumerate(rows)
        if not row["tangency_target_is_frozen_owner"]
    )
    cross_index = next(
        index for index, row in enumerate(rows)
        if row["source_chart_domain"]["classification"]
        == "PHYSICAL_CHART_SEAM_AND_GUARD_OUTSIDE_COMPOSITE"
    )
    e0 = excluded_indices[0]
    m0 = mixed_indices[0]
    prefix = ("result",)
    census = prefix + ("parent_arrangement_census",)
    row_base = census + ("all_22_parent_rows",)
    credit = prefix + ("new_whole_parent_exclusion_credit",)
    residual = prefix + ("residual_arrangement_ledger",)
    composition = prefix + ("Round172_to_Round175_composition",)
    noncredit = prefix + ("dimension_safe_noncredit",)
    scope = prefix + ("scope",)
    nonpromotion = prefix + ("strict_nonpromotion",)
    specs: list[tuple[str, tuple[Any, ...], Any]] = [
        ("schema", ("schema",), "mutated"),
        ("status", prefix + ("status",), "PASS"),
        ("source obstacle", prefix + ("frozen_prefix", "source_obstacle"), "G"),
        ("collision index", prefix + ("frozen_prefix", "collision_index"), 2),
        ("required owner", prefix + ("frozen_prefix", "required_owner"), "G[1,0]"),
        ("required outgoing", prefix + ("frozen_prefix", "required_outgoing_chart"), "N"),
        ("stage one scope", prefix + ("frozen_prefix", "stage_one_only"), False),
        ("input census", census + ("input_Round172_tangency_composites",), 21),
        ("excluded census", census + ("fully_excluded_parent_count",), 7),
        ("fully live census", census + ("fully_live_parent_count",), 1),
        ("mixed census", census + ("mixed_composite_parent_count",), 15),
        ("closure census", census + ("whole_parent_closure_count",), 5),
        ("residual census", census + ("exact_residual_arrangement_count",), 15),
        ("owner census", census + ("frozen_owner_tangency_parent_count",), 19),
        ("exception census", census + ("mismatch_tangency_exception_parent_count",), 1),
        ("cross seam census", census + ("physical_source_chart_cross_seam_parent_count",), 1),
        ("all rows digest", census + ("all_22_parent_rows_sha256",), "0" * 64),
        ("parent key", row_base + (e0, "ambient_leaf_key"), "forged"),
        ("chart id", row_base + (e0, "chart_id"), "W:N"),
        ("atlas path", row_base + (e0, "atlas_path"), "forged"),
        ("parent t bound", row_base + (e0, "parent_box", "t", 0), "0"),
        ("parent p bound", row_base + (e0, "parent_box", "p", 1), "0"),
        ("parent s bound", row_base + (e0, "parent_box", "s", 0), "1"),
        ("parent dimension", row_base + (e0, "parent_box", "ambient_dimension"), 2),
        ("Round172 binding", row_base + (e0, "Round172_resolution"), "forged"),
        ("tangency target", row_base + (e0, "tangency_target"), "W[0,0]"),
        ("owner graph flag", row_base + (e0, "tangency_target_is_frozen_owner"), False),
        ("physical source class", row_base + (e0, "source_chart_domain", "classification"), "GUARD"),
        ("physical equation", row_base + (e0, "source_chart_domain", "physical_chart_equation"), "2*t^2<=1"),
        ("source seam presence", row_base + (e0, "source_chart_domain", "source_chart_seam_present"), True),
        ("guard presence", row_base + (e0, "source_chart_domain", "guard_outside_positive_volume_present"), True),
        ("guard row credit", row_base + (e0, "source_chart_domain", "guard_outside_exterior_exclusion_credit"), 1),
        ("Delta equation", row_base + (e0, "delta_arrangement", "equation"), "Delta=1"),
        ("Delta monotonicity", row_base + (e0, "delta_arrangement", "strictly_monotone_p_graph"), False),
        ("Delta negative dimension", row_base + (e0, "delta_arrangement", "delta_negative_open_side_dimension"), 2),
        ("Delta zero dimension", row_base + (e0, "delta_arrangement", "delta_zero_graph_dimension"), 3),
        ("Delta positive dimension", row_base + (e0, "delta_arrangement", "delta_positive_open_side_dimension"), 2),
        ("Delta zero owner", row_base + (e0, "delta_arrangement", "delta_zero_half_open_owner"), "N"),
        ("Delta negative orientation", row_base + (e0, "delta_arrangement", "owner_graph_orientation", "Delta_negative"), "LIVE"),
        ("Delta zero orientation", row_base + (e0, "delta_arrangement", "owner_graph_orientation", "Delta_zero"), "MISMATCH"),
        ("Delta positive orientation", row_base + (e0, "delta_arrangement", "owner_graph_orientation", "Delta_positive"), "LIVE"),
        ("relevant H", row_base + (e0, "outgoing_arrangement", "relevant_seam"), "H_FAKE"),
        ("adjacent chart", row_base + (e0, "outgoing_arrangement", "adjacent_mismatch_chart"), "E"),
        ("compatible guard", row_base + (e0, "outgoing_arrangement", "compatible_guard"), "forged"),
        ("whole H sign", row_base + (e0, "outgoing_arrangement", "whole_parent_relevant_H_sign"), "UNRESOLVED"),
        ("mismatch H sign", row_base + (e0, "outgoing_arrangement", "mismatch_H_sign"), "STRICT_POSITIVE"),
        ("live H sign", row_base + (e0, "outgoing_arrangement", "W_live_H_sign"), "STRICT_NEGATIVE"),
        ("credited H graph forged", row_base + (e0, "outgoing_arrangement", "H_graph", "present"), True),
        ("credited Delta H status", row_base + (e0, "outgoing_arrangement", "Delta_intersect_H", "status"), "NONEMPTY"),
        ("credited Delta H credit", row_base + (e0, "outgoing_arrangement", "Delta_intersect_H", "integer_credit"), 1),
        ("credited classification", row_base + (e0, "classification"), "MIXED_COMPOSITE"),
        ("credited exclusion flag", row_base + (e0, "whole_parent_new_integer_exclusion"), False),
        ("credited live flag", row_base + (e0, "conservative_live_composite"), True),
        ("credited analytic strata count", row_base + (e0, "analytic_internal_strata_added_to_integer_record_count"), True),
        ("credited residual credit", row_base + (e0, "guard_outside_or_residual_integer_credit"), 1),
        ("credited row digest", row_base + (e0, "row_sha256"), "0" * 64),
        ("mixed H graph kind", row_base + (m0, "outgoing_arrangement", "H_graph", "kind"), "NONUNIQUE"),
        ("mixed H graph dimension", row_base + (m0, "outgoing_arrangement", "H_graph", "dimension"), 3),
        ("mixed H derivative", row_base + (m0, "outgoing_arrangement", "H_graph", "strict_p_derivative_sign"), "UNRESOLVED"),
        ("mixed H owner", row_base + (m0, "outgoing_arrangement", "H_graph", "half_open_owner"), "N"),
        ("mixed H boundary credit", row_base + (m0, "outgoing_arrangement", "H_graph", "boundary_integer_credit"), 1),
        ("mixed Delta H status", row_base + (m0, "outgoing_arrangement", "Delta_intersect_H", "status"), "NONEMPTY"),
        ("mixed live witness owner", row_base + (m0, "strict_live_open_witness", "first_owner"), "G[1,0]"),
        ("mixed mismatch witness class", row_base + (m0, "strict_mismatch_open_witness", "classification"), "LIVE"),
        ("mixed fake exclusion", row_base + (m0, "classification"), "FULLY_EXCLUDED"),
        ("credit count", credit + ("new_whole_parent_exclusion_count",), 7),
        ("credit exact key", credit + ("exact_parent_keys", 0), "forged"),
        ("credit keys digest", credit + ("exact_parent_keys_sha256",), "0" * 64),
        ("all strata guard", credit + ("all_strata_mismatch_required",), False),
        ("physical interior guard", credit + ("all_six_strictly_inside_physical_source_chart",), False),
        ("2D graph credit", credit + ("credit_from_2D_graph_or_guard_slice",), 1),
        ("credited rows digest", credit + ("credited_parent_rows_sha256",), "0" * 64),
        ("residual count", residual + ("mixed_parent_count",), 15),
        ("residual key", residual + ("mixed_parent_keys", 0), "forged"),
        ("residual digest", residual + ("mixed_parent_keys_sha256",), "0" * 64),
        ("witness ledger guard", residual + ("all_have_strict_live_and_mismatch_open_witnesses",), False),
        ("analytic noncount guard", residual + ("analytic_strata_not_added_to_integer_record_count",), False),
        ("cross key", residual + ("source_chart_cross_seam_keys", 0), "forged"),
        ("cross key digest", residual + ("source_chart_cross_seam_keys_sha256",), "0" * 64),
        ("source seam equation", residual + ("source_chart_seam_equation",), "2*t^2<1"),
        ("guard band", residual + ("atlas_rational_guard_band",), "[-1,1]"),
        ("guard disposition", residual + ("guard_outside_is_chart_domain_rejection_not_exterior_exclusion",), False),
        ("guard ledger credit", residual + ("guard_outside_integer_exclusion_credit",), 2),
        ("diagonal owner rule", residual + ("physical_diagonal_half_open_owner_rule",), "N owns"),
        ("live H owner guard", residual + ("all_live_H_seams_half_open_owned_by_W",), False),
        ("prior exclusion", composition + ("Round172_whole_record_excluded",), 73178),
        ("new exclusion", composition + ("Round175_new_whole_parent_excluded",), 0),
        ("combined exclusion", composition + ("combined_whole_record_excluded",), 73172),
        ("credit disjointness", composition + ("new_credit_disjoint_from_Round172_credit",), False),
        ("prior live", composition + ("Round172_conservative_live",), 3654),
        ("new live", composition + ("Round175_conservative_live",), 3660),
        ("mixed live component", composition + ("live_components", "Round175_remaining_mixed_tangency_composites"), 22),
        ("conservation identity", composition + ("conservation_identity",), "73172+3660=76832"),
        ("refined total", composition + ("refined_total_unchanged",), False),
        ("Delta graph noncredit", noncredit + ("Delta_zero_graph_whole_parent_credit",), 1),
        ("H seam noncredit", noncredit + ("outgoing_H_zero_seam_whole_parent_credit",), 1),
        ("corner noncredit", noncredit + ("Delta_intersect_H_or_boundary_corner_integer_credit",), 1),
        ("guard noncredit", noncredit + ("source_chart_guard_outside_exterior_exclusion_credit",), 1),
        ("mixed strata noncredit", noncredit + ("sixteen_mixed_internal_mismatch_strata_whole_parent_credit",), 16),
        ("all physical strata scope", scope + ("every_integer_credit_requires_all_physical_strata_mismatch",), False),
        ("chart guard distinction", scope + ("physical_chart_seam_distinguished_from_rational_guard_band",), False),
        ("cross tube residual", scope + ("cross_seam_positive_volume_tubes_remain_residual",), False),
        ("D02 claim scope", scope + ("not_D02_closure",), False),
        ("D02 promotion", nonpromotion + ("D02",), "PASS"),
        ("CM2 promotion", nonpromotion + ("CM2",), "GO"),
        ("Gate5 promotion", nonpromotion + ("global_Gate5_fields",), "18/18"),
        ("producer pin field", prefix + ("provenance", "producer_sha256"), "0" * 64),
        ("dependency pin field", prefix + ("provenance", "dependency_sha256", OWNERSHIP), "0" * 64),
        ("precision provenance", prefix + ("provenance", "arb_context_precision_bits"), 191),
        ("upstream execution claim", prefix + ("provenance", "Round172_producer_or_verifier_imported_or_executed"), True),
        ("dyadic reconstruction claim", prefix + ("provenance", "parent_boxes_reconstructed_from_pinned_dyadic_paths"), False),
    ]
    attacks: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        (
            name,
            lambda d, path=path, value=value: set_path(d, path, value),
        )
        for name, path, value in specs
    ]
    for index in excluded_indices:
        key = rows[index]["ambient_leaf_key"]
        attacks.append((
            f"credited parent {key} fake mixed",
            lambda d, index=index: set_path(
                d,
                row_base + (index, "classification"),
                "MIXED_COMPOSITE",
            ),
        ))
    for index in mixed_indices:
        key = rows[index]["ambient_leaf_key"]
        attacks.append((
            f"mixed parent {key} fake excluded",
            lambda d, index=index: set_path(
                d,
                row_base + (index, "classification"),
                "FULLY_EXCLUDED",
            ),
        ))
        attacks.append((
            f"mixed parent {key} delete live open witness",
            lambda d, index=index: set_path(
                d,
                row_base + (index, "strict_live_open_witness"),
                None,
            ),
        ))
    attacks.extend([
        (
            "delete mismatch open witness",
            lambda d: set_path(
                d,
                row_base + (m0, "strict_mismatch_open_witness"),
                None,
            ),
        ),
        (
            "cross guard outside credited",
            lambda d: set_path(
                d,
                row_base + (
                    cross_index,
                    "source_chart_domain",
                    "guard_outside_exterior_exclusion_credit",
                ),
                1,
            ),
        ),
        (
            "cross source seam owner",
            lambda d: set_path(
                d,
                row_base + (
                    cross_index,
                    "source_chart_domain",
                    "source_chart_seam_half_open_owner",
                ),
                "N",
            ),
        ),
        (
            "exception terminal cell count",
            lambda d: set_path(
                d,
                row_base + (
                    exception_index,
                    "outgoing_arrangement",
                    "Delta_intersect_H",
                    "terminal_base_cell_count",
                ),
                17,
            ),
        ),
        (
            "exception graph order",
            lambda d: set_path(
                d,
                row_base + (
                    exception_index,
                    "outgoing_arrangement",
                    "Delta_intersect_H",
                    "all_terminal_base_cells",
                    0,
                    "strict_graph_order",
                ),
                "GRAPHS_INTERSECT",
            ),
        ),
        (
            "exception terminal cell deletion",
            lambda d: delete_path(
                d,
                row_base + (
                    exception_index,
                    "outgoing_arrangement",
                    "Delta_intersect_H",
                    "all_terminal_base_cells",
                    0,
                ),
            ),
        ),
        (
            "extra recursive key",
            lambda d: d["result"]["scope"].__setitem__("forged", True),
        ),
    ])
    rejected: list[str] = []
    for name, mutate in attacks:
        candidate = resigned(document, mutate)
        try:
            validate_certificate_document(candidate, expected_document)
        except Exception:
            rejected.append(name)
        else:
            raise VerificationError(f"semantic attack accepted:{name}")
    return {
        "attack_count": len(attacks),
        "rejected_count": len(rejected),
        "all_rejected": len(rejected) == len(attacks),
        "re_signed_result_digest_each_time": True,
        "rejected_attack_names": rejected,
    }


def strict_json_attacks() -> dict[str, Any]:
    good_result: dict[str, Any] = {}
    good_digest = digest(good_result)
    attacks = {
        "duplicate envelope key": (
            b'{"schema":"x","schema":"x","result":{},'
            + f'"result_sha256":"{good_digest}"'.encode()
            + b"}"
        ),
        "duplicate nested key": (
            b'{"schema":"x","result":{"a":1,"a":1},'
            b'"result_sha256":"0"}'
        ),
        "floating number": (
            b'{"schema":"x","result":{"a":1.0},"result_sha256":"0"}'
        ),
        "exponent number": (
            b'{"schema":"x","result":{"a":1e2},"result_sha256":"0"}'
        ),
        "NaN constant": (
            b'{"schema":"x","result":{"a":NaN},"result_sha256":"0"}'
        ),
        "UTF8 BOM": (
            b"\xef\xbb\xbf"
            + b'{"schema":"x","result":{},"result_sha256":"'
            + good_digest.encode()
            + b'"}'
        ),
        "raw NUL": b'{"schema":"x","result":{}\x00,"result_sha256":"0"}',
        "invalid UTF8": b"\xff",
        "noncanonical whitespace": (
            b'{ "schema":"x","result":{},"result_sha256":"'
            + good_digest.encode()
            + b'"}\n'
        ),
    }
    rejected: list[str] = []
    for name, raw in attacks.items():
        try:
            parse_envelope(
                raw,
                label=f"strict attack:{name}",
                require_canonical=True,
            )
        except Exception:
            rejected.append(name)
        else:
            raise VerificationError(f"strict JSON attack accepted:{name}")
    return {
        "attack_count": len(attacks),
        "rejected_count": len(rejected),
        "all_rejected": len(rejected) == len(attacks),
        "rejected_attack_names": rejected,
    }


def safe_atomic_write(
    path: Path,
    data: bytes,
    protected_paths: set[Path],
) -> None:
    path = Path(os.path.abspath(os.fspath(path)))
    require(path.parent.resolve() == HERE, "output directory")
    if path.exists() or path.is_symlink():
        st = path.lstat()
        require(stat.S_ISREG(st.st_mode), "output regular")
        require(not path.is_symlink(), "output symlink")
        require(st.st_nlink == 1, "output hardlink")
    require(
        path.resolve(strict=False) not in protected_paths,
        "protected output alias",
    )
    fd, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        directory_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if temporary.exists():
            temporary.unlink()


def expect_rejection(name: str, operation: Callable[[], Any]) -> str:
    try:
        operation()
    except Exception:
        return name
    raise VerificationError(f"path-safety attack accepted:{name}")


def path_safety_attacks(certificate_path: Path) -> dict[str, Any]:
    rejected: list[str] = []
    scratch = Path(
        tempfile.mkdtemp(prefix=".cm2_round175_path_attack.", dir=HERE)
    )
    symlink_output = HERE / f".cm2_round175_symlink_output.{os.getpid()}"
    hard_output_base = HERE / f".cm2_round175_hard_base.{os.getpid()}"
    hard_output_link = HERE / f".cm2_round175_hard_link.{os.getpid()}"
    outside = HERE.parent / f".cm2_round175_escape.{os.getpid()}"
    try:
        source = scratch / "source"
        source.write_bytes(b"{}\n")
        symlink_input = scratch / "symlink-input"
        symlink_input.symlink_to(source)
        rejected.append(expect_rejection(
            "symlink input",
            lambda: read_regular(symlink_input),
        ))
        hard_input = scratch / "hard-input"
        os.link(source, hard_input)
        rejected.append(expect_rejection(
            "hardlink input",
            lambda: read_regular(hard_input),
        ))
        oversized = scratch / "oversized"
        with oversized.open("wb") as handle:
            handle.truncate(MAX_INPUT_BYTES + 1)
        rejected.append(expect_rejection(
            "oversized sparse input",
            lambda: read_regular(oversized),
        ))
        protected = {
            certificate_path.resolve(),
            PRODUCER.resolve(),
            Path(__file__).resolve(),
        }
        symlink_output.symlink_to(source)
        rejected.append(expect_rejection(
            "symlink output",
            lambda: safe_atomic_write(symlink_output, b"x", protected),
        ))
        hard_output_base.write_bytes(b"x")
        os.link(hard_output_base, hard_output_link)
        rejected.append(expect_rejection(
            "hardlink output",
            lambda: safe_atomic_write(hard_output_link, b"x", protected),
        ))
        rejected.append(expect_rejection(
            "protected certificate output",
            lambda: safe_atomic_write(certificate_path, b"x", protected),
        ))
        rejected.append(expect_rejection(
            "parent directory escape",
            lambda: safe_atomic_write(outside, b"x", protected),
        ))
    finally:
        for path in (
            symlink_output,
            hard_output_link,
            hard_output_base,
            outside,
        ):
            if path.exists() or path.is_symlink():
                path.unlink()
        shutil.rmtree(scratch)
    return {
        "attack_count": 7,
        "rejected_count": len(rejected),
        "all_rejected": len(rejected) == 7,
        "rejected_attack_names": rejected,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    certificate_path = Path(os.path.abspath(os.fspath(arguments.certificate)))
    require(
        certificate_path.parent.resolve() == HERE,
        "certificate directory",
    )
    producer_data = read_regular(PRODUCER, EXPECTED_PRODUCER_SHA256)
    certificate_data = read_regular(
        certificate_path,
        EXPECTED_CERTIFICATE_SHA256,
    )
    document = parse_envelope(
        certificate_data,
        label=certificate_path.name,
        expected_schema=CERTIFICATE_SCHEMA,
        require_canonical=True,
    )
    expected_result, credited_audits = independently_reconstruct_result(
        sha256_bytes(producer_data)
    )
    expected_document = {
        "schema": CERTIFICATE_SCHEMA,
        "result": expected_result,
        "result_sha256": digest(expected_result),
    }
    validate_certificate_document(document, expected_document)
    semantic = semantic_attacks(document, expected_document)
    strict = strict_json_attacks()
    paths = path_safety_attacks(certificate_path)
    verifier_sha256 = sha256_bytes(Path(__file__).read_bytes())
    result = {
        "status": "PASS",
        "certificate_sha256": sha256_bytes(certificate_data),
        "certificate_result_sha256": document["result_sha256"],
        "producer_sha256": sha256_bytes(producer_data),
        "verifier_sha256": verifier_sha256,
        "independence_contract": {
            "Round175_producer_imported_or_executed": False,
            "source_W_parent_geometry_independently_replayed_at_192_bits":
                True,
            "all_22_Round172_parents_reconstructed_from_dyadic_paths": True,
            "all_22_Delta_H_and_physical_chart_arrangements_reconstructed":
                True,
            "all_six_credited_parents_complete_strata_reconstructed": True,
            "all_16_mixed_parents_have_replayed_live_and_mismatch_witnesses":
                True,
            "both_exception_graph_partitions_recomputed": True,
            "source_chart_seam_distinguished_from_rational_guard_band": True,
            "full_expected_result_independently_reconstructed": True,
            "full_expected_canonical_equality": True,
            "recursive_exact_key_tree_matched": True,
        },
        "recomputed_parent_census": {
            "input": 22,
            "fully_excluded": 6,
            "fully_live": 0,
            "mixed": 16,
            "owner_tangency": 20,
            "mismatch_tangency_exceptions": 2,
            "physical_source_chart_cross_seam": 2,
            "exception_terminal_base_cells_each": 18,
            "maximum_exception_extra_base_depth": 6,
        },
        "credited_parent_complete_strata_audit": {
            "credited_parent_count": len(credited_audits),
            "exact_parent_keys": [
                row["ambient_leaf_key"] for row in credited_audits
            ],
            "all_source_physical_interior": True,
            "all_Delta_negative_zero_positive_strata_accounted": True,
            "all_relevant_H_zero_strata_empty": True,
            "all_source_seam_and_guard_strata_empty": True,
            "all_physical_strata_mismatch": True,
            "audit_rows_sha256": digest(credited_audits),
            "audit_rows": credited_audits,
        },
        "ledger_reconstruction": {
            "Round172_whole_record_excluded": 73172,
            "Round175_new_whole_parent_excluded": 6,
            "combined_whole_record_excluded": 73178,
            "Round172_conservative_live": 3660,
            "Round175_conservative_live": 3654,
            "refined_source_W_record_count": 76832,
            "conservation_identity": "73178+3654=76832",
            "exact_six_parent_keys_matched": True,
            "new_credit_disjoint_from_Round172": True,
        },
        "semantic_mutation_attack_suite": semantic,
        "strict_json_attack_suite": strict,
        "path_safety_attack_suite": paths,
        "strict_nonpromotion": {
            "D02": "BLOCKED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    envelope = {
        "schema": VERIFICATION_SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    protected = {
        PRODUCER.resolve(),
        certificate_path.resolve(),
        Path(__file__).resolve(),
        *((HERE / name).resolve() for name in PINS),
    }
    safe_atomic_write(
        arguments.output,
        canonical_bytes(envelope) + b"\n",
        protected,
    )
    print(envelope["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
