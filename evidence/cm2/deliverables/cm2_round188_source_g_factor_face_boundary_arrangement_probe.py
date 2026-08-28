#!/usr/bin/env python3
"""Read-only feasibility probe for Round186 clipped factor-face curves.

This spike asks one narrow question: do the 16,132 Round186 active-factor
faces with a strict derivative but no whole-base bracket admit a complete
rectangle-boundary arrangement?  It evaluates all four corners, requires
strict p and s derivatives on the full face, and counts the uniquely
bracketed boundary edges.

The result is diagnostic only.  It does not write a certificate, does not
materialize side-specific return signatures, and issues no whole-leaf or
global credit.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

from flint import ctx

import cm2_round186_source_g_factor_face_probe as r186


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round188.source-g-factor-face-boundary-arrangement-probe.v1"

ROUND186_SOURCE = "cm2_round186_source_g_factor_face_probe.py"
ROUND186_SOURCE_SHA256 = (
    "5797b8f4c2ba9c8c5b42b32511f3c97a15469b59bdf00cd8430580c3429c7c64"
)
ROUND182_RESULT_SHA256 = (
    "e07da794eed6dbb404de8913f5b871621f9f1b59b355172a37192791ae28911d"
)
ROUND182_VERIFICATION_RESULT_SHA256 = (
    "61715ef39e232937d821ba1c634181f905454b758abbe98d889c768ddc809797"
)
ROUND182_PINS = {
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement.py":
        "8638f2722e68bd5c6e0eb5932dc76780728998f21a47b1d8c02c28449e984d56",
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_certificate.json":
        "27491e3943e88772ec15cee110cd983b14ad82a2a56f8a07d605c3cd8fb49f08",
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json":
        "ae6e0c38df325e98b01a1d75acfbd8a85a71fda6a118db11d7dff6decf3f847c",
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_verifier.py":
        "790b17cf6dadebc37b889fff63c6ecde985cccf53c95523cd6c2bc39d12db566",
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_verification.json":
        "b008c2208891374696b88506e87957bbb754d95d62677d9406c466405b311f36",
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_report.md":
        "708272e9425bef74f3f4639c76fd17078f509d3acc5d324325c224e743985f0c",
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_cold_replay.md":
        "c0fd075a0ba56de5380c6cc89620dc82fa640c0466b118565cf1755aedf61f99",
}
ROUND182_MANIFEST = (
    "cm2_round182_source_g_clipped_graph_and_pair_arrangement_manifest.sha256"
)
ROUND182_MANIFEST_SHA256 = (
    "32dea92dd0de87d3ded6ed69a908b58b01402ddcdef3f0e2b5ffde096a9383c5"
)

EXPECTED_OUTGOING_RESIDUAL_LEAVES = 18_324
EXPECTED_OUTGOING_ORIGINS = 8_268
EXPECTED_RETAINED_CHILDREN = 11_960
EXPECTED_OUTGOING_VOLUME = Q(861459, 419430400000)
EXPECTED_UNRESOLVED_FACES = 18_412
EXPECTED_NO_BRACKET_FACES = 16_132

STRICT_SIGNS = {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
NO_BRACKET = "ONE_ACTIVE_FACTOR_STRICT_DERIVATIVE_NO_BRACKET"


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def canonical(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def file_sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            value.update(chunk)
    return value.hexdigest()


def check_inputs() -> dict[str, Any]:
    require(
        Path(r186.__file__).resolve() == (HERE / ROUND186_SOURCE).resolve(),
        "Round186 module identity",
    )
    require(
        file_sha256(HERE / ROUND186_SOURCE) == ROUND186_SOURCE_SHA256,
        "Round186 source pin",
    )
    for name, expected in ROUND182_PINS.items():
        require(file_sha256(HERE / name) == expected, f"Round182 pin:{name}")
    require(
        file_sha256(HERE / ROUND182_MANIFEST) == ROUND182_MANIFEST_SHA256,
        "Round182 manifest pin",
    )

    manifest: dict[str, str] = {}
    for line in (HERE / ROUND182_MANIFEST).read_text("ascii").splitlines():
        value, name = line.split("  ", 1)
        require(name not in manifest, f"manifest duplicate:{name}")
        manifest[name] = value
    require(manifest == ROUND182_PINS, "Round182 manifest exact entries")

    certificate = json.loads(
        (
            HERE
            / "cm2_round182_source_g_clipped_graph_and_pair_arrangement"
              "_certificate.json"
        ).read_text()
    )
    verification = json.loads(
        (
            HERE
            / "cm2_round182_source_g_clipped_graph_and_pair_arrangement"
              "_verification.json"
        ).read_text()
    )
    require(
        certificate["result_sha256"] == ROUND182_RESULT_SHA256,
        "Round182 result pin",
    )
    require(
        verification["result_sha256"]
        == ROUND182_VERIFICATION_RESULT_SHA256
        and verification["result"]["status"] == "PASS",
        "Round182 verification result",
    )
    return {
        "Round182_result_sha256": ROUND182_RESULT_SHA256,
        "Round182_verification_result_sha256":
            ROUND182_VERIFICATION_RESULT_SHA256,
        "Round182_rows_sha256": ROUND182_PINS[
            "cm2_round182_source_g_clipped_graph_and_pair_arrangement_rows.json"
        ],
        "Round186_probe_source_sha256": ROUND186_SOURCE_SHA256,
    }


def sign(value: Any) -> str:
    return r186.r179.arb_sign(value)


def point_box(
    face: Any,
    p: Q,
    s: Q,
    label: str,
) -> Any:
    return r186.r179.r174.atlas.AtlasBox(
        face.t0,
        face.t1,
        p,
        p,
        s,
        s,
        face.depth,
        face.path + "." + label,
    )


def boundary_arrangement(
    collar: dict[str, Any],
    box: Any,
    upper: bool,
    profile: dict[str, Any],
) -> dict[str, Any]:
    active = [
        kind
        for kind in ("HPLUS", "HMINUS")
        if profile[kind][0] == "OVERWRAP"
    ]
    inactive = [
        kind
        for kind in ("HPLUS", "HMINUS")
        if profile[kind][0] != "OVERWRAP"
    ]
    require(
        len(active) == len(inactive) == 1,
        "one active and one inactive factor",
    )
    active_kind = active[0]
    inactive_kind = inactive[0]
    require(
        profile[inactive_kind][0] in STRICT_SIGNS,
        "inactive factor strict sign",
    )

    face = r186.r179.face_box(box, "t", upper)
    factors = r186.factor_geometry(
        collar["chart"], collar["owner_target"], face
    )
    dp = factors[active_kind][1][1]
    ds = factors[active_kind][1][2]
    dp_sign = "UNAVAILABLE" if dp is None else sign(dp)
    ds_sign = "UNAVAILABLE" if ds is None else sign(ds)
    graph_axis = (
        "p"
        if dp_sign in STRICT_SIGNS
        else "s" if ds_sign in STRICT_SIGNS else None
    )
    if graph_axis is None:
        return {
            "status": "NO_FULL_FACE_STRICT_GRAPH_DERIVATIVE_RESIDUAL",
            "active_factor": active_kind,
            "inactive_factor": inactive_kind,
            "inactive_factor_sign": profile[inactive_kind][0],
            "dp_sign": dp_sign,
            "ds_sign": ds_sign,
        }

    corners = (
        ("SW", face.p0, face.s0),
        ("SE", face.p1, face.s0),
        ("NE", face.p1, face.s1),
        ("NW", face.p0, face.s1),
    )
    corner_signs: dict[str, str] = {}
    for label, p, s in corners:
        value = r186.factor_geometry(
            collar["chart"],
            collar["owner_target"],
            point_box(face, p, s, label),
        )[active_kind][0]
        corner_signs[label] = sign(value)

    if any(value not in STRICT_SIGNS for value in corner_signs.values()):
        return {
            "status": "CORNER_SIGN_OVERWRAP_RESIDUAL",
            "active_factor": active_kind,
            "inactive_factor": inactive_kind,
            "inactive_factor_sign": profile[inactive_kind][0],
            "dp_sign": dp_sign,
            "ds_sign": ds_sign,
            "graph_axis": graph_axis,
            "corner_signs": corner_signs,
        }

    edge_specs = {
        "S": (("SW", "SE"), "s", False, 1),
        "E": (("SE", "NE"), "p", True, 2),
        "N": (("NW", "NE"), "s", True, 1),
        "W": (("SW", "NW"), "p", False, 2),
    }
    edge_dispositions: dict[str, str] = {}
    edge_derivative_signs: dict[str, str] = {}
    edge_C0_signs: dict[str, str] = {}
    for edge, (
        (lower, upper_label),
        fixed_axis,
        fixed_upper,
        derivative_index,
    ) in edge_specs.items():
        edge_box = r186.r179.face_box(face, fixed_axis, fixed_upper)
        edge_factor = r186.factor_geometry(
            collar["chart"], collar["owner_target"], edge_box
        )[active_kind]
        edge_direct_sign = sign(edge_factor[0])
        edge_centered_sign = sign(
            r186.centered_value(
                collar["chart"],
                collar["owner_target"],
                edge_box,
                active_kind,
            )
        )
        edge_C0_sign = (
            edge_direct_sign
            if edge_direct_sign in STRICT_SIGNS
            else edge_centered_sign
        )
        edge_C0_signs[edge] = edge_C0_sign
        derivative = edge_factor[1][derivative_index]
        derivative_sign = (
            "UNAVAILABLE" if derivative is None else sign(derivative)
        )
        edge_derivative_signs[edge] = derivative_sign
        endpoint_signs = {
            corner_signs[lower],
            corner_signs[upper_label],
        }
        if edge_C0_sign in STRICT_SIGNS:
            require(
                corner_signs[lower] == edge_C0_sign
                and corner_signs[upper_label] == edge_C0_sign,
                "edge C0 and corner sign consistency",
            )
            edge_dispositions[edge] = "STRICT_C0_ZERO_ABSENT"
        elif derivative_sign in STRICT_SIGNS:
            edge_dispositions[edge] = (
                "UNIQUE_BRACKETED_ZERO"
                if endpoint_signs == STRICT_SIGNS
                else "STRICT_MONOTONE_ZERO_ABSENT"
            )
        else:
            edge_dispositions[edge] = "EDGE_ZERO_SET_UNRESOLVED"

    unresolved_edges = sorted(
        edge
        for edge, disposition in edge_dispositions.items()
        if disposition == "EDGE_ZERO_SET_UNRESOLVED"
    )
    bracketed_edges = sorted(
        edge
        for edge, disposition in edge_dispositions.items()
        if disposition == "UNIQUE_BRACKETED_ZERO"
    )
    if unresolved_edges or len(bracketed_edges) != 2:
        return {
            "status": "BOUNDARY_ENDPOINT_COUNT_RESIDUAL",
            "active_factor": active_kind,
            "inactive_factor": inactive_kind,
            "inactive_factor_sign": profile[inactive_kind][0],
            "dp_sign": dp_sign,
            "ds_sign": ds_sign,
            "graph_axis": graph_axis,
            "corner_signs": corner_signs,
            "edge_C0_signs": edge_C0_signs,
            "edge_derivative_signs": edge_derivative_signs,
            "edge_dispositions": edge_dispositions,
            "unresolved_edges": unresolved_edges,
            "bracketed_edges": bracketed_edges,
        }

    pair = "|".join(bracketed_edges)
    topology = (
        "FULL_TRANSVERSE_GRAPH_WITH_OPPOSITE_BOUNDARY_ENDPOINTS"
        if (
            (graph_axis == "p" and pair == "N|S")
            or (graph_axis == "s" and pair == "E|W")
        )
        else "CLIPPED_MONOTONE_FACTOR_CURVE"
    )
    return {
        "status": "UNIQUE_TWO_ENDPOINT_FACTOR_CURVE",
        "active_factor": active_kind,
        "inactive_factor": inactive_kind,
        "inactive_factor_sign": profile[inactive_kind][0],
        "dp_sign": dp_sign,
        "ds_sign": ds_sign,
        "graph_axis": graph_axis,
        "corner_signs": corner_signs,
        "edge_C0_signs": edge_C0_signs,
        "edge_derivative_signs": edge_derivative_signs,
        "edge_dispositions": edge_dispositions,
        "bracketed_edges": bracketed_edges,
        "edge_pair": pair,
        "topology": topology,
        "boundary_endpoint_count": 2,
        "each_boundary_endpoint_unique_by_strict_edge_derivative": True,
        "curve_regular_by_selected_strict_derivative": True,
        "curve_single_valued_over_transverse_coordinate": True,
        "inactive_factor_excludes_simultaneous_factor_zero": True,
    }


def main() -> int:
    ctx.prec = 256
    pins = check_inputs()
    wrapper = json.loads(r186.ROWS.read_text())
    source = wrapper["result"]
    schemas = source["row_column_schemas"]
    collars = r186.unpack(
        source["collar_occurrence_rows"],
        schemas["collar_occurrence_rows"],
    )
    collar_by_occurrence = {
        row["Round179_occurrence_row_id"]: row for row in collars
    }
    leaves = r186.unpack(
        source["collar_leaf_rows"],
        schemas["collar_leaf_rows"],
    )
    residual = [
        row
        for row in leaves
        if Q(row["residual_3d_collar_volume"]) > 0
    ]
    outgoing = [
        row
        for row in residual
        if collar_by_occurrence[row["occurrence_row_id"]]["kind"]
        == "OUTGOING"
    ]
    require(
        len(outgoing) == EXPECTED_OUTGOING_RESIDUAL_LEAVES,
        "outgoing leaf count",
    )
    require(
        len({
            collar_by_occurrence[row["occurrence_row_id"]]["origin_row_id"]
            for row in outgoing
        })
        == EXPECTED_OUTGOING_ORIGINS,
        "outgoing origin count",
    )
    require(
        len({row["retained_child_row_id"] for row in outgoing})
        == EXPECTED_RETAINED_CHILDREN,
        "retained child count",
    )
    require(
        sum(
            (Q(row["residual_3d_collar_volume"]) for row in outgoing),
            Q(0),
        )
        == EXPECTED_OUTGOING_VOLUME,
        "outgoing exact volume",
    )

    baseline_classes: Counter[str] = Counter()
    arrangement_statuses: Counter[str] = Counter()
    edge_pairs: Counter[str] = Counter()
    active_factors: Counter[str] = Counter()
    derivative_sign_pairs: Counter[str] = Counter()
    graph_axes: Counter[str] = Counter()
    corner_patterns: Counter[str] = Counter()
    face_sides: Counter[str] = Counter()
    evidence_rows: list[dict[str, Any]] = []
    single_unresolved_leaves = 0
    double_unresolved_leaves = 0

    for index, row in enumerate(outgoing, 1):
        collar = collar_by_occurrence[row["occurrence_row_id"]]
        box = r186.r179.r174.atlas.AtlasBox(
            *(Q(value) for value in row["box"]),
            0,
            row["row_id"],
        )
        unresolved_sides = [
            (side, upper)
            for side, status, upper in (
                ("LOWER", row["lower_t_face_status"], False),
                ("UPPER", row["upper_t_face_status"], True),
            )
            if status == "U"
        ]
        require(unresolved_sides, f"outgoing unresolved face:{row['row_id']}")
        if len(unresolved_sides) == 1:
            single_unresolved_leaves += 1
        elif len(unresolved_sides) == 2:
            double_unresolved_leaves += 1
        else:
            raise RuntimeError(f"unresolved side count:{row['row_id']}")

        for side, upper in unresolved_sides:
            profile, normal_excluded = r186.face_profile(
                collar["chart"], collar["owner_target"], box, upper
            )
            require(normal_excluded, f"normal exclusion:{row['row_id']}:{side}")
            label = r186.resolution(profile)
            baseline_classes[label] += 1
            if label != NO_BRACKET:
                continue
            arrangement = boundary_arrangement(
                collar, box, upper, profile
            )
            arrangement_statuses[arrangement["status"]] += 1
            active_factors[arrangement["active_factor"]] += 1
            derivative_sign_pairs[
                arrangement["dp_sign"] + "|" + arrangement["ds_sign"]
            ] += 1
            graph_axes[str(arrangement.get("graph_axis"))] += 1
            corner_patterns[
                "|".join(
                    arrangement.get("corner_signs", {}).get(
                        name, "NOT_EVALUATED"
                    )
                    for name in ("SW", "SE", "NE", "NW")
                )
            ] += 1
            face_sides[side] += 1
            if "edge_pair" in arrangement:
                edge_pairs[arrangement["edge_pair"]] += 1
            evidence_rows.append({
                "leaf_row_id": row["row_id"],
                "occurrence_row_id": row["occurrence_row_id"],
                "origin_row_id": collar["origin_row_id"],
                "side": side,
                **arrangement,
            })
        if index % 2000 == 0 or index == len(outgoing):
            print(
                f"boundary-arrangement {index}/{len(outgoing)}",
                file=sys.stderr,
                flush=True,
            )

    require(
        sum(baseline_classes.values()) == EXPECTED_UNRESOLVED_FACES,
        "unresolved face conservation",
    )
    require(
        baseline_classes[NO_BRACKET] == EXPECTED_NO_BRACKET_FACES
        and len(evidence_rows) == EXPECTED_NO_BRACKET_FACES,
        "no-bracket face census",
    )
    resolved_count = arrangement_statuses[
        "UNIQUE_TWO_ENDPOINT_FACTOR_CURVE"
    ]
    residual_count = EXPECTED_NO_BRACKET_FACES - resolved_count

    probe_result = {
        "status":
            "READ_ONLY_ZERO_PROMOTION_FACTOR_FACE_BOUNDARY_ARRANGEMENT_PROBE",
        "input_chain": pins,
        "scope": {
            "source_obstacle": "G",
            "target_obstacle": "W",
            "outgoing_residual_leaf_count": len(outgoing),
            "outgoing_origin_count": EXPECTED_OUTGOING_ORIGINS,
            "retained_child_count": EXPECTED_RETAINED_CHILDREN,
            "exact_coordinate_volume": str(EXPECTED_OUTGOING_VOLUME),
            "single_unresolved_t_face_leaf_count": single_unresolved_leaves,
            "double_unresolved_t_face_leaf_count": double_unresolved_leaves,
            "unresolved_t_face_count": sum(baseline_classes.values()),
        },
        "Round186_baseline_face_classes":
            dict(sorted(baseline_classes.items())),
        "boundary_arrangement": {
            "input_no_complete_base_bracket_face_count":
                EXPECTED_NO_BRACKET_FACES,
            "status_count": dict(sorted(arrangement_statuses.items())),
            "resolved_unique_two_endpoint_curve_count": resolved_count,
            "residual_face_count": residual_count,
            "active_factor_count": dict(sorted(active_factors.items())),
            "strict_dp_ds_sign_pair_count":
                dict(sorted(derivative_sign_pairs.items())),
            "selected_graph_axis_count": dict(sorted(graph_axes.items())),
            "bracketed_boundary_edge_pair_count":
                dict(sorted(edge_pairs.items())),
            "corner_sign_pattern_count":
                dict(sorted(corner_patterns.items())),
            "face_side_count": dict(sorted(face_sides.items())),
            "evidence_row_count": len(evidence_rows),
            "evidence_rows_sha256": digest(evidence_rows),
            "all_four_corner_signs_strict":
                not arrangement_statuses[
                    "CORNER_SIGN_OVERWRAP_RESIDUAL"
                ],
            "all_active_factors_have_a_selected_strict_graph_derivative":
                not arrangement_statuses[
                    "NO_FULL_FACE_STRICT_GRAPH_DERIVATIVE_RESIDUAL"
                ],
            "all_resolved_curves_have_exactly_two_unique_boundary_endpoints":
                residual_count == 0,
            "topological_scope":
                "2D t-face factor-zero curve only; not a 3D leaf or "
                "side-specific return-signature certificate",
        },
        "uncovered_tail": {
            "two_sided_U_leaf_count": double_unresolved_leaves,
            "two_sided_curves_require_cross_t_ordering": True,
            "wall_G_residual_leaf_count": 64,
            "wall_G_processed_here": False,
        },
        "zero_promotion_contract": {
            "probe_only": True,
            "filesystem_writes": 0,
            "evidence_rows_emitted_as_attachment": False,
            "official_source_G_global_disposition_count": 0,
            "official_source_G_global_disposition_denominator": 224580,
            "whole_leaf_credit_issued": 0,
            "D02": "UNCHANGED_BLOCKED",
            "global_Gate5_fields": "UNCHANGED_10/18",
            "CM2": "UNCHANGED_NO_GO",
            "required_next":
                "formal producer with full evidence rows, side-specific "
                "return signatures, U|U cross-t ordering, wall-G tail, "
                "and an independent verifier",
        },
    }
    document = {
        "schema": SCHEMA,
        "probe_result": probe_result,
        "probe_result_sha256": digest(probe_result),
    }
    sys.stdout.write(
        json.dumps(
            document,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
