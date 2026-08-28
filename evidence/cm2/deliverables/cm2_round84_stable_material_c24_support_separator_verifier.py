#!/usr/bin/env python3
"""Independent verifier for the Round-84 stable/material-to-C24 separator."""
from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any, Iterable

import cm2_round84_stable_material_c24_support_separator_cert as certificate
from cm2_round79_tangency_intersection_generator import digest


HERE = Path(__file__).resolve().parent
DEFAULT_INPUT = HERE / "cm2-round84-stable-material-c24-support-separator-2026-07-22.json"
VERIFY_PRECISION_BITS = 2700


class VerificationError(RuntimeError):
    pass


def reject_constant(token: str) -> None:
    raise VerificationError(f"non-finite JSON constant: {token}")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise VerificationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_nonfinite(value: Any) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise VerificationError("non-finite JSON number")
    if isinstance(value, dict):
        for child in value.values():
            reject_nonfinite(child)
    elif isinstance(value, list):
        for child in value:
            reject_nonfinite(child)


def loads_strict(raw: str) -> Any:
    value = json.loads(
        raw,
        object_pairs_hook=unique_object,
        parse_constant=reject_constant,
    )
    reject_nonfinite(value)
    return value


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def validate_document(document: Any, expected: dict[str, Any]) -> None:
    require(isinstance(document, dict), "top-level object")
    require(
        set(document) == {"schema", "pins", "result", "result_sha256"},
        "closed top-level schema",
    )
    require(document["schema"] == expected["schema"], "schema identifier")
    require(isinstance(document["pins"], dict), "pins object")
    require(isinstance(document["result"], dict), "result object")
    result = document["result"]
    require(document["result_sha256"] == digest(result), "result digest")
    require(result.get("state_rows_sha256") == digest(result.get("state_rows")), "state row digest")
    require(
        result.get("comparison_rows_sha256") == digest(result.get("comparison_rows")),
        "comparison row digest",
    )
    # This equality binds every scalar, row, pin, nonclaim, count, and status to a
    # fresh producer reconstruction.  It also makes all nested schemas closed.
    require(document == expected, "fresh reconstruction equality")


def arb_fraction(module: Any, value: Any) -> Any:
    return module.arb(value.numerator) / value.denominator


def coordinate_gaps(module: Any, t_value: Any, p_value: Any, core: Any) -> dict[str, Any]:
    return {
        "t_below": arb_fraction(module, core.t0) - t_value,
        "t_above": t_value - arb_fraction(module, core.t1),
        "p_below": arb_fraction(module, core.p0) - p_value,
        "p_above": p_value - arb_fraction(module, core.p1),
    }


def check_dihedral_group() -> None:
    matrices = certificate.symmetry.MATRICES
    require(len(matrices) == 8, "D4 action count")
    tuples = {tuple(matrix) for matrix in matrices.values()}
    require(len(tuples) == 8, "D4 actions unique")
    for matrix in tuples:
        require(len(matrix) == 4, "2x2 action shape")
        a, b, c, d = matrix
        require(a * a + c * c == 1, "D4 first column unit")
        require(b * b + d * d == 1, "D4 second column unit")
        require(a * b + c * d == 0, "D4 columns orthogonal")
        require(abs(a * d - b * c) == 1, "D4 determinant")
    for left in tuples:
        a, b, c, d = left
        for right in tuples:
            e, f, g, h = right
            product = (a * e + b * g, a * f + b * h, c * e + d * g, c * f + d * h)
            require(product in tuples, "D4 closure")


def independent_separator_recomputation(document: dict[str, Any]) -> dict[str, Any]:
    result = document["result"]
    module = certificate.plaque.load(
        certificate.plaque.TANGENT_CERT,
        "cm2_round84_separator_verifier_tangent",
    ).load_frozen_certificate()
    module.ctx.prec = VERIFY_PRECISION_BITS
    cores = certificate.core_cert.physical_cores()
    state_rows = result["state_rows"]
    comparison_rows = result["comparison_rows"]
    require(len(state_rows) == 97, "independent state count")
    require(len(cores) == 24, "independent C24 core count")
    require(len(comparison_rows) == 8 * 97 * 24, "independent comparison count")
    check_dihedral_group()

    tube_threshold = arb_fraction(module, certificate.TUBE_GAP_LOWER)
    center_threshold = arb_fraction(module, certificate.CENTER_GAP_LOWER)
    radius_threshold = arb_fraction(module, certificate.TUBE_RADIUS_UPPER)
    categorical = numeric = certified = 0
    row_index = 0
    maximum_radius = module.arb(0)
    minimum_tube = None
    minimum_center = None

    state_keys = {
        "state_rank", "source_component", "next_target", "theta_center",
        "momentum_center", "theta_radius", "momentum_radius", "cumulative_lift",
    }
    categorical_keys = {"state_rank", "symmetry", "core_index", "status"}
    numeric_keys = categorical_keys | {"separator"}

    for expected_rank, state in enumerate(state_rows):
        require(set(state) == state_keys, "closed state-row schema")
        require(state["state_rank"] == expected_rank, "state-rank enumeration")
        require(state["source_component"] in {core.source for core in cores}, "state component")
        require(
            isinstance(state["cumulative_lift"], list)
            and len(state["cumulative_lift"]) == 2
            and all(isinstance(item, int) for item in state["cumulative_lift"]),
            "state lift",
        )
        theta_center = module.arb(state["theta_center"])
        momentum_center = module.arb(state["momentum_center"])
        theta_radius = module.arb(state["theta_radius"])
        momentum_radius = module.arb(state["momentum_radius"])
        require(theta_radius > 0 and momentum_radius > 0, "positive state radius")
        maximum_radius = maximum_radius.max(theta_radius).max(momentum_radius)
        require(theta_radius < radius_threshold and momentum_radius < radius_threshold, "state radius bound")

        # Reconstruct the outward tube used by the producer.  The factor four is
        # deliberate slack over the already outward-rounded Taylor radii.
        theta_rad_text = (4 * theta_radius.abs_upper()).str(150, radius=False, more=True)
        momentum_rad_text = (4 * momentum_radius.abs_upper()).str(150, radius=False, more=True)
        theta_box = theta_center + module.arb(0, theta_rad_text)
        momentum_box = momentum_center + module.arb(0, momentum_rad_text)
        nx_box, ny_box = theta_box.cos(), theta_box.sin()
        nx_center, ny_center = theta_center.cos(), theta_center.sin()

        for action_name, matrix in certificate.symmetry.MATRICES.items():
            a, b, c, d = matrix
            determinant = a * d - b * c
            transformed_box = (
                a * nx_box + b * ny_box,
                c * nx_box + d * ny_box,
                determinant * momentum_box,
            )
            transformed_center = (
                a * nx_center + b * ny_center,
                c * nx_center + d * ny_center,
                determinant * momentum_center,
            )
            for core_index, core in enumerate(cores):
                row = comparison_rows[row_index]
                row_index += 1
                identity = {
                    "state_rank": expected_rank,
                    "symmetry": action_name,
                    "core_index": core_index,
                }
                for key, value in identity.items():
                    require(row.get(key) == value, f"comparison identity {key}")
                if core.source != state["source_component"]:
                    require(set(row) == categorical_keys, "closed categorical row schema")
                    require(row["status"] == "DISJOINT_COMPONENT", "categorical separation")
                    categorical += 1
                    certified += 1
                    continue

                require(set(row) == numeric_keys, "closed numeric row schema")
                require(row["status"] == "STRICT_COORDINATE_SEPARATION", "numeric separation status")
                side = core.chart_id.split(":")[1]
                t_box = transformed_box[1] if side in {"E", "W"} else transformed_box[0]
                t_center = transformed_center[1] if side in {"E", "W"} else transformed_center[0]
                tube_gaps = coordinate_gaps(module, t_box, transformed_box[2], core)
                center_gaps = coordinate_gaps(module, t_center, transformed_center[2], core)
                require(row["separator"] in tube_gaps, "registered separator label")
                require(tube_gaps[row["separator"]] > tube_threshold, "registered tube separator")
                strict_tube = [gap for gap in tube_gaps.values() if gap > 0]
                strict_center = [gap for gap in center_gaps.values() if gap > 0]
                require(strict_tube and strict_center, "strict coordinate alternatives")
                best_tube = max(strict_tube, key=lambda gap: float(gap.mid()))
                best_center = max(strict_center, key=lambda gap: float(gap.mid()))
                require(best_tube > tube_threshold, "independent tube gap")
                require(best_center > center_threshold, "independent center gap")
                if minimum_tube is None or float(best_tube.mid()) < float(minimum_tube.mid()):
                    minimum_tube = best_tube
                if minimum_center is None or float(best_center.mid()) < float(minimum_center.mid()):
                    minimum_center = best_center
                numeric += 1
                certified += 1

    require(row_index == len(comparison_rows), "comparison enumeration exhausted")
    require(categorical == 9312 and numeric == 9312 and certified == 18624, "independent partition")
    require(minimum_tube is not None and minimum_center is not None, "independent minima")
    claimed_radius = module.arb(result["maximum_phase_state_radius"])
    claimed_tube = module.arb(result["minimum_tube_coordinate_gap"])
    claimed_center = module.arb(result["minimum_center_coordinate_gap"])
    require((maximum_radius - claimed_radius).contains(0), "maximum-radius witness")
    require((minimum_tube - claimed_tube).contains(0), "minimum-tube witness")
    require((minimum_center - claimed_center).contains(0), "minimum-center witness")
    return {
        "precision_bits": VERIFY_PRECISION_BITS,
        "state_rows": len(state_rows),
        "D4_actions": len(certificate.symmetry.MATRICES),
        "C24_cores": len(cores),
        "comparisons": len(comparison_rows),
        "categorical_component_mismatches": categorical,
        "numeric_strict_coordinate_separations": numeric,
        "unresolved": 0,
        "radius_bound": "VERIFIED",
        "center_gap_bound": "VERIFIED",
        "tube_gap_bound": "VERIFIED",
    }


def scalar_paths(value: Any, prefix: tuple[Any, ...] = ()) -> Iterable[tuple[Any, ...]]:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in {"state_rows", "comparison_rows"}:
                continue
            yield from scalar_paths(child, prefix + (key,))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from scalar_paths(child, prefix + (index,))
    else:
        yield prefix


def get_path(value: Any, path: tuple[Any, ...]) -> Any:
    for key in path:
        value = value[key]
    return value


def set_path(value: Any, path: tuple[Any, ...], replacement: Any) -> None:
    for key in path[:-1]:
        value = value[key]
    value[path[-1]] = replacement


def altered(value: Any) -> Any:
    if value is None:
        return "MUTATED"
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if isinstance(value, str):
        return value + "_MUTATED"
    raise TypeError(f"unsupported hostile scalar: {type(value).__name__}")


def expect_rejection(document: dict[str, Any], expected: dict[str, Any]) -> None:
    try:
        validate_document(document, expected)
    except (VerificationError, KeyError, TypeError, ValueError):
        return
    raise VerificationError("hostile mutation accepted")


def mutation_suite(document: dict[str, Any], expected: dict[str, Any]) -> dict[str, Any]:
    result = document["result"]
    scalar_count = 0
    for path in list(scalar_paths(result)):
        old = get_path(result, path)
        set_path(result, path, altered(old))
        document["result_sha256"] = digest(result)
        expect_rejection(document, expected)
        set_path(result, path, old)
        document["result_sha256"] = digest(result)
        scalar_count += 1

    pin_count = 0
    for key in list(document["pins"]):
        old = document["pins"][key]
        document["pins"][key] = altered(old)
        expect_rejection(document, expected)
        document["pins"][key] = old
        pin_count += 1

    row_count = 0
    state_rows = result["state_rows"]
    for index in (0, len(state_rows) - 1):
        for key in list(state_rows[index]):
            old = state_rows[index][key]
            if isinstance(old, list):
                replacement = list(old)
                replacement[0] += 1
            else:
                replacement = altered(old)
            state_rows[index][key] = replacement
            result["state_rows_sha256"] = digest(state_rows)
            document["result_sha256"] = digest(result)
            expect_rejection(document, expected)
            state_rows[index][key] = old
            result["state_rows_sha256"] = digest(state_rows)
            document["result_sha256"] = digest(result)
            row_count += 1

    comparison_rows = result["comparison_rows"]
    representatives = [
        next(index for index, row in enumerate(comparison_rows) if row["status"] == "DISJOINT_COMPONENT"),
        next(index for index, row in enumerate(comparison_rows) if row["status"] == "STRICT_COORDINATE_SEPARATION"),
        len(comparison_rows) - 1,
    ]
    for index in representatives:
        for key in list(comparison_rows[index]):
            old = comparison_rows[index][key]
            comparison_rows[index][key] = altered(old)
            result["comparison_rows_sha256"] = digest(comparison_rows)
            document["result_sha256"] = digest(result)
            expect_rejection(document, expected)
            comparison_rows[index][key] = old
            result["comparison_rows_sha256"] = digest(comparison_rows)
            document["result_sha256"] = digest(result)
            row_count += 1

    structural_count = 0
    document["extra_claim"] = "CERTIFIED"
    expect_rejection(document, expected)
    del document["extra_claim"]
    structural_count += 1
    result["extra_claim"] = "CERTIFIED"
    document["result_sha256"] = digest(result)
    expect_rejection(document, expected)
    del result["extra_claim"]
    document["result_sha256"] = digest(result)
    structural_count += 1
    old_schema = document["schema"]
    document["schema"] = old_schema + ".hostile"
    expect_rejection(document, expected)
    document["schema"] = old_schema
    structural_count += 1
    old_hash = document["result_sha256"]
    document["result_sha256"] = "0" * 64
    expect_rejection(document, expected)
    document["result_sha256"] = old_hash
    structural_count += 1

    require(document == expected, "mutation suite restoration")
    return {
        "top_level_result_scalar_mutations_rejected": scalar_count,
        "pin_mutations_rejected": pin_count,
        "representative_nested_row_field_mutations_rejected": row_count,
        "structural_mutations_rejected": structural_count,
        "all_rejected": True,
    }


def strict_json_suite() -> dict[str, Any]:
    attacks = (
        '{"schema":"a","schema":"b"}',
        '{"value":NaN}',
        '{"value":Infinity}',
        '{"value":1e9999}',
    )
    rejected = 0
    for raw in attacks:
        try:
            loads_strict(raw)
        except (VerificationError, ValueError):
            rejected += 1
    require(rejected == len(attacks), "strict JSON attacks")
    return {"attacks": len(attacks), "rejected": rejected}


def build_audit(path: Path) -> dict[str, Any]:
    raw = path.read_text()
    document = loads_strict(raw)
    expected = certificate.build()
    validate_document(document, expected)
    independent = independent_separator_recomputation(document)
    mutations = mutation_suite(document, expected)
    strict_json = strict_json_suite()
    result = {
        "input_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "producer_reconstruction": "BYTE_SEMANTIC_EQUALITY_VERIFIED",
        "closed_schema": "VERIFIED_AT_ALL_NESTED_LEVELS_BY_EXACT_RECONSTRUCTION",
        "independent_higher_precision_separator_recomputation": independent,
        "hostile_mutation_suite": mutations,
        "strict_json_suite": strict_json,
        "verdict": "PASS",
    }
    return {
        "schema": "cm2.round84.stable-material-c24-support-separator-audit.v1",
        "result": result,
        "result_sha256": digest(result),
    }


def main(argv: list[str]) -> int:
    path = Path(argv[1]).resolve() if len(argv) > 1 else DEFAULT_INPUT
    json.dump(build_audit(path), sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
