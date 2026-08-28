#!/usr/bin/env python3
"""Round145 feasibility wrapper for translated and clipped leaf cells.

Round141's engine deliberately treats collision three as a D0 double-root
boundary audit.  That is correct only for the cell touching ``x_star``.
Translated cells lie strictly to its left, where D0 is an ordinary strict
miss.  This wrapper changes only that audit dispatch and leaves the frozen
recentered-affine propagation unchanged.

The file is a feasibility tool, not a certificate.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from fractions import Fraction as Q

from flint import arb, ctx

import cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier as r139
import cm2_round141_centered_affine_d0_collar_spike as engine
import cm2_round143_r1648_terminal_face_endpoint_recut_frontier as endpoint


ORIGINAL_ANCHOR_AUDIT = r139.candidates_owner_excluding_anchor
ORIGINAL_INITIAL_MODEL = engine.initial_model
RETURN_DEPTH = 1648


def terminal_derivative_audit(
    lambda_lower: Q,
    lambda_upper: Q,
    precision: int,
) -> dict[str, object]:
    """Enclose terminal p and image-observable derivatives on one cell."""

    ctx.prec = precision
    document = json.loads(engine.R139_CERTIFICATE.read_text(encoding="utf-8"))
    result = document["result"]
    owners = [
        row["selected_absolute_owner_id"]
        for row in result["collision_rows"]
    ]
    t_star = tuple(
        Q(value)
        for value in result["deep_same_D0_root_and_b_star"][
            "deep_D0_root_bracket"
        ]
    )
    model, sensitivity = endpoint.initial_model(
        (lambda_lower, lambda_upper),
        t_star,
    )
    for expected in owners:
        model, sensitivity = endpoint.step_model(
            model, sensitivity, expected
        )
    boxes = model.boxes()
    variables = [
        endpoint.Dual(
            boxes[index],
            [arb(int(index == column)) for column in range(4)],
        )
        for index in range(4)
    ]
    center, radius = endpoint.target_geometry(r139.EXPECTED_TERMINAL_OWNER)
    t = (variables[0] - center[0]) / radius
    ny = (variables[1] - center[1]) / radius
    p = -variables[2] * ny + variables[3] * t
    if r139.lower.time3.time2_cert.strict_chart(t.value, ny.value) != "S":
        raise RuntimeError("terminal derivative S chart")
    t_gradient = [
        sum(
            t.gradient[inner] * sensitivity[inner][column]
            for inner in range(4)
        )
        for column in range(2)
    ]
    p_gradient = [
        sum(
            p.gradient[inner] * sensitivity[inner][column]
            for inner in range(4)
        )
        for column in range(2)
    ]
    t_denominator = (1 - t.value * t.value).sqrt()
    p_denominator = (1 - p.value * p.value).sqrt()
    image_gradient = [
        t_gradient[column] / t_denominator
        + p_gradient[column] / p_denominator
        for column in range(2)
    ]
    if not bool(p_gradient[0] < 0):
        raise RuntimeError(f"terminal p derivative sign:{p_gradient[0]}")
    if not bool(image_gradient[0] < 0):
        raise RuntimeError(
            f"terminal image derivative sign:{image_gradient[0]}"
        )
    return {
        "lambda_bounds": [r139.qstr(lambda_lower), r139.qstr(lambda_upper)],
        "terminal_p_derivative_lambda_sign": -1,
        "terminal_p_derivative_lambda_margin_dyadic_depth":
            r139.lower.round136.strict_dyadic_depth(-p_gradient[0]),
        "terminal_image_observable":
            "asin(t_1648)+asin(p_1648)",
        "terminal_image_derivative_lambda_sign": -1,
        "terminal_image_derivative_lambda_margin_dyadic_depth":
            r139.lower.round136.strict_dyadic_depth(-image_gradient[0]),
        "terminal_t_strictly_inside_asin_domain":
            bool(t.value > -1) and bool(t.value < 1),
        "terminal_p_strictly_inside_asin_domain":
            bool(p.value > -1) and bool(p.value < 1),
    }


def translated_anchor_audit():
    retained_owner: dict[str, object] = {}

    def audit(
        state,
        current_target,
        _candidates,
        ledger,
        collision_index,
        full_radius4,
    ):
        if not full_radius4:
            owner, row = r139.lower.round136.complete_owner(
                state, current_target, ledger, collision_index
            )
            retained_owner.clear()
            retained_owner.update(owner)
            return owner, row
        if not retained_owner:
            raise RuntimeError("missing translated retained owner")
        row = r139.lower.full_radius4_candidate_audit(
            state,
            current_target,
            retained_owner,
            ledger,
            collision_index,
        )
        return dict(retained_owner), row

    return audit


def arbitrary_initial_model(
    lambda_lower: Q,
    lambda_upper: Q,
    scale_power: int,
):
    if not Q(0) <= lambda_lower < lambda_upper:
        raise RuntimeError("ordered nonnegative lambda interval")

    def build(_power: int, root: tuple[Q, Q], _cell_index: int):
        scale = r139.lower.aq(Q(1, 2**scale_power))
        z_lower = -r139.lower.aq(lambda_upper) * scale
        z_upper = -r139.lower.aq(lambda_lower) * scale
        z_center = (z_lower + z_upper) / 2
        z_radius = (z_upper - z_lower) / 2
        root_lower, root_upper = map(r139.lower.aq, root)
        root_center = (root_lower + root_upper) / 2
        root_radius = (root_upper - root_lower) / 2
        center_inputs = (
            engine.Dual(z_center, [arb(1), arb(0)]),
            engine.Dual(root_center, [arb(0), arb(1)]),
        )
        interval_inputs = (
            engine.Dual(
                z_center + engine.symmetric(z_radius),
                [arb(1), arb(0)],
            ),
            engine.Dual(
                root_center + engine.symmetric(root_radius),
                [arb(0), arb(1)],
            ),
        )
        center_values = engine.initial_state(*center_inputs)
        interval_values = engine.initial_state(*interval_inputs)
        raw_affine = engine.rows(center_values)
        affine = [
            [engine.point(entry) for entry in row]
            for row in raw_affine
        ]
        interval_derivatives = engine.rows(interval_values)
        domain_radii = (z_radius, root_radius)
        remainders = [
            (
                center_values[row].value
                - engine.point(center_values[row].value)
            ).abs_upper()
            + sum(
                (
                    raw_affine[row][column] - affine[row][column]
                ).abs_upper()
                * domain_radii[column]
                for column in range(2)
            )
            + sum(
                (
                    interval_derivatives[row][column]
                    - raw_affine[row][column]
                ).abs_upper()
                * domain_radii[column]
                for column in range(2)
            )
            for row in range(4)
        ]
        return engine.Model(
            [engine.point(value.value) for value in center_values],
            affine,
            remainders,
            domain_radii,
        )

    return build


def endpoint_complete_audit(
    lambda_lower: Q,
    lambda_upper: Q,
    scale_power: int,
    precision: int,
) -> None:
    """Audit a cell crossing only the terminal C24 p=-1/50 face."""

    ctx.prec = precision
    document = json.loads(engine.R139_CERTIFICATE.read_text(encoding="utf-8"))
    result = document["result"]
    owners = [
        row["selected_absolute_owner_id"]
        for row in result["collision_rows"]
    ]
    root = tuple(
        Q(value)
        for value in result["deep_same_D0_root_and_b_star"][
            "deep_D0_root_bracket"
        ]
    )
    model = arbitrary_initial_model(
        lambda_lower,
        lambda_upper,
        scale_power,
    )(scale_power, root, 1)
    ledger = engine.AuditLedger()
    current_target = r139.lower.SOURCE_ABSOLUTE_OWNER
    current_chart = "E"
    cores = tuple(r139.lower.core_cert.physical_cores())
    pair_index, pattern_index, registry_sha = (
        r139.lower.component_cert.key_index_tables()
    )
    if registry_sha != r139.OFFICIAL_REGISTRY_SHA256:
        raise RuntimeError("official registry digest")
    initial_boxes = model.boxes()
    source_center, source_radius = engine.target_geometry(current_target)
    initial_nx = (initial_boxes[0] - source_center[0]) / source_radius
    initial_ny = (initial_boxes[1] - source_center[1]) / source_radius
    initial_p = (
        -initial_boxes[2] * initial_ny
        + initial_boxes[3] * initial_nx
    )
    previous_cosine = (1 - initial_p * initial_p).sqrt()
    official_ids: list[str] = []
    raw_compact_rows: list[list[object]] = []
    interior_compact_rows: list[list[object]] = []
    homogeneity_labels: list[str] = []
    incidence_ranks: list[int] = []
    model_radius_rows: list[list[object]] = []
    maximum_radius = arb(0)
    maximum_witness: list[int | None] | None = None
    terminal_phase: dict[str, object] | None = None
    for collision_index, expected_owner in enumerate(owners, start=1):
        incoming_target = current_target
        boxes = model.boxes()
        for component, radius in enumerate(model.radii()):
            if bool(radius > maximum_radius):
                maximum_radius = radius.abs_upper()
                maximum_witness = [
                    collision_index - 1,
                    component,
                    engine.strict_upper_power_of_two_exponent(radius),
                ]
        state = {
            "contact_x": boxes[0],
            "contact_y": boxes[1],
            "outgoing_x": boxes[2],
            "outgoing_y": boxes[3],
            "s": arb(0),
            "chart": current_chart,
        }
        owner, _retained = r139.lower.round136.complete_owner(
            state, current_target, ledger, collision_index
        )
        _full = r139.lower.full_radius4_candidate_audit(
            state, current_target, owner, ledger, collision_index
        )
        if owner["selected_target_id"] != expected_owner:
            raise RuntimeError(f"endpoint owner:{collision_index}")
        word, error = (
            r139.lower.round136.translation_normalized_official_word(
                state,
                current_target,
                owner,
                pair_index,
                pattern_index,
            )
        )
        if word is None or error is not None:
            raise RuntimeError(f"endpoint official word:{collision_index}:{error}")
        r139.official_wall_margin_audit(
            state, current_target, owner, ledger, collision_index
        )
        model, step_audit = engine.step_model_with_audit(
            model, expected_owner
        )
        for component, radius in enumerate(
            step_audit["output_state_radii"]
        ):
            if bool(radius > maximum_radius):
                maximum_radius = radius.abs_upper()
                maximum_witness = [
                    collision_index,
                    component,
                    engine.strict_upper_power_of_two_exponent(radius),
                ]
        model_radius_rows.append([
            collision_index,
            engine.vector_upper_exponents(
                step_audit["input_affine_radii"]
            ),
            engine.vector_upper_exponents(
                step_audit["input_remainders"]
            ),
            engine.vector_upper_exponents(
                step_audit["input_state_radii"]
            ),
            engine.vector_upper_exponents(
                step_audit["raw_propagated_remainders"]
            ),
            engine.vector_upper_exponents(
                step_audit["center_recenter_losses"]
            ),
            engine.vector_upper_exponents(
                step_audit["coefficient_recenter_losses"]
            ),
            engine.vector_upper_exponents(
                step_audit["output_affine_radii"]
            ),
            engine.vector_upper_exponents(
                step_audit["output_remainders"]
            ),
            engine.vector_upper_exponents(
                step_audit["output_state_radii"]
            ),
        ])
        current_target = expected_owner
        current_chart, phase = engine.chart_and_owner_state(
            model, current_target
        )
        if not bool(phase["cosine"] > 0):
            raise RuntimeError(f"endpoint cosine:{collision_index}")
        certified_owner = {
            **phase,
            "selected_target_id": expected_owner,
            "selected_root": owner["selected_root"],
        }
        classification, destination, _witnesses = (
            r139.lower.time3.core_classification(
                certified_owner, cores
            )
        )
        if collision_index < RETURN_DEPTH:
            if (
                classification != "SURVIVE_THROUGH_3_INNER"
                or destination is not None
            ):
                raise RuntimeError(f"endpoint preterminal:{collision_index}")
            r139.lower.round136.core_margin(
                certified_owner,
                classification,
                destination,
                cores,
                ledger,
            )
        else:
            if (
                classification != "UNRESOLVED_TIME3_OUTER"
                or destination is not None
            ):
                raise RuntimeError(
                    f"endpoint terminal:{classification}:{destination}"
                )
            if not (
                bool(phase["p"] < r139.lower.aq(Q(1, 50)))
                and bool(phase["p"] > r139.lower.aq(Q(-3, 100)))
                and bool(phase["p"] < r139.lower.aq(Q(-1, 50)))
                is False
                and bool(phase["p"] > r139.lower.aq(Q(-1, 50)))
                is False
                and bool(
                    phase["normal_x"] > r139.lower.aq(Q(69, 100))
                )
                and bool(
                    phase["normal_x"] < r139.lower.aq(Q(7, 10))
                )
            ):
                raise RuntimeError("endpoint unique terminal face window")
            terminal_phase = phase
        label, _label_audit = r139.lower.generic_homogeneity_label(
            collision_index, phase["cosine"], ledger
        )
        source_rank = r139.lower.round136.capped_reciprocal_cosine_rank(
            previous_cosine,
            ledger,
            collision_index,
            "source",
        )
        target_rank = r139.lower.round136.capped_reciprocal_cosine_rank(
            phase["cosine"],
            ledger,
            collision_index,
            "target",
        )
        incidence = max(14, source_rank, target_rank)
        r139.lower.round136.chart_margin(
            {
                "chart": current_chart,
                "normal_x": phase["normal_x"],
                "normal_y": phase["normal_y"],
            },
            ledger,
        )
        compact_key = r139.lower.round136.compact_key(word["key"])
        official_id = compact_key["official_word_key_id"]
        official_ids.append(official_id)
        raw_row = [
            collision_index,
            incoming_target,
            expected_owner,
            official_id,
            label,
            incidence,
            classification,
            destination,
        ]
        raw_compact_rows.append(raw_row)
        interior_compact_rows.append(
            raw_row
            if collision_index < RETURN_DEPTH
            else [
                collision_index,
                incoming_target,
                expected_owner,
                official_id,
                label,
                incidence,
                "RETURN_AT_3_INNER",
                r139.EXPECTED_DESTINATION_CORE_ID,
            ]
        )
        homogeneity_labels.append(label)
        incidence_ranks.append(incidence)
        previous_cosine = phase["cosine"]
        if collision_index % 100 == 0 or collision_index == RETURN_DEPTH:
            print(
                collision_index,
                current_target,
                current_chart,
                flush=True,
            )
    if terminal_phase is None:
        raise RuntimeError("endpoint terminal phase missing")
    if (
        engine.digest(official_ids)
        != r139.EXPECTED_OFFICIAL_SEQUENCE_SHA256
        or engine.digest(interior_compact_rows)
        != r139.EXPECTED_COMPACT_PATH_SHA256
        or Counter(homogeneity_labels) != Counter({"H0_CENTRAL": RETURN_DEPTH})
        or Counter(incidence_ranks) != Counter({14: RETURN_DEPTH})
    ):
        raise RuntimeError("endpoint frozen path identities")
    print(json.dumps({
        "status": "FEASIBLE_ENDPOINT_FACE_CELL",
        "lambda_bounds": [
            r139.qstr(lambda_lower),
            r139.qstr(lambda_upper),
        ],
        "lambda_scale_power": scale_power,
        "precision": precision,
        "collision_count": RETURN_DEPTH,
        "complete_audit": True,
        "ordinary_D0_strict_miss": True,
        "full_radius4_candidate_test_count": 161 * RETURN_DEPTH,
        "official_sequence_sha256": engine.digest(official_ids),
        "raw_box_compact_rows_sha256": engine.digest(raw_compact_rows),
        "physical_interior_compact_rows_sha256":
            engine.digest(interior_compact_rows),
        "homogeneity_histogram": dict(Counter(homogeneity_labels)),
        "incidence_histogram": dict(Counter(incidence_ranks)),
        "preterminal_strict_nonreturn_count": RETURN_DEPTH - 1,
        "terminal_box_classification": "UNRESOLVED_TIME3_OUTER",
        "terminal_only_active_face": "p=-1/50",
        "maximum_state_radius_strict_upper_power_of_two_exponent":
            engine.strict_upper_power_of_two_exponent(maximum_radius),
        "maximum_state_radius_witness": maximum_witness,
        "terminal_state_radius_strict_upper_power_of_two_exponents":
            engine.vector_upper_exponents(model.radii()),
        "model_radius_ledger_row_count": len(model_radius_rows),
        "model_radius_ledger_sha256": engine.digest(model_radius_rows),
        "ledger_worst_depth": max(ledger.depths.values()),
        "ledger_worst_names": sorted(
            name
            for name, depth in ledger.depths.items()
            if depth == max(ledger.depths.values())
        ),
        "terminal_p_fixed_dyadic_outer": [
            r139.qstr(value)
            for value in engine.fixed_padded_outer(
                terminal_phase["p"], 128
            )
        ],
        "terminal_normal_y_fixed_dyadic_outer": [
            r139.qstr(value)
            for value in engine.fixed_padded_outer(
                terminal_phase["normal_y"], 128
            )
        ],
        "terminal_normal_x_fixed_dyadic_outer": [
            r139.qstr(value)
            for value in engine.fixed_padded_outer(
                terminal_phase["normal_x"], 128
            )
        ],
    }, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cell-index", type=int)
    parser.add_argument("--power", type=int, default=4292)
    parser.add_argument("--lambda-lower")
    parser.add_argument("--lambda-upper")
    parser.add_argument("--scale-power", type=int, default=4289)
    parser.add_argument("--precision", type=int, default=8192)
    parser.add_argument("--audit-candidates", action="store_true")
    parser.add_argument("--audit-all", action="store_true")
    parser.add_argument("--endpoint-complete-audit", action="store_true")
    args = parser.parse_args()
    if args.cell_index is not None:
        if args.lambda_lower is not None or args.lambda_upper is not None:
            raise RuntimeError("choose translated or arbitrary cell")
        power = args.power
        cell_index = args.cell_index
    else:
        if args.lambda_lower is None or args.lambda_upper is None:
            raise RuntimeError("both lambda bounds required")
        engine.initial_model = arbitrary_initial_model(
            Q(args.lambda_lower),
            Q(args.lambda_upper),
            args.scale_power,
        )
        power = args.scale_power
        cell_index = 1
    if args.endpoint_complete_audit:
        if args.cell_index is not None:
            raise RuntimeError("endpoint audit needs lambda bounds")
        endpoint_complete_audit(
            Q(args.lambda_lower),
            Q(args.lambda_upper),
            args.scale_power,
            args.precision,
        )
        return
    if cell_index > 0:
        r139.candidates_owner_excluding_anchor = translated_anchor_audit()
    try:
        engine.run(
            power,
            args.precision,
            args.audit_candidates,
            args.audit_all,
            cell_index,
        )
    finally:
        r139.candidates_owner_excluding_anchor = ORIGINAL_ANCHOR_AUDIT
        engine.initial_model = ORIGINAL_INITIAL_MODEL


if __name__ == "__main__":
    main()
