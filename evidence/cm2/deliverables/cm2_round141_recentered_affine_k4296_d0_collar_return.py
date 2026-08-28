#!/usr/bin/env python3
"""Round141: recentered-affine enlargement of the Round139 D0 collar.

The exact fixed-s, slope-four leaf is parameterized by intrinsic H1 arclength

    z = x - x_star in [-2^-4296, 0].

A second generator retains the certified Round139 D0-root enclosure.  At
every collision the physical state is represented by a point center, two
affine generators, and four rigorous scalar remainders.  A full interval
Jacobian on the current state enclosure propagates the remainder.  State
centers and affine coefficients are recentered to exact Arb midpoints after
every collision; every discarded ball radius is explicitly charged to the
new remainder.

All retained and radius-four owner decisions, official wall words, chart
decisions, homogeneity/incidence labels, and C24 return decisions are then
replayed on these rigorous state enclosures.  The collision-three D0 anchor
is excluded only by the same exact-leaf analytic argument as Round139.

This is a local fixed-leaf result.  It is not a historical maximal component,
Round35 restriction, short-cell or image-recut rank, and it does not promote
Gate5 or CM2.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import os
import stat
import sys
import tempfile
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import arb, ctx

import cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier as r139
import cm2_round141_centered_affine_d0_collar_spike as engine


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

HERE = Path(__file__).resolve().parent
OUTPUT = (
    HERE
    / "cm2-round141-recentered-affine-k4296-d0-collar-return-2026-07-24.json"
)
FUTURE_VERIFIER = (
    HERE
    / "cm2_round141_recentered_affine_k4296_d0_collar_return_verifier.py"
)
SCHEMA = "cm2.round141.recentered-affine-k4296-d0-collar-return.v1"
MINIMUM_PRECISION_BITS = 8192
SECONDARY_PRECISION_BITS = 12288
X_COLLAR_POWER = 4296
COORDINATE_OUTER_BITS = 6144
RETURN_DEPTH = 1648

ENGINE = HERE / "cm2_round141_centered_affine_d0_collar_spike.py"
ENGINE_SHA256 = "5656f33a4974b63124bda19c56716dccb7c52ad7840741668512795560007ef1"

R139_PRODUCER = (
    HERE / "cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier.py"
)
R139_CERTIFICATE = (
    HERE
    / "cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-2026-07-24.json"
)
R139_VERIFIER = (
    HERE
    / "cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier_verifier.py"
)
R139_VERIFICATION = (
    HERE
    / "cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-verification-2026-07-24.json"
)
R140_PRODUCER = (
    HERE / "cm2_round140_round35_parent_w_r1648_materialization_audit.py"
)
R140_CERTIFICATE = (
    HERE
    / "cm2-round140-round35-parent-w-r1648-materialization-audit-2026-07-24.json"
)
R140_VERIFIER = (
    HERE
    / "cm2_round140_round35_parent_w_r1648_materialization_audit_verifier.py"
)
R140_VERIFICATION = (
    HERE
    / "cm2-round140-round35-parent-w-r1648-materialization-audit-verification-2026-07-24.json"
)

PINS = {
    R139_PRODUCER.name:
        "462ffcb41ba24771ce655ddb3ad5f18d5a22c8d0cb443ec1791ea9272d3d512b",
    R139_CERTIFICATE.name:
        "64e91e6b1efcb2675982fbc453b08349b003c8be5b4d236f61e1392aaee045f0",
    R139_VERIFIER.name:
        "cb96e0e1a74abcac4254f20584bab6997edb8de69f0d979f1d65d4c3fdfadd09",
    R139_VERIFICATION.name:
        "57093537ae3f464e276da830ee5821ffbe3576278c71adbe111b22a128f3005f",
    R140_PRODUCER.name:
        "6329e0050f6727f8c0fa7d2a5052028645a375c5d59c51169e2ec81fb2ad7377",
    R140_CERTIFICATE.name:
        "bb6283e2fccba194b47f9aa174e85594560ba88062ed57d06651003744755a79",
    R140_VERIFIER.name:
        "9494a893edf8ed136a0150d3919690b6fe84d438aadc00e5bb278a7b6ba6069e",
    R140_VERIFICATION.name:
        "b38306fb85e4a8a27d0339d95ff9e7ee3eabea044239972c719c926e0891782d",
}

CLOSED = {
    R139_CERTIFICATE.name: (
        "cm2.round139.rank3-minus-d0-adjacent-h1-collar-return-frontier.v1",
        "6e8f54c34154ea5ba3c95d4e901bc643c020a0a42e180241ae9053bb24f42236",
    ),
    R139_VERIFICATION.name: (
        "cm2.round139.rank3-minus-d0-adjacent-h1-collar-return-frontier-verification.v1",
        "e96609b3ff1ba35c94e224c5d16897ed6d173fe69cc3cbf260ff85e5340165e1",
    ),
    R140_CERTIFICATE.name: (
        "cm2.round140.round35-parent-w-r1648-materialization-audit.v1",
        "7988f4c9588894ec964e2c6efec4dd07dd28d5011c0bf004ad73f99414534eed",
    ),
    R140_VERIFICATION.name: (
        "cm2.round140.round35-parent-w-r1648-materialization-audit-verification.v1",
        "9d898c0cea05069511732acd2be74f04d66f416d10f4ca72cd6e6bccf8b9cf33",
    ),
}


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
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qstr(value: Q | int) -> str:
    return r139.qstr(value)


def fixed_outer(value: arb, bits: int) -> tuple[Q, Q]:
    raw_lower, raw_upper = r139.lower.round136.arb_pair(value)
    scale = 2**bits
    fixed_lower = Q(r139.lower.floor_q(raw_lower * scale) - 1, scale)
    fixed_upper = Q(r139.lower.ceil_q(raw_upper * scale) + 1, scale)
    require(
        fixed_lower < fixed_upper
        and bool(value > r139.lower.aq(fixed_lower))
        and bool(value < r139.lower.aq(fixed_upper)),
        "fixed padded coordinate outer",
    )
    return fixed_lower, fixed_upper


def validate_dependencies() -> dict[str, dict[str, Any]]:
    require(sha256(ENGINE) == ENGINE_SHA256, "centered engine pin")
    documents: dict[str, dict[str, Any]] = {}
    for path in (
        R139_PRODUCER,
        R139_CERTIFICATE,
        R139_VERIFIER,
        R139_VERIFICATION,
        R140_PRODUCER,
        R140_CERTIFICATE,
        R140_VERIFIER,
        R140_VERIFICATION,
    ):
        require(sha256(path) == PINS[path.name], f"dependency pin:{path.name}")
        if path.name not in CLOSED:
            continue
        document = r139.strict_json(path)
        expected_schema, expected_result = CLOSED[path.name]
        require(
            document["schema"] == expected_schema
            and document["result_sha256"] == expected_result
            and digest(document["result"]) == expected_result,
            f"closed dependency:{path.name}",
        )
        documents[path.name] = document["result"]
    require(
        documents[R139_CERTIFICATE.name]["status"]
        == "CERTIFIED_MINUS_D0_ADJACENT_H1_COLLAR_STRICT_FIRST_RETURN"
        and documents[R139_VERIFICATION.name]["status"] == "PASS"
        and documents[R140_CERTIFICATE.name]["status"]
        == "CERTIFIED_MAXIMAL_LEGAL_ROUND35_PARENT_W_DATA_FROM_R1648"
        and documents[R140_VERIFICATION.name]["status"] == "PASS",
        "dependency statuses",
    )
    return documents


def leaf_domain_audit(
    r139_result: dict[str, Any],
    precision_bits: int,
) -> dict[str, Any]:
    r139.lower.round116.init_worker(precision_bits)
    nested = r139.lower.round136.validate_dependencies()
    source, _face, _link, strip = (
        r139.lower.round136.selected_corrected_objects(nested)
    )
    root = tuple(
        Q(value)
        for value in r139_result["deep_same_D0_root_and_b_star"][
            "deep_D0_root_bracket"
        ]
    )
    b_outer = tuple(
        Q(value)
        for value in r139_result["deep_same_D0_root_and_b_star"][
            "b_star_fixed_dyadic_outer"
        ]
    )
    ell = Q(1, 2**X_COLLAR_POWER)
    delta_r = r139.lower.aq(ell) / arb(17).sqrt()
    root_angle = r139.lower.interval(*root).asin()
    delta_r_half = delta_r / 2
    leaf_offset = arb(0, delta_r_half.upper()) - delta_r_half
    whole_angle = (
        root_angle
        + leaf_offset / r139.lower.aq(r139.lower.R_W)
    )
    t_ball = whole_angle.sin()
    p_ball = (
        r139.lower.aq(r139.lower.SOURCE_P_STAR).asin()
        + 4 * leaf_offset
    ).sin()
    t_outer = fixed_outer(t_ball, COORDINATE_OUTER_BITS)
    p_outer = fixed_outer(p_ball, COORDINATE_OUTER_BITS)
    require(
        strip[0] < t_outer[0] < t_outer[1] < strip[1]
        and strip[2] < p_outer[0] < p_outer[1] < strip[3]
        and source.t0 < t_outer[0] < t_outer[1] < source.t1
        and source.p0 < p_outer[0] < p_outer[1] < source.p1,
        "enlarged exact leaf enclosure contained",
    )
    far_t = (
        root_angle - delta_r / r139.lower.aq(r139.lower.R_W)
    ).sin()
    far_p = (
        r139.lower.aq(r139.lower.SOURCE_P_STAR).asin()
        - 4 * delta_r
    ).sin()
    far_t_outer = fixed_outer(far_t, COORDINATE_OUTER_BITS)
    far_p_outer = fixed_outer(far_p, COORDINATE_OUTER_BITS)
    far_D = r139.lower.third_tangency_jet(
        source,
        r139.lower.SECOND_OWNER,
        r139.ANCHOR,
        far_t_outer[0],
        far_t_outer[1],
        far_p_outer[0],
        far_p_outer[1],
    ).value
    require(bool(far_D < 0), "enlarged far endpoint D3 negative")
    graph_jet = r139.lower.third_tangency_jet(
        source,
        r139.lower.SECOND_OWNER,
        r139.ANCHOR,
        t_outer[0],
        t_outer[1],
        p_outer[0],
        p_outer[1],
    )
    t_interval = r139.lower.interval(*t_outer)
    p_interval = r139.lower.interval(*p_outer)
    dp_dt = (
        r139.lower.aq(r139.lower.KAPPA)
        * (1 - p_interval * p_interval).sqrt()
        / (1 - t_interval * t_interval).sqrt()
    )
    along = graph_jet.gradient[0] + graph_jet.gradient[1] * dp_dt
    require(bool(along > 0), "D3 monotone on enlarged leaf collar")
    return {
        "coordinate":
            "x=sqrt(17)*r, r=(4/25)*asin(t), fixed v=asin(p)-4r",
        "exact_parameter": f"z=x-x_star in [-2^-{X_COLLAR_POWER},0]",
        "exact_half_open_collar":
            f"[x_star-2^-{X_COLLAR_POWER},x_star)",
        "closed_model_domain_includes_endpoint": True,
        "root_generator_is_Round139_deep_D0_bracket": True,
        "root_bracket": [qstr(value) for value in root],
        "b_star_outer_cross_check": [qstr(value) for value in b_outer],
        "coordinate_outer_bits": COORDINATE_OUTER_BITS,
        "t_outer": [qstr(value) for value in t_outer],
        "p_outer": [qstr(value) for value in p_outer],
        "inside_Round116_strip": True,
        "inside_source_core": True,
        "far_t_outer": [qstr(value) for value in far_t_outer],
        "far_p_outer": [qstr(value) for value in far_p_outer],
        "far_D3_strict_negative": True,
        "far_D3_margin_dyadic_depth":
            r139.lower.round136.strict_dyadic_depth(-far_D),
        "D3_strictly_increasing_along_whole_leaf_collar": True,
        "D3_along_leaf_margin_dyadic_depth":
            r139.lower.round136.strict_dyadic_depth(along),
        "D3_negative_on_exact_half_open_collar": True,
        "only_D3_zero_endpoint": "x_star",
    }


def centered_replay_summary(precision_bits: int) -> dict[str, Any]:
    capture = io.StringIO()
    with contextlib.redirect_stdout(capture):
        engine.run(
            X_COLLAR_POWER,
            precision_bits,
            False,
            True,
            0,
        )
    lines = [
        line for line in capture.getvalue().splitlines()
        if line.startswith("{")
    ]
    require(len(lines) == 1, "one centered replay summary")
    summary = json.loads(lines[0])
    require(
        summary["status"] == "FEASIBLE"
        and summary["complete_audit"] is True
        and summary["collision_count"] == RETURN_DEPTH
        and summary["cell_index"] == 0
        and summary["official_sequence_sha256"]
        == r139.EXPECTED_OFFICIAL_SEQUENCE_SHA256
        and summary["compact_rows_sha256"]
        == r139.EXPECTED_COMPACT_PATH_SHA256
        and summary["homogeneity_histogram"] == {"H0_CENTRAL": RETURN_DEPTH}
        and summary["incidence_histogram"] == {"14": RETURN_DEPTH},
        "centered replay frozen path",
    )
    return summary


def build(precision_bits: int = MINIMUM_PRECISION_BITS) -> dict[str, Any]:
    require(
        type(precision_bits) is int
        and precision_bits >= MINIMUM_PRECISION_BITS,
        "producer precision below minimum",
    )
    ctx.prec = precision_bits
    closed = validate_dependencies()
    r139_result = closed[R139_CERTIFICATE.name]
    r140_result = closed[R140_CERTIFICATE.name]
    leaf = leaf_domain_audit(r139_result, precision_bits)
    replay = centered_replay_summary(precision_bits)
    require(
        replay["maximum_state_radius_strict_upper_power_of_two_exponent"]
        <= -14
        and replay["terminal_state_radius_strict_upper_power_of_two_exponents"]
        == [-17, -17, -14, -14],
        "frozen model radius envelope",
    )
    result = {
        "status":
            "CERTIFIED_RECENTERED_AFFINE_K4296_D0_COLLAR_STRICT_R1648_RETURN",
        "minimum_certified_precision_bits": MINIMUM_PRECISION_BITS,
        "secondary_verifier_precision_bits": SECONDARY_PRECISION_BITS,
        "provenance": {
            "producer_sha256": sha256(Path(__file__).resolve()),
            "centered_engine_sha256": ENGINE_SHA256,
            "direct_Round139_Round140_parent_W_sha256":
                dict(sorted(PINS.items())),
            "append_only": True,
            "Round139_files_modified": False,
            "Round140_files_modified": False,
        },
        "exact_fixed_leaf_domain": leaf,
        "recentered_affine_contract": {
            "parameter_generator_count": 2,
            "parameter_generators": [
                "intrinsic leaf z in [-2^-4296,0]",
                "Round139 certified D0-root bracket",
            ],
            "physical_state_dimension": 4,
            "state_representation": "center + A*xi + componentwise remainder",
            "local_derivative_enclosure":
                "full 4x4 interval Jacobian on current state box",
            "remainder_recurrence":
                "(J(X)-J(c))*A*xi + J(X)*remainder",
            "center_recenter_rule":
                "replace each output center by exact Arb midpoint and charge lost radius",
            "coefficient_recenter_rule":
                "replace each affine coefficient by exact Arb midpoint and charge lost radius times parameter radius",
            "center_recenter_loss_charged_at_every_stage": True,
            "coefficient_recenter_loss_charged_at_every_stage": True,
            "collision_stage_count": RETURN_DEPTH,
            "model_radius_ledger_row_count":
                replay["model_radius_ledger_row_count"],
            "model_radius_ledger_sha256":
                replay["model_radius_ledger_sha256"],
            "maximum_state_radius_strict_upper_power_of_two_exponent":
                replay[
                    "maximum_state_radius_strict_upper_power_of_two_exponent"
                ],
            "maximum_state_radius_witness":
                replay["maximum_state_radius_witness"],
            "terminal_state_radius_strict_upper_power_of_two_exponents":
                replay[
                    "terminal_state_radius_strict_upper_power_of_two_exponents"
                ],
        },
        "complete_decision_replay": {
            "return_depth": RETURN_DEPTH,
            "owner_sequence_sha256":
                r139.EXPECTED_OWNER_SEQUENCE_SHA256,
            "official_sequence_sha256":
                replay["official_sequence_sha256"],
            "compact_path_sha256": replay["compact_rows_sha256"],
            "retained_candidate_stage_count": RETURN_DEPTH,
            "full_radius4_candidate_stage_count": RETURN_DEPTH,
            "full_radius4_candidate_count_per_stage": 161,
            "full_radius4_candidate_test_count": 161 * RETURN_DEPTH,
            "collision3_D0_anchor_analytic_exclusion_count": 1,
            "all_nonanchor_candidate_decisions_strict": True,
            "all_owner_winner_gaps_strict": True,
            "all_official_wall_endpoint_and_order_decisions_strict": True,
            "all_outgoing_chart_decisions_strict": True,
            "homogeneity_histogram": replay["homogeneity_histogram"],
            "incidence_rank_histogram": replay["incidence_histogram"],
            "preterminal_strict_nonreturn_count": RETURN_DEPTH - 1,
            "terminal_strict_return_count": 1,
            "terminal_owner": r139.EXPECTED_TERMINAL_OWNER,
            "terminal_destination_core":
                r139.EXPECTED_DESTINATION_CORE_ID,
            "strict_margin_ledger": replay["strict_margin_ledger"],
            "worst_decision_margin_dyadic_depth":
                replay["ledger_worst_depth"],
            "worst_decision_margin_names":
                replay["ledger_worst_names"],
        },
        "terminal_phase_enclosure": {
            "fixed_dyadic_outer_bits":
                replay["terminal_phase_fixed_dyadic_outer_bits"],
            "normal_x":
                replay["terminal_normal_x_fixed_dyadic_outer"],
            "normal_y":
                replay["terminal_normal_y_fixed_dyadic_outer"],
            "p": replay["terminal_p_fixed_dyadic_outer"],
            "cosine":
                replay["terminal_cosine_fixed_dyadic_outer"],
            "strictly_inside_destination_core": True,
        },
        "width_upgrade": {
            "Round139_power": 5888,
            "Round141_power": X_COLLAR_POWER,
            "certified_width_factor_power_of_two": 5888 - X_COLLAR_POWER,
            "certified_width_factor": "2^1592",
            "same_D0_endpoint": True,
            "same_exact_slope4_leaf": True,
            "same_R1648_owner_and_official_word": True,
        },
        "Round140_parent_W_consistency": {
            "same_source_core_index":
                r140_result["materialized_source_core_path_tuple"][
                    "source_core_index"
                ],
            "same_return_depth":
                r140_result["materialized_source_core_path_tuple"][
                    "return_depth"
                ],
            "same_path_tuple_sha256":
                r140_result["materialized_source_core_path_tuple"][
                    "payload_sha256"
                ],
            "Round140_parent_W_input_pinned": True,
        },
        "strict_nonpromotion": {
            "historical_maximal_component_materialized": False,
            "historical_least_component_rank_materialized": False,
            "Round35_restriction_materialized": False,
            "natural_short_cell_k_materialized": False,
            "parent_W_id_materialized": False,
            "image_recut_rank_materialized": False,
            "Round50_owner_materialized": False,
            "Round54_token_materialized": False,
            "Round67_q_j_materialized": False,
            "Gate5": "NOT_CERTIFIED",
            "global_gate5_maturity": "10/18",
            "global_complete_18_field_block_count": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "strict_nonclaims": [
            "the D0 endpoint is used only as an analytic boundary and is not claimed as a regular billiard trajectory",
            "this fixed-leaf collar is not a historical maximal component or a proof of historical least rank",
            "the local state-radius and decision margins are not identified with global H1 component separation",
            "no natural 1e-90 short-cell, parent-W ID, image-recut rank or Round35 restriction is materialized",
            "Gate5 remains 10/18 with zero complete blocks and CM2 remains NO-GO_FOR_CLAIM",
        ],
    }
    require(
        result["strict_nonpromotion"]["global_gate5_maturity"] == "10/18"
        and result["strict_nonpromotion"][
            "global_complete_18_field_block_count"
        ] == 0
        and result["strict_nonpromotion"]["CM2"] == "NO-GO_FOR_CLAIM",
        "final nonpromotion",
    )
    result = json.loads(json.dumps(result, sort_keys=True))
    return {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def protected_paths() -> set[Path]:
    return {
        Path(__file__).resolve(),
        FUTURE_VERIFIER.resolve(),
        ENGINE.resolve(),
        *((HERE / name).resolve() for name in PINS),
    }


def validate_output_target(path: Path) -> Path:
    absolute = path.absolute()
    parent = absolute.parent
    require(
        absolute.name not in {"", ".", ".."}
        and parent.exists()
        and parent.is_dir()
        and not parent.is_symlink()
        and parent.resolve() == parent,
        "safe output parent",
    )
    require(not absolute.is_symlink(), "output symlink")
    resolved = absolute.resolve(strict=False)
    require(resolved not in protected_paths(), "output aliases input")
    if absolute.exists():
        metadata = absolute.lstat()
        require(
            stat.S_ISREG(metadata.st_mode) and metadata.st_nlink == 1,
            "safe existing output",
        )
        require(
            all(
                not os.path.samefile(absolute, item)
                for item in protected_paths()
                if item.exists()
            ),
            "output hardlink aliases input",
        )
    return resolved


def atomic_write(path: Path, payload: str) -> None:
    target = validate_output_target(path)
    descriptor, temporary = tempfile.mkstemp(
        prefix=f".{target.name}.",
        suffix=".tmp",
        dir=target.parent,
        text=True,
    )
    temporary_path = Path(temporary)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, target)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument(
        "--precision-bits",
        type=int,
        default=MINIMUM_PRECISION_BITS,
    )
    args = parser.parse_args()
    document = build(args.precision_bits)
    payload = json.dumps(
        document,
        sort_keys=True,
        indent=2,
        ensure_ascii=False,
        allow_nan=False,
    ) + "\n"
    atomic_write(args.output, payload)
    print(json.dumps({
        "schema": document["schema"],
        "result_sha256": document["result_sha256"],
        "output": str(args.output),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
