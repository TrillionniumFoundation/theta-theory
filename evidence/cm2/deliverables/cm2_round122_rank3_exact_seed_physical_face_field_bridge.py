#!/usr/bin/env python3
"""Round122: physical-face and artificial-recut-face fields on the Round121 seed.

Round121 materialized twenty-four common-refinement children of one exact-b
grazing parent-W seed and installed child-local F1--F6.  This producer keeps
that seed and every frozen Round121 ID unchanged, opens the deliberately tiny
parameter collar ``|s| <= 2^-512``, and pays two different face interfaces:

* the complete physical five-face/seven-boundary grammar is interval-replayed
  on all 24 children and all three collision legs and has no incidence; and
* the two stationary outer source faces plus the 23 actual pullback recut
  faces are retained as parameterized artificial faces.  The moving cuts are
  the implicit analytic graphs ``U_i(x,s)=j*10^-90`` and are never erased by
  the physical-face empty statement.

The second interface supplies F8/F9/F12.  The first supplies the zero-valued
F10/F13/F16 slots.  F7 is the actual density-weighted Round32 field value,
not the bare Xi subfactor.  F11 uses the authoritative full-phase envelopes,
not the much smaller along-seed diagnostic derivatives.

The result is child-local F1--F13 plus F16, namely 14/18, on this one exact
seed only.  Global Gate5 remains 10/18 and CM2 remains NO-GO_FOR_CLAIM.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_round26_q1_time2_frontier_cert as time2
import cm2_round112_rank3_double_grazing_two_sided_root_sheet as round112
import cm2_round121_rank3_exact_seed_three_leg_recut_f5f6 as r121
from cm2_round76_r2_numeric_fields_generator import Jet, aq, center, interval, normal


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "cm2-round122-rank3-exact-seed-physical-face-field-bridge-2026-07-23.json"
SCHEMA = "cm2.round122.rank3-exact-seed-physical-face-field-bridge.v1"
PRECISION_BITS = 2048

ROUND121 = HERE / "cm2-round121-rank3-exact-seed-three-leg-recut-f5f6-2026-07-23.json"
ROUND121_PRODUCER = HERE / "cm2_round121_rank3_exact_seed_three_leg_recut_f5f6.py"
ROUND121_VERIFIER = HERE / "cm2_round121_rank3_exact_seed_three_leg_recut_f5f6_verifier.py"
ROUND121_VERIFICATION = HERE / "cm2-round121-rank3-exact-seed-three-leg-recut-f5f6-verification-2026-07-23.json"
ROUND121_MANIFEST = HERE / "cm2-one-hundred-twenty-first-direct-assault-manifest-2026-07-23.sha256"

PINS = {
    ROUND121.name: "ba56b41a41fbf0d77c6467fcb5fc521ef4d6928f65a9f79d5bba8b83c9b4fc6e",
    ROUND121_PRODUCER.name: "30c69e1849867841398483749f547a7840d401bc3cc24b9e4ef0a4892ad990ed",
    ROUND121_VERIFIER.name: "d35c0e04b9d339c1271533abdefa5addcb73096b70abdec94d60e475daa45e95",
    ROUND121_VERIFICATION.name: "ec527c19a8c50025514db0769808ce21aeb53c7d1cc64edb75f1a9c5a6aa3e80",
    ROUND121_MANIFEST.name: "e53ad73d4e7120c2ce4f30c49f83f29d4d2b99a5f8a451f9085e5fb473959b83",
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json":
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866",
    "cm2-gate45-global-invariant-cone-manifest-2026-07-16.json":
        "173949cb9cde01ae1326576c2a9a48b268a80bce2e48954a49efa46ccd9759f9",
    "cm2-gate4-componentwise-global-growth-recovery-frontier-manifest-2026-07-16.json":
        "34ff376dafa9f95f7b03df661655240657b114ffc4e1bc20fca036c84f1dd691",
    "cm2-gate45-round32-actual-instance-f7-join-manifest-2026-07-19.json":
        "81e59b1ca2ff8b2aeac1c2eba36592e0e788618a33ef97c7a7d65faa94c2c310",
    "cm2-gate5-round32-parameterized-face-rank-f8-manifest-2026-07-19.json":
        "f9c4eca78065001e65381880deef8681b3a626c2bd419e4ecfe3b02f37a7b53e",
    "cm2-gate5-round36-all-face-rank-path-f9-manifest-2026-07-19.json":
        "f603dd8e638d661b22c746742a5e5c3fd48242f4c0ad40bb35fbe74d35325788",
    "cm2-gate5-round40-arbitrary-rn-f10-parameter-jet-frontier-manifest-2026-07-19.json":
        "b5e1a965bb7fa1fc0f18ff6eb441c0bb181ac61d70451ce2eb67ea9d00c5695e",
    "cm2-gate5-round41-physical-parameter-jet-envelopes-manifest-2026-07-19.json":
        "dd19fd73a01c3aa9868fb9e3c89a039a5e8c97d807b6f57048fddc35c744c2cc",
    "cm2-gate5-round27-r1-empty-physical-face-join-manifest-2026-07-18.json":
        "9d900f2d0fee5ab8ad1a7e1f999e640ef88edc928ba6208987d1a74c93ca0e38",
    "cm2-gate5-round45-all-face-suffix-f12-frontier-manifest-2026-07-19.json":
        "7260c3162ba66c634a9583ebfe04d6345dd946fedd40e19b9de244b47fd603be",
    "cm2-gate5-round44-all-face-suffix-two-trace-f13-manifest-2026-07-19.json":
        "3cf6635532622427bcde0525205212e1970b92ee56b2eb290ed01c1984443a9d",
    "cm2-gate5-round46-piola-f16-frontier-manifest-2026-07-19.json":
        "ee4a4fd441ff5b63e5607bcd367b04c336a49173d3e7be8ca4b5e1181d3e5a49",
    "cm2-gate34-round47-postcut-dyadic-recovery-manifest-2026-07-19.json":
        "79eeff7d5c18ec7d28a30c61ae857a733b3136202917c54f6aeaf93d7f414089",
    "cm2-gate34-round50-physical-whole-family-grouping-manifest-2026-07-19.json":
        "79032e73e9b8d89fd3ecb8e60ac6b1899093e5cc35c8889a62ac47e168a90b73",
    "cm2-gate5-round28-limiting-physical-face-atlas-frontier-manifest-2026-07-18.json":
        "ad385983a4152da3bc1d9c58a5a2fba1abb928466ecf9a9f61260b612bddf140",
    "cm2-gate5-round48-seven-boundary-f10-seed-frontier-manifest-2026-07-19.json":
        "d2eb549656098abfc3fd57ae3eb5796e4ec3d57ebf579b21497ee3721ee3116c",
}

EPSILON = Q(1, 2**512)
DELTA = Q(1, 10**90)
XI = Q(900337, 901685)
DENSITY_RATIO = Q(2000, 1999)
F7_VALUE = Q(360134800, 360493663)
F8_LOWER = Q(1, 6)
F9_STAGE1 = Q(80253367137726629098291200)
F9_STAGE2 = Q(310359909615573026525432020225398669312000000)
F12_STAGE1 = Q(6039797760001)
F12_STAGE2 = Q(2457601)
F12_OUTER = Q(29686813949952000001)
F11_BY_STAGE = {0: Q(4915200), 1: Q(2457600), 2: Q(2457600)}

NEW_FIELDS = (
    (7, "one_step_cut_growth_Z_sum"),
    (8, "face_transversality_lower"),
    (9, "face_C2_atlas_bound"),
    (10, "coarea_density_regular_bound"),
    (11, "dynamic_Holder_test_pullback_bound"),
    (12, "C1_face_trace_pullback_bound"),
    (13, "moving_boundary_DQ_current_and_two_traces"),
    (16, "flux_face_operator_cost"),
)

STAGE_CURRENT = ("G[0,0]", "W[-1,-1]", "G[0,0]")
STAGE_CHART = ("W", "N", "S")
STAGE_SELECTED = ("W[-1,-1]", "G[0,0]", "G[-1,-2]")
COLLISION_CHARTS = ("W", "N", "S", "N")
COLLISION_OBSTACLES = ("G", "W", "G", "G")

SAFE_PHYSICAL_MARGINS = {
    "candidate_tangency": Q(1, 10**12),
    "coordinate_velocity_zero": Q(1, 10),
    "core_face": Q(1, 3),
    "integer_corner_ray": Q(1, 20),
    "owner_gap": Q(9, 10),
    "root_sign": Q(1, 10),
    "source_chart_seam": Q(1, 10),
    "source_endpoint_wall": Q(1, 25),
    "source_homogeneity": Q(1, 10**14),
    "target_chart_seam": Q(1, 25),
    "target_endpoint_wall": Q(1, 5),
    "target_homogeneity": Q(4, 5),
}

EXPECTED_PHYSICAL_COUNTS = {
    "candidate_tangency": 4056,
    "coordinate_velocity_zero": 144,
    "core_face": 1152,
    "integer_corner_ray": 2040,
    "owner_gap": 144,
    "root_sign": 384,
    "source_chart_seam": 72,
    "source_endpoint_wall": 72,
    "source_homogeneity": 72,
    "target_chart_seam": 72,
    "target_endpoint_wall": 72,
    "target_homogeneity": 72,
}


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qstr(value: Q | int) -> str:
    return str(Q(value))


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        require(key not in value, f"duplicate JSON key: {key}")
        value[key] = item
    return value


def strict_json(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_pairs,
        parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
        parse_float=lambda token: (_ for _ in ()).throw(ValueError(f"float forbidden: {token}")),
    )
    require(type(value) is dict, f"top-level object: {path.name}")
    return value


def load_round121() -> dict[str, Any]:
    for name, expected in PINS.items():
        require(sha256(HERE / name) == expected, f"pin mismatch: {name}")
    document = strict_json(ROUND121)
    require(set(document) == {"schema", "result", "result_sha256"}, "Round121 closed envelope")
    require(document["schema"] == r121.SCHEMA, "Round121 schema")
    require(document["result_sha256"] == digest(document["result"]), "Round121 result digest")
    result = document["result"]
    require(result["rank3_seed_child_field_maturity"] == "6/18", "Round121 maturity")
    require(result["gate5_global_maturity"] == "10/18", "Round121 global maturity")
    require(result["complete_18_field_block_count"] == 0, "Round121 complete blocks")
    require(result["cm2_verdict"] == "NO-GO_FOR_CLAIM", "Round121 CM2")
    require(result["count_ledger"]["common_refinement_actual_child_count"] == 24, "Round121 children")
    require(result["count_ledger"]["pullback_internal_cut_count"] == 23, "Round121 cuts")
    require(result["count_ledger"]["F1_F6_total_slot_count"] == 720, "Round121 slots")
    require(result["gate5_F1_F6_slot_rows_sha256"] == digest(result["gate5_F1_F6_slot_rows"]), "Round121 slot digest")
    require(result["pullback_endpoint_rows_sha256"] == digest(result["pullback_endpoint_rows"]), "Round121 endpoint digest")
    require(result["common_refinement_rows_sha256"] == digest(result["common_refinement_rows"]), "Round121 child digest")

    schema = strict_json(HERE / "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json")
    fields = schema["result"]["required_operator_field_schema"]["required_fields"]
    require(len(fields) == 18, "Gate5 field count")
    for index, field in NEW_FIELDS:
        require(fields[index - 1] == field, f"Gate5 F{index} name")

    cone = strict_json(HERE / "cm2-gate45-global-invariant-cone-manifest-2026-07-16.json")
    cone_row = cone["result"]["global_invariant_geometric_cone"]
    require(cone_row["fixed_geometric_unstable_cone"] == "25/9<V=dphi/dr<4108425/145348<29", "cone")
    require(cone_row["strict_forward_invariance"] is True, "cone invariance")

    gate4 = strict_json(HERE / "cm2-gate4-componentwise-global-growth-recovery-frontier-manifest-2026-07-16.json")
    require(gate4["replay_summary"]["global_one_step_Xi_strict_upper"] == qstr(XI), "Xi")
    f7 = strict_json(HERE / "cm2-gate45-round32-actual-instance-f7-join-manifest-2026-07-19.json")
    f7_text = canonical(f7)
    require(qstr(XI) in f7_text and qstr(DENSITY_RATIO) in f7_text, "F7 factors")
    require(qstr(F7_VALUE) in f7_text, "actual F7 value")
    require(DENSITY_RATIO * XI == F7_VALUE and F7_VALUE < 1, "F7 arithmetic")
    return result


def lohi(value: arb) -> tuple[Q, Q]:
    return r121.arb_pair(value)


def abs_lower(value: arb) -> Q:
    lower, upper = lohi(value)
    if lower > 0:
        return lower
    if upper < 0:
        return -upper
    return Q(0)


def abs_upper(value: arb) -> Q:
    lower, upper = lohi(value)
    return max(abs(lower), abs(upper))


def positive_lower(value: arb) -> Q:
    return lohi(value)[0]


def negative_margin(value: arb) -> Q:
    return -lohi(value)[1]


def interval_strings(value: arb) -> list[str]:
    lower, upper = lohi(value)
    return [qstr(lower), qstr(upper)]


def dist_interval(value: arb, lower: Q, upper: Q) -> Q:
    lo, hi = lohi(value)
    if hi < lower:
        return lower - hi
    if lo > upper:
        return lo - upper
    return Q(0)


def distance_to_core_face(t: arb, p: arb, core: object, face: str) -> Q:
    if face == "t0":
        return max(abs_lower(t - aq(core.t0)), dist_interval(p, core.p0, core.p1))
    if face == "t1":
        return max(abs_lower(t - aq(core.t1)), dist_interval(p, core.p0, core.p1))
    if face == "p0":
        return max(abs_lower(p - aq(core.p0)), dist_interval(t, core.t0, core.t1))
    if face == "p1":
        return max(abs_lower(p - aq(core.p1)), dist_interval(t, core.t0, core.t1))
    raise RuntimeError(f"unknown core face: {face}")


def chart_coordinate(chart: str, nx: Jet, ny: Jet) -> Jet:
    return ny if chart in ("E", "W") else nx


def chart_margin(nx: Jet, ny: Jet) -> Q:
    return abs_lower(abs(nx.value) - abs(ny.value))


def nearest_integer_margin(value: arb) -> Q:
    return min(abs_lower(value - arb(k)) for k in range(-7, 8))


def adapted_angle(chart: str, nx: Jet, ny: Jet, p: Jet) -> Jet:
    if chart == "E":
        theta = r121.asin_jet(ny)
    elif chart == "N":
        theta = Jet(arb.pi() / 2) - r121.asin_jet(nx)
    elif chart == "W":
        theta = Jet(arb.pi()) - r121.asin_jet(ny)
    elif chart == "S":
        theta = -Jet(arb.pi() / 2) + r121.asin_jet(nx)
    else:
        raise RuntimeError(f"chart: {chart}")
    return theta + r121.asin_jet(p)


def moving_geometry(
    seed: dict[str, Any],
    root_bracket: tuple[Q, Q],
    x_lower: Q,
    x_upper: Q,
) -> dict[str, Any]:
    t_star = interval(*root_bracket)
    theta_star = arb.pi() - t_star.asin()
    phi_star = aq(r121.ANCHOR_C0).acos()
    x = Jet.variable(interval(x_lower, x_upper), 0)
    s = Jet.variable(interval(-EPSILON, EPSILON), 2)
    theta0 = Jet(theta_star) + aq(r121.SOURCE_THETA_COEFFICIENT * DELTA) * x
    phi0 = Jet(phi_star) + aq(r121.SOURCE_PHI_COEFFICIENT * DELTA) * x
    t0 = r121.sin_jet(theta0)
    c0 = r121.cos_jet(phi0)
    n0x, n0y = normal("W", t0)
    p0 = r121.sin_jet(phi0)
    u0x = c0 * n0x - p0 * n0y
    u0y = c0 * n0y + p0 * n0x
    sx, sy = center("G[0,0]", s)
    q0x, q0y = sx + aq(Q(9, 25)) * n0x, sy + aq(Q(9, 25)) * n0y

    c1x, c1y = center("W[-1,-1]", s)
    first = round112.collision_diagnostic(q0x, q0y, u0x, u0y, c1x, c1y, Q(4, 25))
    cp1 = (arb(1) - first["momentum"] * first["momentum"]).sqrt()
    u1x = cp1 * first["normal_x"] - first["momentum"] * first["normal_y"]
    u1y = cp1 * first["normal_y"] + first["momentum"] * first["normal_x"]

    c2x, c2y = center("G[0,0]", s)
    second = round112.collision_diagnostic(
        first["hit_x"], first["hit_y"], u1x, u1y, c2x, c2y, Q(9, 25),
    )
    cp2 = (arb(1) - second["momentum"] * second["momentum"]).sqrt()
    u2x = cp2 * second["normal_x"] - second["momentum"] * second["normal_y"]
    u2y = cp2 * second["normal_y"] + second["momentum"] * second["normal_x"]

    c3x, c3y = center("G[-1,-2]", s)
    third = round112.collision_diagnostic(
        second["hit_x"], second["hit_y"], u2x, u2y, c3x, c3y, Q(9, 25),
    )
    cp3 = (arb(1) - third["momentum"] * third["momentum"]).sqrt()

    states = (
        (q0x, q0y, u0x, u0y),
        (first["hit_x"], first["hit_y"], u1x, u1y),
        (second["hit_x"], second["hit_y"], u2x, u2y),
    )
    collisions = (
        (n0x, n0y, p0, c0),
        (first["normal_x"], first["normal_y"], first["momentum"], cp1),
        (second["normal_x"], second["normal_y"], second["momentum"], cp2),
        (third["normal_x"], third["normal_y"], third["momentum"], cp3),
    )
    adapted = (
        adapted_angle("W", n0x, n0y, p0),
        adapted_angle("N", first["normal_x"], first["normal_y"], first["momentum"]),
        adapted_angle("S", second["normal_x"], second["normal_y"], second["momentum"]),
        adapted_angle("N", third["normal_x"], third["normal_y"], third["momentum"]),
    )
    return {
        "x": x,
        "s": s,
        "states": states,
        "collisions": collisions,
        "adapted": adapted,
        "selected": (first, second, third),
    }


def candidate(
    state: tuple[Jet, Jet, Jet, Jet],
    candidate_id: str,
    parameter: Jet,
) -> dict[str, Any]:
    qx, qy, ux, uy = state
    ax, ay = center(candidate_id, parameter)
    dx, dy = ax - qx, ay - qy
    longitudinal = ux * dx + uy * dy
    transverse = -uy * dx + ux * dy
    radius = aq(round112.radius(candidate_id))
    discriminant = radius * radius - transverse * transverse
    result: dict[str, Any] = {
        "id": candidate_id,
        "longitudinal": longitudinal,
        "transverse": transverse,
        "discriminant": discriminant,
    }
    if negative_margin(discriminant.value) > 0:
        result["kind"] = "MISS"
        return result
    require(positive_lower(discriminant.value) > 0, f"unresolved discriminant: {candidate_id}")
    radical = discriminant.sqrt()
    near, far = longitudinal - radical, longitudinal + radical
    result.update({"near": near, "far": far})
    if negative_margin(far.value) > 0:
        result["kind"] = "BEHIND"
    elif positive_lower(near.value) > 0:
        result["kind"] = "FUTURE"
    else:
        raise RuntimeError(f"unresolved root: {candidate_id}")
    return result


def common_child_intervals(round121: dict[str, Any]) -> list[tuple[dict[str, Any], Q, Q]]:
    endpoints = {
        row["endpoint_id"]: tuple(map(Q, row["x_dyadic_bracket"]))
        for row in round121["pullback_endpoint_rows"]
    }
    rows: list[tuple[dict[str, Any], Q, Q]] = []
    for child in round121["common_refinement_rows"]:
        lower_id = child["source_x_lower_endpoint_id"]
        upper_id = child["source_x_upper_endpoint_id"]
        lower = Q(0) if "source-left-endpoint" in lower_id else endpoints[lower_id][0]
        upper = Q(1) if "source-right-endpoint" in upper_id else endpoints[upper_id][1]
        rows.append((child, lower, upper))
    rows.sort(key=lambda item: item[0]["common_rank"])
    require([item[0]["common_rank"] for item in rows] == list(range(24)), "common ranks")
    return rows


def physical_empty_audit(
    seed: dict[str, Any],
    root_bracket: tuple[Q, Q],
    round121: dict[str, Any],
) -> dict[str, Any]:
    h128 = aq(Q(1, 128**2)).sin()
    cores = core_cert.physical_cores()
    counts = {key: 0 for key in SAFE_PHYSICAL_MARGINS}
    actual_minima: dict[str, Q | None] = {key: None for key in SAFE_PHYSICAL_MARGINS}
    core_rows: list[dict[str, Any]] = []
    child_stage_rows: list[dict[str, Any]] = []
    along_curve_upper = [Q(0), Q(0), Q(0)]

    def observe(local: dict[str, list[Q]], key: str, value: Q) -> None:
        require(value > SAFE_PHYSICAL_MARGINS[key], f"{key} safe margin")
        counts[key] += 1
        local.setdefault(key, []).append(value)
        previous = actual_minima[key]
        if previous is None or value < previous:
            actual_minima[key] = value

    for child, x_lower, x_upper in common_child_intervals(round121):
        geometry = moving_geometry(seed, root_bracket, x_lower, x_upper)
        local_core: dict[str, list[Q]] = {}
        for section, ((nx, ny, p, _cp), chart, obstacle) in enumerate(
            zip(geometry["collisions"], COLLISION_CHARTS, COLLISION_OBSTACLES),
        ):
            t = chart_coordinate(chart, nx, ny).value
            section_values: list[Q] = []
            section_count = 0
            for core in cores:
                if core.chart_id != f"{obstacle}:{chart}":
                    continue
                for face in ("t0", "t1", "p0", "p1"):
                    value = distance_to_core_face(t, p.value, core, face)
                    observe(local_core, "core_face", value)
                    section_values.append(value)
                    section_count += 1
            require(section_count == 12, "twelve typed C24 core faces per section")
            role = "source_core_clipping_face"
            if section in (1, 2):
                role = "intermediate_core_avoidance_preimage_face"
            elif section == 3:
                role = "terminal_core_preimage_face"
            core_row = {
                "common_child_id": child["common_child_id"],
                "common_rank": child["common_rank"],
                "collision_section": section,
                "physical_face_grammar_kind": role,
                "obstacle": obstacle,
                "chart": chart,
                "typed_C24_core_face_check_count": section_count,
                "distance_strict_lower": qstr(SAFE_PHYSICAL_MARGINS["core_face"]),
                "actual_interval_lower_minimum": qstr(min(section_values)),
                "incidence_count": 0,
            }
            core_row["row_sha256"] = digest(core_row)
            core_rows.append(core_row)

        adapted_derivatives = [row.gradient[0] for row in geometry["adapted"]]
        for stage in range(3):
            local: dict[str, list[Q]] = {}
            source_state = geometry["states"][stage]
            qx, qy, ux, uy = source_state
            nx, ny, _p, cp = geometry["collisions"][stage]
            next_nx, next_ny, _next_p, next_cp = geometry["collisions"][stage + 1]
            observe(local, "source_endpoint_wall", min(
                nearest_integer_margin(qx.value), nearest_integer_margin(qy.value),
            ))
            observe(local, "source_chart_seam", chart_margin(nx, ny))
            observe(local, "source_homogeneity", positive_lower(cp.value - h128))
            observe(local, "coordinate_velocity_zero", abs_lower(ux.value))
            observe(local, "coordinate_velocity_zero", abs_lower(uy.value))

            table: list[dict[str, Any]] = []
            for candidate_id in time2.translated_candidate_ids(
                STAGE_CURRENT[stage], STAGE_CHART[stage],
            ):
                row = candidate(source_state, candidate_id, geometry["s"])
                table.append(row)
                observe(local, "candidate_tangency", abs_lower(row["discriminant"].value))
                if row["kind"] == "BEHIND":
                    observe(local, "root_sign", negative_margin(row["far"].value))
                elif row["kind"] == "FUTURE":
                    observe(local, "root_sign", positive_lower(row["near"].value))

            selected = next(row for row in table if row["id"] == STAGE_SELECTED[stage])
            require(selected["kind"] == "FUTURE", "selected owner future")
            for row in table:
                if row["kind"] == "FUTURE" and row["id"] != selected["id"]:
                    observe(local, "owner_gap", positive_lower(
                        row["near"].value - selected["near"].value,
                    ))

            selected_diagnostic = geometry["selected"][stage]
            observe(local, "target_endpoint_wall", min(
                nearest_integer_margin(selected_diagnostic["hit_x"].value),
                nearest_integer_margin(selected_diagnostic["hit_y"].value),
            ))
            observe(local, "target_chart_seam", chart_margin(next_nx, next_ny))
            observe(local, "target_homogeneity", positive_lower(next_cp.value - h128))

            _source, ix, iy = time2.parse_target(STAGE_CURRENT[stage])
            corner_count = 0
            for corner_x in range(ix - 5, ix + 6):
                for corner_y in range(iy - 5, iy + 6):
                    dx, dy = arb(corner_x) - qx.value, arb(corner_y) - qy.value
                    longitudinal = ux.value * dx + uy.value * dy
                    low, high = lohi(longitudinal)
                    if high <= Q(1, 2) or low >= Q(3):
                        continue
                    transverse = -uy.value * dx + ux.value * dy
                    observe(local, "integer_corner_ray", abs_lower(transverse))
                    corner_count += 1

            denominator_lower = abs_lower(adapted_derivatives[stage])
            require(denominator_lower > 0, "adapted input derivative")
            along_upper = abs_upper(adapted_derivatives[stage + 1]) / denominator_lower
            direct_bound = (Q(7), Q(3), Q(12))[stage]
            require(along_upper < direct_bound, f"along-seed derivative stage {stage}")
            along_curve_upper[stage] = max(along_curve_upper[stage], along_upper)

            row = {
                "common_child_id": child["common_child_id"],
                "common_rank": child["common_rank"],
                "stage": stage,
                "source_owner": STAGE_CURRENT[stage],
                "actual_next_owner": STAGE_SELECTED[stage],
                "source_chart": STAGE_CHART[stage],
                "s_collar": f"|s|<={qstr(EPSILON)}",
                "candidate_check_count": len(table),
                "active_integer_corner_ray_check_count": corner_count,
                "typed_boundary_check_counts": {
                    key: len(values) for key, values in sorted(local.items())
                },
                "typed_boundary_actual_interval_lower_minima": {
                    key: qstr(min(values)) for key, values in sorted(local.items())
                },
                "typed_boundary_claimed_strict_lower": {
                    key: qstr(SAFE_PHYSICAL_MARGINS[key]) for key in sorted(local)
                },
                "physical_boundary_incidence_count": 0,
                "BYPASS_designated_b3_used_as_collision_angle": False,
                "along_seed_adapted_forward_Lipschitz_actual_upper": qstr(along_upper),
                "along_seed_diagnostic_only_not_F11_field_value": True,
            }
            row["row_sha256"] = digest(row)
            child_stage_rows.append(row)

    require(counts == EXPECTED_PHYSICAL_COUNTS, "physical audit census")
    require(len(core_rows) == 96, "core rows")
    require(len(child_stage_rows) == 72, "child-stage rows")
    for common_rank in range(24):
        rank_rows = [
            row for row in child_stage_rows if row["common_rank"] == common_rank
        ]
        require(len(rank_rows) == 3, "three stage rows per common child")
        require(
            [row["candidate_check_count"] for row in rank_rows] == [57, 55, 57],
            "rank-3 complete 169-candidate stage census",
        )
        require(
            sum(row["candidate_check_count"] for row in rank_rows) == 169,
            "rank-3 complete 169-candidate census",
        )
    require(all(value is not None for value in actual_minima.values()), "all physical minima")
    return {
        "core_clearance_rows": core_rows,
        "core_clearance_rows_sha256": digest(core_rows),
        "child_stage_boundary_rows": child_stage_rows,
        "child_stage_boundary_rows_sha256": digest(child_stage_rows),
        "check_counts": counts,
        "actual_interval_lower_minima": {
            key: qstr(value) for key, value in sorted(actual_minima.items()) if value is not None
        },
        "claimed_strict_lower_margins": {
            key: qstr(value) for key, value in sorted(SAFE_PHYSICAL_MARGINS.items())
        },
        "along_seed_adapted_forward_Lipschitz_actual_upper": [
            qstr(value) for value in along_curve_upper
        ],
        "legacy_parameterized_moving_occurrence_grammar_seed_count": 64,
        "rank3_candidate_occurrence_count_per_common_child": 169,
        "rank3_candidate_occurrence_stage_counts": [57, 55, 57],
        "rank3_candidate_occurrence_total_check_count": 4056,
        "complete_new_rank3_candidate_census_replaces_old_Q2_locator": True,
        "old_Q2_time2_atom_or_occurrence_ID_reused": False,
        "physical_five_face_incidence_count": 0,
        "residual_physical_face_count": 0,
    }


def fix_x(value: Jet) -> Jet:
    gradient = list(value.gradient)
    hessian = [list(row) for row in value.hessian]
    gradient[0] = arb(0)
    for index in range(3):
        hessian[0][index] = arb(0)
        hessian[index][0] = arb(0)
    return Jet(value.value, gradient, hessian)


def recut_equation(
    seed: dict[str, Any],
    root_bracket: tuple[Q, Q],
    stage: int,
    natural_index: int,
    x_lower: Q,
    x_upper: Q,
) -> tuple[Jet, dict[str, Any]]:
    base = moving_geometry(seed, root_bracket, Q(0), Q(0))
    current = moving_geometry(seed, root_bracket, x_lower, x_upper)
    if stage == 1:
        equation = (
            fix_x(base["adapted"][1])
            - current["adapted"][1]
            - aq(natural_index * DELTA)
        )
    else:
        require(stage == 2, "moving recut stage")
        equation = (
            current["adapted"][2]
            - fix_x(base["adapted"][2])
            - aq(natural_index * DELTA)
        )
    return equation, current


def trace_id(face_id: str, side: str) -> str:
    require(side in {"lower", "upper"}, "trace side")
    return "round122-recut-face-trace:" + digest(
        ["round122-recut-face-trace-v1", face_id, side],
    )


def moving_recut_faces(
    seed: dict[str, Any],
    root_bracket: tuple[Q, Q],
    round121: dict[str, Any],
) -> list[dict[str, Any]]:
    exact_seed_id = round121["exact_seed_contract"]["exact_parent_W_seed_id"]
    rows: list[dict[str, Any]] = []
    require(
        36 * (Q(25, 4) + 29) ** 2
        - (1 + Q(25, 4) ** 2) * (1 + Q(29) ** 2)
        == Q(87997, 8),
        "F8 worst-case squared residual",
    )
    for endpoint in round121["pullback_endpoint_rows"]:
        stage = endpoint["stage"]
        natural_index = endpoint["natural_index_j"]
        x_lower, x_upper = map(Q, endpoint["x_dyadic_bracket"])
        equation, _current = recut_equation(
            seed, root_bracket, stage, natural_index, x_lower, x_upper,
        )
        left, _ = recut_equation(
            seed, root_bracket, stage, natural_index, x_lower, x_lower,
        )
        right, _ = recut_equation(
            seed, root_bracket, stage, natural_index, x_upper, x_upper,
        )
        require(lohi(left.value)[1] < 0 < lohi(right.value)[0], "collar root face signs")
        fx, fs = equation.gradient[0], equation.gradient[2]
        fxx = equation.hessian[0][0]
        fxs = equation.hessian[0][2]
        fss = equation.hessian[2][2]
        fx_lower = abs_lower(fx)
        claimed_fx = (Q(5), Q(16))[stage - 1] * DELTA
        require(fx_lower > claimed_fx, "moving recut Fx")
        x_prime = -fs / fx
        x_second = -(fss + 2 * fxs * x_prime + fxx * x_prime * x_prime) / fx
        x_prime_claim = (Q(4), Q(13))[stage - 1]
        x_second_claim = (Q(56), Q(616))[stage - 1]
        require(abs_upper(x_prime) < x_prime_claim, "moving recut x prime")
        require(abs_upper(x_second) < x_second_claim, "moving recut x second")
        require(x_prime_claim * EPSILON < Q(1, 2**201), "moving recut remains in bracket")
        require(2 * x_prime_claim * EPSILON < Q(1, 1000), "moving cut order shift")

        s0_equation, _ = recut_equation(
            seed, root_bracket, stage, natural_index, x_lower, x_upper,
        )
        # The same routine has the full collar in its s variable.  Its Fx
        # lower is therefore also a valid (slightly weaker) s=0 lower.
        s0_fx_lower = abs_lower(s0_equation.gradient[0])
        base_curvature = Q(25, 4) if stage == 1 else Q(25, 9)
        f9 = F9_STAGE1 if stage == 1 else F9_STAGE2
        f12 = F12_STAGE1 if stage == 1 else F12_STAGE2
        pullback_path = [15] if stage == 1 else [15, 14]
        suffix_path = [14, 14] if stage == 1 else [14]
        face_payload = [
            "round122-parameterized-recut-face-v1",
            exact_seed_id,
            stage,
            natural_index,
            endpoint["exact_root_equation_id"],
        ]
        face_id = "round122-parameterized-recut-face:" + digest(face_payload)
        row = {
            "face_id": face_id,
            "face_kind": "PARAMETERIZED_ARTIFICIAL_PULLBACK_RECUT",
            "exact_seed_id": exact_seed_id,
            "stage": stage,
            "natural_index_j": natural_index,
            "boundary_label": f"U{stage}={natural_index}*delta",
            "exact_level_equation_id": endpoint["exact_root_equation_id"],
            "exact_level_equation": f"U{stage}(x,s)={natural_index}*10^-90",
            "delta": "1e-90",
            "s_collar": f"|s|<={qstr(EPSILON)}",
            "round121_s0_endpoint_id": endpoint["endpoint_id"],
            "s0_x_dyadic_bracket": endpoint["x_dyadic_bracket"],
            "equation_decimal_participates_in_id": False,
            "base_image_chart": ("N", "S")[stage - 1],
            "base_image_obstacle": ("W", "G")[stage - 1],
            "base_curvature": qstr(base_curvature),
            "source_pullback_rank_path": pullback_path,
            "owner_below": endpoint["lower_owner"],
            "owner_above": endpoint["upper_owner"],
            "lower_trace_id": trace_id(face_id, "lower"),
            "upper_trace_id": trace_id(face_id, "upper"),
            "F_x_sign": 1,
            "F_x_s0_abs_lower": qstr(s0_fx_lower),
            "F_x_collar_abs_lower": qstr(fx_lower),
            "F_x_claimed_strict_lower": qstr(claimed_fx),
            "F_s_abs_upper": qstr(abs_upper(fs)),
            "F_xx_abs_upper": qstr(abs_upper(fxx)),
            "F_xs_abs_upper": qstr(abs_upper(fxs)),
            "F_ss_abs_upper": qstr(abs_upper(fss)),
            "implicit_x_s_first_derivative_actual_abs_upper": qstr(abs_upper(x_prime)),
            "implicit_x_s_first_derivative_abs_upper": qstr(x_prime_claim),
            "implicit_x_s_second_derivative_actual_abs_upper": qstr(abs_upper(x_second)),
            "implicit_x_s_second_derivative_abs_upper": qstr(x_second_claim),
            "unique_analytic_graph": True,
            "graph_stays_in_s0_guard": True,
            "cut_order_preserved": True,
            "minimum_pair_separation_lower": "1/200",
            "F8_normalized_wedge_strict_lower": qstr(F8_LOWER),
            "F8_formula": "(kappa+V)/(sqrt(1+kappa^2)*sqrt(1+V^2))",
            "F8_unstable_slope_interval": "25/9<V<29",
            "F8_worst_case_squared_residual": "87997/8",
            "F9_source_pullback_unit_speed_C2_strict_upper": qstr(f9),
            "F12_suffix_rank_path": suffix_path,
            "F12_C1_trace_pullback_strict_upper": qstr(f12),
            "artificial_not_physical": True,
        }
        row["row_sha256"] = digest(row)
        rows.append(row)
    rows.sort(key=lambda row: Q(row["s0_x_dyadic_bracket"][0]))
    require(len(rows) == 23, "moving recut face count")
    require(
        [(row["stage"], row["natural_index_j"]) for row in rows]
        == list(r121.EXPECTED_CUT_ORDER),
        "moving recut order",
    )
    return rows


def outer_faces(round121: dict[str, Any]) -> list[dict[str, Any]]:
    exact_seed_id = round121["exact_seed_contract"]["exact_parent_W_seed_id"]
    rows: list[dict[str, Any]] = []
    for label, x_value, equation, lower_owner, upper_owner in (
        ("source-left", 0, "u0(x,s)=0", "EXTERNAL_NOT_MATERIALIZED", "common-rank-0"),
        ("source-right", 1, "u0(x,s)=delta", "common-rank-23", "EXTERNAL_NOT_MATERIALIZED"),
    ):
        face_id = "round122-outer-recut-face:" + digest([
            "round122-stationary-outer-recut-face-v1", exact_seed_id, label, equation,
        ])
        lower_trace = None if label == "source-left" else trace_id(face_id, "lower")
        upper_trace = trace_id(face_id, "upper") if label == "source-left" else None
        row = {
            "face_id": face_id,
            "face_kind": "STATIONARY_ARTIFICIAL_SOURCE_OUTER_FACE",
            "exact_seed_id": exact_seed_id,
            "stage": 0,
            "natural_index_j": x_value,
            "boundary_label": label,
            "exact_level_equation_id": f"round122-u0-outer-{x_value}",
            "exact_level_equation": equation,
            "delta": "1e-90",
            "s_collar": f"|s|<={qstr(EPSILON)}",
            "round121_s0_endpoint_id": r121.boundary_id(
                "left" if x_value == 0 else "right", exact_seed_id,
            ),
            "s0_x_dyadic_bracket": [str(x_value), str(x_value)],
            "equation_decimal_participates_in_id": False,
            "base_image_chart": "W",
            "base_image_obstacle": "G",
            "base_curvature": "25/9",
            "source_pullback_rank_path": [],
            "owner_below": lower_owner,
            "owner_above": upper_owner,
            "lower_trace_id": lower_trace,
            "upper_trace_id": upper_trace,
            "F_x_sign": 1,
            "F_x_s0_abs_lower": qstr(DELTA),
            "F_x_collar_abs_lower": qstr(DELTA),
            "F_x_claimed_strict_lower": qstr(DELTA),
            "F_s_abs_upper": "0",
            "F_xx_abs_upper": "0",
            "F_xs_abs_upper": "0",
            "F_ss_abs_upper": "0",
            "implicit_x_s_first_derivative_actual_abs_upper": "0",
            "implicit_x_s_first_derivative_abs_upper": "0",
            "implicit_x_s_second_derivative_actual_abs_upper": "0",
            "implicit_x_s_second_derivative_abs_upper": "0",
            "unique_analytic_graph": True,
            "graph_stays_in_s0_guard": True,
            "cut_order_preserved": True,
            "minimum_pair_separation_lower": "1/200",
            "F8_normalized_wedge_strict_lower": qstr(F8_LOWER),
            "F8_formula": "(kappa+V)/(sqrt(1+kappa^2)*sqrt(1+V^2))",
            "F8_unstable_slope_interval": "25/9<V<29",
            "F8_worst_case_squared_residual": "2350204/81",
            "F9_source_pullback_unit_speed_C2_strict_upper": "0",
            "F12_suffix_rank_path": [15, 14, 14],
            "F12_C1_trace_pullback_strict_upper": qstr(F12_OUTER),
            "artificial_not_physical": True,
            "external_neighbor_materialized": False,
        }
        row["row_sha256"] = digest(row)
        rows.append(row)
    return rows


def face_trace_and_incidence_rows(
    moving: list[dict[str, Any]],
    outer: list[dict[str, Any]],
    round121: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    children = sorted(round121["common_refinement_rows"], key=lambda row: row["common_rank"])
    boundaries = [outer[0], *moving, outer[1]]
    traces: list[dict[str, Any]] = []
    trace_index: dict[tuple[str, str], str] = {}
    for boundary_index, face in enumerate(boundaries):
        sides: list[tuple[str, dict[str, Any] | None]] = []
        if boundary_index > 0:
            sides.append(("lower", children[boundary_index - 1]))
        if boundary_index < len(children):
            sides.append(("upper", children[boundary_index]))
        for side, child in sides:
            require(child is not None, "trace child")
            identifier = trace_id(face["face_id"], side)
            require(identifier == face[f"{side}_trace_id"], "trace ID crosswalk")
            row = {
                "trace_id": identifier,
                "face_id": face["face_id"],
                "side": side,
                "adjacent_common_child_id": child["common_child_id"],
                "adjacent_common_rank": child["common_rank"],
                "external_neighbor_materialized": False if face in outer else True,
                "owner_predicate": (
                    "lower side owns points below the analytic level"
                    if side == "lower"
                    else "upper side owns the analytic level and points above it"
                ),
                "F12_C1_trace_pullback_strict_upper": face[
                    "F12_C1_trace_pullback_strict_upper"
                ],
                "artificial_not_physical": True,
            }
            row["row_sha256"] = digest(row)
            traces.append(row)
            trace_index[(face["face_id"], side)] = identifier
    require(len(traces) == 48, "face trace count")

    incidences: list[dict[str, Any]] = []
    for rank, child in enumerate(children):
        lower_face, upper_face = boundaries[rank], boundaries[rank + 1]
        row = {
            "common_child_id": child["common_child_id"],
            "common_rank": rank,
            "lower_face_id": lower_face["face_id"],
            "upper_face_id": upper_face["face_id"],
            "lower_trace_id": trace_index[(lower_face["face_id"], "upper")],
            "upper_trace_id": trace_index[(upper_face["face_id"], "lower")],
            "exactly_two_artificial_boundary_faces": True,
            "both_face_origins_retained": True,
        }
        row["row_sha256"] = digest(row)
        incidences.append(row)
    require(len(incidences) == 24, "child face incidence count")
    return traces, incidences


def physical_grammar_rows(physical: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    five = [
        {
            "kind": "source_core_clipping_face",
            "clearance_evidence": "collision-section-0 C24 core-face rows",
            "actual_instance_count": 0,
        },
        {
            "kind": "intermediate_core_avoidance_preimage_face",
            "clearance_evidence": "collision-section-1-and-2 C24 core-face rows",
            "actual_instance_count": 0,
        },
        {
            "kind": "terminal_core_preimage_face",
            "clearance_evidence": "collision-section-3 C24 core-face rows",
            "actual_instance_count": 0,
        },
        {
            "kind": "collision_singularity_or_owner_change_face",
            "clearance_evidence": "candidate tangency, root-sign, owner-gap, chart and homogeneity rows",
            "actual_instance_count": 0,
        },
        {
            "kind": "moving_occurrence_face",
            "clearance_evidence": (
                "complete seven-boundary and integer-corner-ray rows plus the "
                "57+55+57=169 immutable candidate occurrences on each rank-3 child"
            ),
            "legacy_parameterized_grammar_seed_count": 64,
            "rank3_candidate_occurrence_count_per_common_child": 169,
            "rank3_candidate_occurrence_total_check_count": 4056,
            "old_Q2_time2_atom_or_occurrence_ID_reused": False,
            "actual_instance_count": 0,
        },
    ]
    seven_specs = (
        ("candidate_signed_tangency", ("candidate_tangency",)),
        (
            "target_endpoint_on_wall_or_target_chart_seam",
            ("target_endpoint_wall", "target_chart_seam"),
        ),
        ("target_momentum_homogeneity_face", ("target_homogeneity",)),
        ("forward_integer_corner_ray", ("integer_corner_ray",)),
        ("coordinate_velocity_zero", ("coordinate_velocity_zero",)),
        (
            "source_endpoint_on_wall_or_source_chart_seam",
            ("source_endpoint_wall", "source_chart_seam"),
        ),
        ("source_momentum_homogeneity_face", ("source_homogeneity",)),
    )
    seven = []
    for kind, keys in seven_specs:
        row = {
            "kind": kind,
            "audit_keys": list(keys),
            "check_count": sum(physical["check_counts"][key] for key in keys),
            "strict_lower_margins": {
                key: physical["claimed_strict_lower_margins"][key] for key in keys
            },
            "actual_instance_count": 0,
        }
        row["row_sha256"] = digest(row)
        seven.append(row)
    for row in five:
        row["row_sha256"] = digest(row)
    require(len(five) == 5 and len(seven) == 7, "face grammar counts")
    return five, seven


def new_slot_rows(
    round121: dict[str, Any],
    incidences: list[dict[str, Any]],
    faces: list[dict[str, Any]],
    physical_digest: str,
) -> list[dict[str, Any]]:
    incidence_index = {row["common_child_id"]: row for row in incidences}
    face_index = {row["face_id"]: row for row in faces}
    base_rows = sorted(
        (
            row for row in round121["gate5_F1_F6_slot_rows"]
            if row["field_index"] == 1
        ),
        key=lambda row: (
            row["common_child_id"], row["stage"], row["roof_level_j"],
        ),
    )
    require(len(base_rows) == 120, "base slot rows")
    rows: list[dict[str, Any]] = []
    for base in base_rows:
        incidence = incidence_index[base["common_child_id"]]
        lower_face = face_index[incidence["lower_face_id"]]
        upper_face = face_index[incidence["upper_face_id"]]
        pair_f9 = max(
            Q(lower_face["F9_source_pullback_unit_speed_C2_strict_upper"]),
            Q(upper_face["F9_source_pullback_unit_speed_C2_strict_upper"]),
        )
        pair_f12 = max(
            Q(lower_face["F12_C1_trace_pullback_strict_upper"]),
            Q(upper_face["F12_C1_trace_pullback_strict_upper"]),
        )
        require(pair_f9 <= F9_STAGE2, "pair F9 global bound")
        require(pair_f12 <= F12_OUTER, "pair F12 global bound")
        for field_index, field_name in NEW_FIELDS:
            key = [
                base["official_word_key_id"],
                base["refined_homogeneous_subbranch_id"],
                base["roof_level_j"],
                field_name,
            ]
            if field_index == 7:
                value, semantics = qstr(F7_VALUE), "STRICT_UPPER"
            elif field_index == 8:
                value, semantics = qstr(F8_LOWER), "STRICT_LOWER"
            elif field_index == 9:
                value, semantics = qstr(F9_STAGE2), "STRICT_UPPER"
            elif field_index == 10:
                value, semantics = "0", "EXACT_EMPTY_PHYSICAL_FACE"
            elif field_index == 11:
                value, semantics = qstr(F11_BY_STAGE[base["stage"]]), "STRICT_UPPER"
            elif field_index == 12:
                value, semantics = qstr(F12_OUTER), "STRICT_UPPER"
            elif field_index == 13:
                value, semantics = "0", "EXACT_EMPTY_PHYSICAL_CURRENT_AND_TWO_TRACES"
            else:
                require(field_index == 16, "new field index")
                value, semantics = "0", "EXACT_EMPTY_PHYSICAL_FLUX_TRACE"
            row = {
                "slot_id": "round122-gate5-slot:" + digest(key),
                "immutable_slot_key": key,
                "official_word_key_id": base["official_word_key_id"],
                "refined_homogeneous_subbranch_id": base[
                    "refined_homogeneous_subbranch_id"
                ],
                "common_child_id": base["common_child_id"],
                "stage": base["stage"],
                "roof_level_j": base["roof_level_j"],
                "field_index": field_index,
                "field_name": field_name,
                "field_value_or_contract": value,
                "field_bound_semantics": semantics,
                "lower_artificial_face_id": incidence["lower_face_id"],
                "upper_artificial_face_id": incidence["upper_face_id"],
                "child_face_incidence_row_sha256": incidence["row_sha256"],
                "face_pair_F9_exact_max": qstr(pair_f9),
                "face_pair_F12_exact_max": qstr(pair_f12),
                "complete_artificial_face_registry_digest_replicated_across_roofs": True,
                "physical_face_empty_audit_sha256": physical_digest,
                "F7_Xi_strict_upper": qstr(XI) if field_index == 7 else None,
                "F7_invariant_density_ratio_upper": (
                    qstr(DENSITY_RATIO) if field_index == 7 else None
                ),
                "F7_actual_density_weighted_product": (
                    qstr(F7_VALUE) if field_index == 7 else None
                ),
                "F11_uses_full_phase_authoritative_envelope": field_index == 11,
                "transparent_wall_roof_split_does_not_add_F7_F11_factor": True,
                "artificial_faces_not_erased_by_physical_empty_claim": True,
                "slot_status": "CERTIFIED_ON_THIS_EXACT_SEED_COMMON_CHILD",
            }
            rows.append(row)
    require(len(rows) == 960, "new slot count")
    require(len({row["slot_id"] for row in rows}) == 960, "new slot IDs")
    require(len({tuple(row["immutable_slot_key"]) for row in rows}) == 960, "new slot keys")
    for field_index, _field_name in NEW_FIELDS:
        require(sum(row["field_index"] == field_index for row in rows) == 120, f"F{field_index} slots")
    return rows


def build(precision_bits: int = PRECISION_BITS) -> dict[str, Any]:
    require(precision_bits >= 2048, "precision must be at least 2048 bits")
    ctx.prec = precision_bits
    round121 = load_round121()
    inherited_values = r121.load_inputs()
    seed = r121.locate_seed(inherited_values)
    root_lower, root_upper, _lower_sign, _upper_sign = r121.isolate_anchor_root(seed)
    root_bracket = (root_lower, root_upper)

    physical = physical_empty_audit(seed, root_bracket, round121)
    five_face_rows, seven_boundary_rows = physical_grammar_rows(physical)
    moving_faces = moving_recut_faces(seed, root_bracket, round121)
    stationary_faces = outer_faces(round121)
    all_faces = [stationary_faces[0], *moving_faces, stationary_faces[1]]
    traces, incidences = face_trace_and_incidence_rows(
        moving_faces, stationary_faces, round121,
    )
    physical_digest = digest({
        "core": physical["core_clearance_rows_sha256"],
        "child_stage": physical["child_stage_boundary_rows_sha256"],
        "five": digest(five_face_rows),
        "seven": digest(seven_boundary_rows),
    })
    slots = new_slot_rows(round121, incidences, all_faces, physical_digest)

    inherited_slot_ids = [row["slot_id"] for row in round121["gate5_F1_F6_slot_rows"]]
    combined_slot_ids = inherited_slot_ids + [row["slot_id"] for row in slots]
    require(len(combined_slot_ids) == len(set(combined_slot_ids)) == 1680, "combined slots")

    inherited_pins = dict(round121["upstream_and_helper_pins"])
    all_pins = {**inherited_pins, **PINS}
    for name, expected in all_pins.items():
        require(sha256(HERE / name) == expected, f"all-pin mismatch: {name}")

    result = {
        "precision_bits": precision_bits,
        "round121_contract": {
            "schema": r121.SCHEMA,
            "result_sha256": digest(round121),
            "exact_parent_W_seed_id": round121["exact_seed_contract"][
                "exact_parent_W_seed_id"
            ],
            "common_refinement_actual_child_count": 24,
            "pullback_internal_cut_count": 23,
            "inherited_F1_F6_slot_count": 720,
            "inherited_F1_F6_slot_rows_sha256": round121[
                "gate5_F1_F6_slot_rows_sha256"
            ],
            "frozen_Round121_files_modified": False,
        },
        "parameter_collar_contract": {
            "parameter": "horizontal displacement of every W obstacle center",
            "closed_collar": f"|s|<={qstr(EPSILON)}",
            "epsilon": qstr(EPSILON),
            "epsilon_is_exact_dyadic": True,
            "common_to_all_24_children_and_three_legs": True,
            "source_G_obstacle_is_stationary": True,
            "W_obstacles_move_by_(s,0)": True,
            "moving_cut_shift_strict_upper": f"13*{qstr(EPSILON)}",
            "moving_cut_shift_below_Round121_2^-200_guard": True,
            "moving_cut_pair_shift_below_1/1000": True,
            "Round121_minimum_distinct_cut_separation_strict_lower": "1/200",
        },
        "physical_face_typed_empty_audit": physical,
        "physical_face_typed_empty_audit_sha256": physical_digest,
        "physical_five_face_grammar_rows": five_face_rows,
        "physical_five_face_grammar_rows_sha256": digest(five_face_rows),
        "physical_seven_boundary_kind_rows": seven_boundary_rows,
        "physical_seven_boundary_kind_rows_sha256": digest(seven_boundary_rows),
        "parameterized_recut_face_rows": moving_faces,
        "parameterized_recut_face_rows_sha256": digest(moving_faces),
        "stationary_outer_face_rows": stationary_faces,
        "stationary_outer_face_rows_sha256": digest(stationary_faces),
        "recut_face_trace_rows": traces,
        "recut_face_trace_rows_sha256": digest(traces),
        "child_face_incidence_rows": incidences,
        "child_face_incidence_rows_sha256": digest(incidences),
        "dynamic_F11_rows": [
            {
                "stage": stage,
                "full_phase_dynamic_Holder_test_pullback_strict_upper": qstr(bound),
                "alpha_scope": "0<alpha<=1",
                "along_seed_tight_diagnostic_upper": physical[
                    "along_seed_adapted_forward_Lipschitz_actual_upper"
                ][stage],
                "along_seed_tight_diagnostic_used_as_field_value": False,
            }
            for stage, bound in sorted(F11_BY_STAGE.items())
        ],
        "gate5_F7_F13_F16_slot_rows": slots,
        "gate5_F7_F13_F16_slot_rows_sha256": digest(slots),
        "combined_F1_F13_F16_slot_registry": {
            "inherited_F1_F6_slot_count": 720,
            "new_F7_F13_F16_slot_count": 960,
            "combined_slot_count": 1680,
            "slot_count_per_certified_field": 120,
            "certified_field_indices": list(range(1, 14)) + [16],
            "combined_slot_ids_sha256": digest(combined_slot_ids),
            "all_immutable_slot_keys_are_full_word_subbranch_roof_field_keys": True,
        },
        "field_bridge_theorems": {
            "F7": {
                "Xi_strict_upper": qstr(XI),
                "invariant_density_ratio_upper": qstr(DENSITY_RATIO),
                "actual_field_value_density_times_Xi": qstr(F7_VALUE),
                "arithmetic_identity": "(2000/1999)*(900337/901685)=360134800/360493663",
                "bare_Xi_installed_as_F7": False,
                "transparent_wall_roof_split_is_only_a_symbolic_prefix_suffix_split": True,
                "transparent_wall_roof_split_does_not_add_an_F7_factor": True,
            },
            "F8": {
                "artificial_face_count": 25,
                "stationary_outer_face_count": 2,
                "moving_implicit_recut_face_count": 23,
                "common_normalized_wedge_strict_lower": qstr(F8_LOWER),
                "proof_formula": "(kappa+V)/(sqrt(1+kappa^2)*sqrt(1+V^2))",
                "worst_kappa": "25/4",
                "unstable_slope_range": "25/9<V<29",
                "worst_case_squared_residual": "87997/8>0",
            },
            "F9": {
                "stationary_outer_face_C2_strict_upper": "0",
                "stage1_source_pullback_unit_speed_C2_strict_upper": qstr(F9_STAGE1),
                "stage2_source_pullback_unit_speed_C2_strict_upper": qstr(F9_STAGE2),
                "slot_common_strict_upper": qstr(F9_STAGE2),
                "per_face_origin_mapping_retained": True,
            },
            "F10": {
                "complete_physical_five_face_incidence_count": 0,
                "coarea_density_regular_bound": "0",
                "artificial_recut_faces_are_not_coarea_physical_faces": True,
            },
            "F11": {
                "stage0_full_phase_strict_upper": qstr(F11_BY_STAGE[0]),
                "stage1_full_phase_strict_upper": qstr(F11_BY_STAGE[1]),
                "stage2_full_phase_strict_upper": qstr(F11_BY_STAGE[2]),
                "along_curve_7_3_12_used_as_field_values": False,
                "transparent_wall_roof_split_is_only_a_symbolic_prefix_suffix_split": True,
                "transparent_wall_roof_split_does_not_add_an_F11_factor": True,
            },
            "F12": {
                "stationary_outer_suffix_rank_path": [15, 14, 14],
                "stationary_outer_C1_trace_pullback_strict_upper": qstr(F12_OUTER),
                "stage1_suffix_rank_path": [14, 14],
                "stage1_C1_trace_pullback_strict_upper": qstr(F12_STAGE1),
                "stage2_suffix_rank_path": [14],
                "stage2_C1_trace_pullback_strict_upper": qstr(F12_STAGE2),
                "slot_common_strict_upper": qstr(F12_OUTER),
                "internal_signed_trace_count": 46,
                "outer_seed_side_trace_count": 2,
            },
            "F13": {
                "physical_moving_boundary_current_count": 0,
                "physical_one_sided_trace_count": 0,
                "field_value": "0",
                "artificial_signed_recut_traces_are_separately_typed": True,
            },
            "F16": {
                "physical_flux_face_trace_count": 0,
                "field_value": "0",
                "empty_physical_trace_only": True,
            },
        },
        "count_ledger": {
            "exact_b_seed_count": 1,
            "common_refinement_actual_child_count": 24,
            "child_stage_physical_audit_row_count": 72,
            "core_clearance_row_count": 96,
            "physical_five_face_kind_count": 5,
            "physical_seven_boundary_kind_count": 7,
            "physical_face_instance_count": 0,
            "stationary_outer_artificial_face_count": 2,
            "moving_artificial_recut_face_count": 23,
            "artificial_face_count": 25,
            "internal_signed_artificial_trace_count": 46,
            "outer_seed_side_artificial_trace_count": 2,
            "artificial_trace_count": 48,
            "child_face_incidence_row_count": 24,
            "new_field_count": 8,
            "new_slot_count": 960,
            "combined_certified_field_count": 14,
            "combined_slot_count": 1680,
            "residual_physical_face_count": 0,
            "residual_implicit_face_count": 0,
            "residual_slot_count": 0,
        },
        "gate5_actual_child_field_status": {
            **{
                f"F{index}": "CERTIFIED_ON_ALL_24_ROUND121_EXACT_SEED_CHILDREN"
                for index in list(range(1, 14)) + [16]
            },
            "F14": "NOT_INSTALLED_ON_ROUND121_EXACT_SEED_CHILDREN",
            "F15": "NOT_INSTALLED_ON_ROUND121_EXACT_SEED_CHILDREN",
            "F17": "NOT_INSTALLED_ON_ROUND121_EXACT_SEED_CHILDREN",
            "F18": "NOT_INSTALLED_ON_ROUND121_EXACT_SEED_CHILDREN",
        },
        "rank3_seed_child_field_maturity": "14/18",
        "gate5_global_maturity": "10/18",
        "complete_18_field_block_count": 0,
        "gate5_block_count": 0,
        "cm2_verdict": "NO-GO_FOR_CLAIM",
        "strict_scope": (
            "one Round121 exact-b seed, its 24 materialized common-refinement children, "
            "the common dyadic collar |s|<=2^-512, the complete typed physical-face "
            "empty audit, and the two outer plus 23 moving artificial recut faces"
        ),
        "strict_nonclaims": [
            "no full Borel-b family uniform materialization or ranking theorem",
            "no nonempty physical-face instance, current, trace, coarea or flux claim",
            "no identification of an artificial recut face with a physical singular face",
            "no endpoint-inclusive physical collar or cross-trace union reach",
            "no F14 regular-density operator cost",
            "no F15 standard-family operator cost",
            "no F17 dynamic-test operator cost",
            "no F18 operator phase block",
            "no complete 18-field block",
            "no global Gate5 maturity upgrade",
            "no CM2 claim",
        ],
        "upstream_and_helper_pins": dict(sorted(all_pins.items())),
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--precision-bits", type=int, default=PRECISION_BITS)
    args = parser.parse_args()
    result = build(args.precision_bits)
    envelope = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    args.output.write_text(
        json.dumps(envelope, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {args.output}")
    print(f"result_sha256={envelope['result_sha256']}")
    print("ROUND122_EXACT_SEED_FIELD_MATURITY=14/18")
    print("GLOBAL_GATE5=10/18")
    print("CM2=NO-GO_FOR_CLAIM")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
