#!/usr/bin/env python3
"""Round134: fail-closed Round28-to-exact-seed occurrence incidence frontier.

This layer installs the typed crosswalk that Round122 deliberately did not
install.  It joins all 64 materialized Round28 occurrence records to the
Round113/121 exact-seed source type, reduces the 44 source-G records to 16
signed target sheets and 12 target lifts, and checks the target tangency
discriminants on the whole selected Round113 source rectangle and
``s in [-1/400,1/400]``.

No discriminant meets zero.  This independently agrees with the complete
Round122 24-child by 3-stage empty audit.  The 32 Round75 curves are also
typed here: they are stationary destination-core boundary preimages, not
moving occurrence pullbacks.  Thus neither route supplies an owned Round67
record.  Existence of an occurrence pullback on some other, newly constructed
parent curve remains UNKNOWN_NOT_CERTIFIED rather than being declared empty.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_gate3_candidate_first_hit_cert as first_hit


HERE = Path(__file__).resolve().parent
PRODUCER = Path(__file__).resolve()
OUTPUT = (
    HERE
    / "cm2-round134-round28-exact-seed-occurrence-incidence-frontier-2026-07-24.json"
)
SCHEMA = "cm2.round134.round28-exact-seed-occurrence-incidence-frontier.v1"
PRECISION_BITS = 2048

FIRST_HIT_P = HERE / "cm2_gate3_candidate_first_hit_cert.py"
R75P = HERE / "cm2_round75_r2_physical_curve_generator.py"
R75 = HERE / "cm2-round75-r2-physical-curves-2026-07-21.json"
R75QP = HERE / "cm2_round75_r2_physical_subquotient_cert.py"
R75Q = HERE / "cm2-round75-r2-physical-subquotient-manifest-2026-07-21.json"
R113P = HERE / "cm2_round113_rank3_endpoint_sheet_owner_ordering.py"
R113 = HERE / "cm2-round113-rank3-endpoint-sheet-owner-ordering-2026-07-23.json"
R122P = HERE / "cm2_round122_rank3_exact_seed_physical_face_field_bridge.py"
R122 = HERE / "cm2-round122-rank3-exact-seed-physical-face-field-bridge-2026-07-23.json"
R132P = HERE / "cm2_round132_round28_occurrence_record_materialization.py"
R132 = HERE / "cm2-round132-round28-occurrence-record-materialization-2026-07-24.json"
R133P = HERE / "cm2_round133_round132_owner_map_realizability_audit.py"
R133 = HERE / "cm2-round133-round132-owner-map-realizability-audit-2026-07-24.json"

INPUTS = (
    FIRST_HIT_P,
    R75P, R75, R75QP, R75Q, R113P, R113, R122P, R122, R132P, R132, R133P, R133,
)

BYTE_PINS = {
    FIRST_HIT_P.name: "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    R75P.name: "60cbbd4e433c0c7aef15ce500af428e19041f281fcf235d55e7413b6f7b5b026",
    R75.name: "ef3005c3306e321966daf6cf10db04a9ea54b5f10b1de0cd7bb4194b8eaa85cb",
    R75QP.name: "22c39c5d693cb04a50a2a801a6b510a3ca2877f31c85b4c54376ad7c980a1191",
    R75Q.name: "460f32ffd650b14c5f9c4688b8cc01cfd08778751ee4d3dd73ca0d63151a0580",
    R113P.name: "249e30c6410bf77e2c81aec346461fd4c0d4d4c8448e74894f73f0b8ccd0bfd3",
    R113.name: "d38d0fb159ea31ce430c1e2a27b88cc630d786921d3d4642f2bd3fe7c298e181",
    R122P.name: "44a64789635b8adfb597376d25afcbf8cb39dbaf0c2a19c4031bcbe78b3848f4",
    R122.name: "a7ed51149916bbf0d181b9cd45114cd11d81a5d30e72fea50b3336d1ead22028",
    R132P.name: "88a12779148a49f111380c0560b0cb490a4e87f00d7ba7671878eec858f87d53",
    R132.name: "b5d09c7398dae4b77a6f011430286f88539e0f13ca449e50eb84fc3712d67d31",
    R133P.name: "3607bf2a3b2498c13d4bab27113dd151577e050cb83e68535ee32aaadbd79722",
    R133.name: "a020ce376c1398384e5f304aff320aa214721f5f8d8bcc1e35bfa31eadd54c91",
}

SCHEMA_PINS = {
    R75.name: "cm2.round75.r2-physical-curves.v1",
    R75Q.name: "cm2.round75.r2-physical-subquotient.v1",
    R113.name: "cm2.round113.rank3-endpoint-sheet-owner-ordering.v1",
    R122.name: "cm2.round122.rank3-exact-seed-physical-face-field-bridge.v1",
    R132.name: "cm2.round132.round28-occurrence-record-materialization.v1",
    R133.name: "cm2.round133.round132-owner-map-realizability-audit.v1",
}

RESULT_PINS = {
    R75.name: "94208887c3364995e5a781b8d57c60741fef33b14441343d6a3f71a459aa94b4",
    R75Q.name: "104c7935465ee53d749381628e00e0f85f079a6b284ea70095e4167bae833bca",
    R113.name: "33f564bd6afea1ba346ed0048a4bc61fa1a1bf91ebbbac546a32b051643bda67",
    R122.name: "e8bc4e02635b70dda7cee0485811ae68d42ee595c37a03a5b2aa94ecf170f6cb",
    R132.name: "3a5b4450d838ac39e0e7f596344589b520a8060bb0131bd88fb8f2c77af4d624",
    R133.name: "0e8e446fc81b1432dac31a9e7fc407b74bd6948dbd72451c67ffc43034f05ed2",
}

PARENT_CELL_ID = (
    "round113-cell:08b7ca8449af5f6e8d4e3abce98803656664ed7ec957aba62406763b68b2fea6"
)
EXACT_PARENT_ID = (
    "round121-exact-parent-W:41462c4f6815ad00fd5d4456e5c13885feeab5e8343b009b8872b72d15cf18c8"
)
TARGET_LIFTS_SHA256 = (
    "221eddd881ca4a82729a7842e0d89a8b71a1307d63ecb550f7545b931dabf769"
)
SIGNED_SHEETS_SHA256 = (
    "5ed98afe90cd8bd8504260edce1623efa1795a1075faff793bd15c08d600f6c5"
)
OCCURRENCE_MAP_SHA256 = (
    "91e5495bc44057296f883261027505786a79855b1042cdecd96a8408d9279f12"
)


class VerificationError(RuntimeError):
    """Fail-closed input, reconstruction, semantic or output error."""


def require(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


def canonical(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, child in pairs:
        require(key not in value, f"duplicate JSON key:{key}")
        value[key] = child
    return value


def reject_constant(token: str) -> None:
    raise VerificationError(f"non-finite JSON token:{token}")


def strict_json(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    require(not raw.startswith(b"\xef\xbb\xbf"), f"UTF-8 BOM:{path.name}")
    try:
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=strict_object,
            parse_constant=reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise VerificationError(f"strict JSON:{path.name}") from exc
    require(isinstance(value, dict), f"top-level object:{path.name}")
    return value


def exact_dyadic(point: Any) -> Q:
    mantissa, exponent = point.man_exp()
    return Q(int(mantissa)) * (Q(2) ** int(exponent))


def arb_pair(value: arb) -> tuple[Q, Q]:
    return exact_dyadic(value.lower()), exact_dyadic(value.upper())


def aq(value: Q | int) -> arb:
    value = Q(value)
    return arb(value.numerator) / value.denominator


def arb_delta(t: arb, c0: arb, s: arb, target: str) -> arb:
    """Evaluate the source-to-white-target line discriminant on Arb inputs."""
    require(target.startswith("W[") and target.endswith("]"), "white target")
    ix_text, iy_text = target[2:-1].split(",")
    ix, iy = int(ix_text), int(iy_text)
    nx = -(arb(1) - t * t).sqrt()
    ny = t
    p = (arb(1) - c0 * c0).sqrt()
    ux = c0 * nx - p * ny
    uy = c0 * ny + p * nx
    qx = aq(Q(9, 25)) * nx
    qy = aq(Q(9, 25)) * ny
    dx = arb(ix) + aq(Q(1, 2)) + s - qx
    dy = arb(iy) + aq(Q(1, 2)) - qy
    transverse = -uy * dx + ux * dy
    return aq(Q(16, 625)) - transverse * transverse


def point_delta(t: Q, c0: Q, s: Q, target: str) -> arb:
    """Auxiliary point evaluation at one box corner."""
    return arb_delta(aq(t), aq(c0), aq(s), target)


def box_delta(
    t_bounds: tuple[Q, Q],
    c0_bounds: tuple[Q, Q],
    s_bounds: tuple[Q, Q],
    target: str,
) -> arb:
    """Direct interval evaluation on the complete ``t x c0 x s`` box."""
    return arb_delta(
        first_hit.arb_interval(*t_bounds),
        first_hit.arb_interval(*c0_bounds),
        first_hit.arb_interval(*s_bounds),
        target,
    )


def floor_fraction(value: Q) -> int:
    return value.numerator // value.denominator


def ceil_fraction(value: Q) -> int:
    return -((-value.numerator) // value.denominator)


def outward_decimal_enclosure(
    lower: Q,
    upper: Q,
    decimal_places: int = 12,
) -> tuple[Q, Q]:
    """Return a compact decimal-rational enclosure containing exact Arb ends."""
    scale = 10 ** decimal_places
    return (
        Q(floor_fraction(lower * scale), scale),
        Q(ceil_fraction(upper * scale), scale),
    )


def q_text(value: Q) -> str:
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def load_inputs() -> dict[str, dict[str, Any]]:
    for path in INPUTS:
        require(path.is_file() and not path.is_symlink(), f"regular input:{path.name}")
        require(path.resolve().parent == HERE, f"input parent:{path.name}")
        require(sha256_path(path) == BYTE_PINS[path.name], f"byte pin:{path.name}")

    documents: dict[str, dict[str, Any]] = {}
    for path in (R75, R75Q, R113, R122, R132, R133):
        document = strict_json(path)
        require(document.get("schema") == SCHEMA_PINS[path.name], f"schema:{path.name}")
        result = document.get("result")
        require(isinstance(result, dict), f"result object:{path.name}")
        require(digest(result) == RESULT_PINS[path.name], f"result pin:{path.name}")
        stored = document.get("result_sha256")
        if stored is not None:
            require(stored == RESULT_PINS[path.name], f"stored result pin:{path.name}")
        documents[path.name] = document
    return documents


def selected_cell(r113: dict[str, Any]) -> dict[str, Any]:
    matches = [
        cell
        for sheet in r113["sheet_rows"]
        for cell in sheet.get("certified_cells", [])
        if cell["cell_id"] == PARENT_CELL_ID
    ]
    require(len(matches) == 1, "unique selected Round113 cell")
    cell = matches[0]
    require(cell["source_chart"] == "W", "selected source chart")
    require(cell["parameter_box"] == {
        "b3": ["1/32768", "1/16384"],
        "c0": ["3/65536", "1/16384"],
    }, "selected parameter box")
    return cell


def typed_occurrence_crosswalk(
    r132: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[list[Any]], list[str]]:
    rows = r132["occurrence_face_record_rows"]
    require(isinstance(rows, list) and len(rows) == 64, "64 Round132 records")
    mapping = [
        {
            "occurrence_record_id": row["occurrence_record_id"],
            "source": row["source"],
            "target": row["tangent_target"],
            "epsilon": row["epsilon"],
        }
        for row in rows
    ]
    require(digest(mapping) == OCCURRENCE_MAP_SHA256, "64-record typed map digest")
    source_g = [row for row in mapping if row["source"] == "G"]
    source_w = [row for row in mapping if row["source"] == "W"]
    require(len(source_g) == 44 and len(source_w) == 20, "44/20 source split")
    signed = sorted({(row["target"], row["epsilon"]) for row in source_g})
    signed_rows = [[target, epsilon] for target, epsilon in signed]
    targets = sorted({target for target, _epsilon in signed})
    require(len(signed_rows) == 16 and len(targets) == 12, "16 sheets / 12 lifts")
    require(digest(signed_rows) == SIGNED_SHEETS_SHA256, "signed-sheet digest")
    require(digest(targets) == TARGET_LIFTS_SHA256, "target-lift digest")
    return mapping, signed_rows, targets


def discriminant_audit(
    cell: dict[str, Any],
    signed_rows: list[list[Any]],
    targets: list[str],
) -> list[dict[str, Any]]:
    ctx.prec = PRECISION_BITS
    t_bounds = tuple(Q(value) for value in cell["implicit_t_root_enclosure"])
    c_bounds = tuple(Q(value) for value in cell["parameter_box"]["c0"])
    s_bounds = (Q(-1, 400), Q(1, 400))
    signed_count = {target: 0 for target in targets}
    for target, _epsilon in signed_rows:
        signed_count[target] += 1

    rows: list[dict[str, Any]] = []
    for target in targets:
        box_value = box_delta(t_bounds, c_bounds, s_bounds, target)
        box_lower, box_upper = arb_pair(box_value)
        require(
            box_lower > 0 or box_upper < 0,
            f"whole rectangle interval sign:{target}",
        )
        enclosure_lower, enclosure_upper = outward_decimal_enclosure(
            box_lower,
            box_upper,
        )
        require(
            enclosure_lower <= box_lower and box_upper <= enclosure_upper,
            f"outward enclosure:{target}",
        )
        interval_sign = 1 if box_lower > 0 else -1

        # Corner evaluations are retained only as a reproducibility crosscheck.
        # They do not establish a sign on the nonlinear whole rectangle.
        corner_values = [
            point_delta(t, c0, s, target)
            for t in t_bounds
            for c0 in c_bounds
            for s in s_bounds
        ]
        lower = min(arb_pair(value)[0] for value in corner_values)
        upper = max(arb_pair(value)[1] for value in corner_values)
        require(lower > 0 or upper < 0, f"corner sign:{target}")
        corner_sign = 1 if lower > 0 else -1
        require(corner_sign == interval_sign, f"corner/box sign agreement:{target}")
        status = "STRICT_POSITIVE_TWO_LINE_INTERSECTIONS" if interval_sign > 0 else (
            "STRICT_NEGATIVE_WHOLE_LINE_MISS"
        )
        row = {
            "target_lift": target,
            "Round28_signed_sheet_count": signed_count[target],
            "whole_rectangle_interval_check": True,
            "whole_rectangle_discriminant_enclosure": [
                q_text(enclosure_lower),
                q_text(enclosure_upper),
            ],
            "whole_rectangle_interval_sign": interval_sign,
            "whole_rectangle_status": status,
            "zero_tangency_root_count": 0,
            "corner_auxiliary_evaluation_count": len(corner_values),
            "corner_auxiliary_sign": corner_sign,
            "corner_auxiliary_sign_agrees": True,
        }
        row["row_sha256"] = digest(row)
        rows.append(row)

    positive = [
        row for row in rows if row["whole_rectangle_interval_sign"] == 1
    ]
    negative = [
        row for row in rows if row["whole_rectangle_interval_sign"] == -1
    ]
    require(len(positive) == 2 and len(negative) == 10, "2 positive / 10 negative")
    require(
        [row["target_lift"] for row in positive] == ["W[-1,-1]", "W[-1,-2]"],
        "positive target identities",
    )

    tightest = min(
        rows,
        key=lambda row: (
            Q(row["whole_rectangle_discriminant_enclosure"][0])
            if row["whole_rectangle_interval_sign"] > 0
            else -Q(row["whole_rectangle_discriminant_enclosure"][1])
        ),
    )
    require(tightest["target_lift"] == "W[-1,0]", "tightest target identity")
    tight_lower, tight_upper = (
        Q(value) for value in tightest["whole_rectangle_discriminant_enclosure"]
    )
    require(
        [q_text(tight_lower), q_text(tight_upper)]
        == ["-374189179/25000000000", "-101296291/7812500000"],
        "tightest target outward enclosure",
    )
    require(tight_upper < Q(-1, 100), "uniform discriminant gap")
    return rows


def validate_round75(r75: dict[str, Any], r75q: dict[str, Any]) -> None:
    require(
        r75["physical_R2_component_count"] == 16
        and r75["physical_R2_curve_count"] == 32,
        "Round75 census",
    )
    curves = r75["curve_rows"]
    require(len(curves) == 32, "Round75 curve rows")
    require(all(
        row["active_side"] in {"t_lower", "t_upper", "p_lower", "p_upper"}
        and row["source_stationary_sides"]
        for row in curves
    ), "Round75 stationary side levels")
    require(
        r75q["scope"].startswith("actual fixed s=0 depth-two physical subquotient"),
        "Round75 fixed-s R2 scope",
    )
    require(
        r75q["physical_R2_curve_atlas"]["physical_curves"] == 32,
        "Round75 subquotient curve count",
    )


def build_result() -> dict[str, Any]:
    documents = load_inputs()
    r75 = documents[R75.name]["result"]
    r75q = documents[R75Q.name]["result"]
    r113 = documents[R113.name]["result"]
    r122 = documents[R122.name]["result"]
    r132 = documents[R132.name]["result"]
    r133 = documents[R133.name]["result"]
    validate_round75(r75, r75q)
    cell = selected_cell(r113)
    mapping, signed_rows, targets = typed_occurrence_crosswalk(r132)
    delta_rows = discriminant_audit(cell, signed_rows, targets)

    empty = r122["physical_face_typed_empty_audit"]
    ledger = r122["count_ledger"]
    require(
        r122["round121_contract"]["exact_parent_W_seed_id"] == EXACT_PARENT_ID,
        "Round122 exact parent ID",
    )
    require(
        r122["physical_face_typed_empty_audit_sha256"]
        == "840a2c470df61e399d2ff89daf3875610602daeb431f24b5c8a5c1300b0c81c3",
        "Round122 physical audit digest",
    )
    require(
        ledger["child_stage_physical_audit_row_count"] == 72
        and ledger["physical_face_instance_count"] == 0,
        "Round122 72-row empty audit",
    )
    require(
        empty["rank3_candidate_occurrence_stage_counts"] == [57, 55, 57]
        and empty["rank3_candidate_occurrence_count_per_common_child"] == 169
        and empty["rank3_candidate_occurrence_total_check_count"] == 4056
        and empty["residual_physical_face_count"] == 0,
        "Round122 occurrence census",
    )
    moving = next(
        row for row in r122["physical_five_face_grammar_rows"]
        if row["kind"] == "moving_occurrence_face"
    )
    require(
        moving["actual_instance_count"] == 0
        and moving["rank3_candidate_occurrence_total_check_count"] == 4056,
        "Round122 moving-face empty row",
    )
    require(
        r133["count_ledger"][
            "certified_or_materialized_Round67_owned_Omega_j_record_count"
        ] == 0
        and r133["count_ledger"]["owner_key_count"] == 0
        and r133["count_ledger"]["q_j_recordwise_output_count"] == 0,
        "Round133 owner frontier",
    )

    result = {
        "provenance": {
            "producer_sha256_filled_after_write": True,
            "dependency_sha256": dict(BYTE_PINS),
            "old_artifacts_modified": False,
            "precision_bits": PRECISION_BITS,
        },
        "Round132_to_Round113_typed_crosswalk": {
            "Round132_occurrence_record_count": len(mapping),
            "Round132_occurrence_record_source_target_epsilon_map_sha256":
                OCCURRENCE_MAP_SHA256,
            "source_G_compatible_record_count": 44,
            "source_W_type_mismatch_record_count": 20,
            "source_G_unique_signed_target_sheet_count": len(signed_rows),
            "source_G_unique_signed_target_sheets": signed_rows,
            "source_G_unique_signed_target_sheets_sha256": SIGNED_SHEETS_SHA256,
            "source_G_unique_target_lift_count": len(targets),
            "source_G_unique_target_lifts": targets,
            "source_G_unique_target_lifts_sha256": TARGET_LIFTS_SHA256,
            "Round122_itself_typed_joined_Round28_occurrence_IDs": False,
            "Round134_installs_the_missing_Round28_ID_to_exact_seed_target_crosswalk":
                True,
        },
        "whole_Round113_rectangle_discriminant_audit": {
            "parent_round113_cell_id": PARENT_CELL_ID,
            "exact_parent_W_seed_id": EXACT_PARENT_ID,
            "source_type": "G",
            "source_normal_chart": "W",
            "parameter_box": cell["parameter_box"],
            "implicit_t_root_enclosure": cell["implicit_t_root_enclosure"],
            "system_parameter_interval": ["-1/400", "1/400"],
            "precision_bits": PRECISION_BITS,
            "target_lift_row_count": len(delta_rows),
            "target_lift_rows": delta_rows,
            "target_lift_rows_sha256": digest(delta_rows),
            "strict_positive_discriminant_target_count": 2,
            "strict_negative_discriminant_target_count": 10,
            "zero_discriminant_target_count": 0,
            "uniform_absolute_discriminant_strict_lower": "1/100",
            "tightest_target_lift": "W[-1,0]",
            "tightest_outward_discriminant_enclosure":
                ["-374189179/25000000000", "-101296291/7812500000"],
            "interpretation":
                "positive means two transverse line intersections and negative means whole-line miss; neither is a tangency root",
            "exact_seed_Round28_moving_occurrence_root_count": 0,
            "status": "CERTIFIED_EMPTY",
        },
        "Round122_crosscheck": {
            "strict_scope": r122["strict_scope"],
            "common_child_count": ledger["common_refinement_actual_child_count"],
            "child_stage_physical_audit_row_count":
                ledger["child_stage_physical_audit_row_count"],
            "candidate_occurrence_stage_counts":
                empty["rank3_candidate_occurrence_stage_counts"],
            "candidate_occurrence_count_per_common_child":
                empty["rank3_candidate_occurrence_count_per_common_child"],
            "candidate_occurrence_total_check_count":
                empty["rank3_candidate_occurrence_total_check_count"],
            "seven_physical_boundary_kinds_all_checked":
                ledger["physical_seven_boundary_kind_count"] == 7,
            "physical_face_instance_count": ledger["physical_face_instance_count"],
            "residual_physical_face_count": empty["residual_physical_face_count"],
            "physical_face_empty_audit_sha256":
                r122["physical_face_typed_empty_audit_sha256"],
            "status": "CERTIFIED_EMPTY",
        },
        "Round75_type_check": {
            "physical_R2_component_count": r75["physical_R2_component_count"],
            "physical_R2_curve_count": r75["physical_R2_curve_count"],
            "actual_carrier_type":
                "stationary destination-core t/p boundary preimage crosscuts",
            "requested_carrier_type":
                "moving occurrence pullback family at an active transverse tangency root",
            "carrier_types_match": False,
            "stationary_terminal_preimage_may_replace_occurrence_pullback": False,
            "status": "REJECTED_TYPE_MISMATCH",
        },
        "feasibility_frontier": {
            "Round121_exact_seed_Round28_occurrence_incidence":
                "CERTIFIED_EMPTY",
            "Round75_as_Round28_occurrence_parent":
                "REJECTED_TYPE_MISMATCH",
            "actual_nonempty_n_ge_2_occurrence_pullback_elsewhere":
                "UNKNOWN_NOT_CERTIFIED",
            "first_unpaid_construction_elsewhere":
                "materialize a genuine fixed-s n>=2 parent-W/path component crossing one Round28 moving-occurrence graph, then enumerate the complete primitive-free active fibre",
            "tailored_analytic_leaf_through_a_face_witness_is_by_itself_a_component":
                False,
            "parameter-s hit/miss germ_may_replace_fixed-s_plaque-side_path_proof":
                False,
            "stationary_terminal_preimage_curve_may_replace_occurrence_pullback":
                False,
        },
        "materialization_ledger": {
            "new_nonempty_occurrence_pullback_return_component_count": 0,
            "new_rank_zero_occurrence_component_count": 0,
            "new_complete_active_primitive_fibre_count": 0,
            "new_owner_key_count": 0,
            "new_q_j_recordwise_output_count": 0,
            "new_Round67_owned_Omega_j_record_count": 0,
            "new_global_complete_18_field_block_count": 0,
        },
        "global_safety": {
            "gate5_global_maturity": "10/18",
            "global_complete_18_field_block_count": 0,
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "strict_nonclaims": [
            "the exact-seed empty result is not a global absence theorem",
            "actual n>=2 occurrence incidence elsewhere is UNKNOWN_NOT_CERTIFIED, not empty",
            "the 32 Round75 stationary terminal-preimage curves are not occurrence pullbacks",
            "a positive line discriminant is not a tangency root",
            "no Round67 owner key, q_j output, positive owner law or Gate5 field is promoted",
        ],
    }
    return result


def safe_output_path(path: Path) -> Path:
    expanded = path.expanduser()
    protected = {PRODUCER.resolve(), *((HERE / item.name).resolve() for item in INPUTS)}
    require(not expanded.is_symlink(), "output must not be a symlink")
    if expanded.exists():
        metadata = expanded.lstat()
        require(stat.S_ISREG(metadata.st_mode), "existing output must be regular")
        require(metadata.st_nlink == 1, "existing output must not have hardlinks")
        for item in protected:
            try:
                require(not os.path.samefile(expanded, item), "output aliases input")
            except FileNotFoundError:
                pass
    resolved = expanded.resolve()
    require(resolved not in protected, "output overwrites protected input")
    require(resolved.parent.is_dir(), "output parent")
    return resolved


def write_document(path: Path, document: dict[str, Any]) -> None:
    payload = json.dumps(
        document,
        sort_keys=True,
        indent=2,
        ensure_ascii=False,
        allow_nan=False,
    ) + "\n"
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.tmp-",
        dir=path.parent,
        text=True,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    try:
        result = build_result()
        document = {
            "schema": SCHEMA,
            "result": result,
            "result_sha256": digest(result),
        }
        output = safe_output_path(args.output)
        write_document(output, document)
        print(canonical({
            "output": str(output),
            "result_sha256": document["result_sha256"],
            "status": "PASS",
        }))
        return 0
    except (OSError, ValueError, VerificationError) as exc:
        print(f"{type(exc).__name__}: {exc}", file=os.sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
