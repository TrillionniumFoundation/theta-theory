#!/usr/bin/env python3
"""Read-only exact-near-positivity probe for the Round187 source-W tail.

For each of the exact 37,198 Round187 depth-2 clipped cells that fails the
coarse ``ell - radius > 0`` test, this spike checks the exact root-sign
criterion on the Delta >= 0 strata:

    ell > 0 and ell^2 - Delta > 0.

The second quantity is recomputed preferentially as
``distance_squared - target_radius_squared`` and cross-checked against the
direct ``ell^2 - Delta`` interval enclosure.  TAU and every competitor order
condition are independently replayed.  The 64 full-p cells stay separate.

This is not a certificate producer.  It has no output-path option, performs no
filesystem writes, emits progress only on stderr, prints one final JSON
document on stdout, and issues zero official promotion.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
import hashlib
import importlib
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any

sys.dont_write_bytecode = True

from flint import arb, ctx


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round193.source-w-exact-near-positivity-probe.v1"
MAX_INPUT_BYTES = 8 * 1024 * 1024

ROUND187_NAME = "cm2_round187_source_w_strict_first_refinement_probe.py"
ROUND187_SHA256 = (
    "6278b744f091657ff6035dc71a5656ba1ae861d3b672b591e6a77d718864c5cc"
)
ROUND190_NAME = "cm2_round190_source_w_strict_first_axis_probe.py"
ROUND190_SHA256 = (
    "722e155df1ec992fc837603997151cda79e938b241c4761c5a958ee7665ad397"
)

EXPECTED_ORIGIN_COUNT = 162
EXPECTED_ORIGIN_KEYS_SHA256 = (
    "c86ec3a7042b6aaa58eee59ec43a6ec2ebda8bd192cedfcf4c47d8c42c4615c3"
)
EXPECTED_TARGET_CELL_COUNT = 37198
EXPECTED_FULL_P_COUNT = 64
EXPECTED_TOTAL_RESIDUAL_COUNT = 37262
EXPECTED_TOTAL_RESIDUAL_VOLUME = Q(3297687, 838860800000)
EXPECTED_TOTAL_RESIDUAL_KEYS_SHA256 = (
    "060ac08ec0ccb026ad4cf735a4ebe5af30753a690e7fbe80a4b95f25de3be19e"
)

TARGET_FAILURE = "TARGET_NOT_STRICT_POSITIVE_FIRST"
FULL_P_FAILURE = "NOT_CLIPPED_FULL_P_GRAPH"

ELL_NOT_POSITIVE = "ELL_NOT_STRICT_POSITIVE"
DISTANCE_NOT_POSITIVE = (
    "DISTANCE_SQUARED_MINUS_RADIUS_SQUARED_NOT_STRICT_POSITIVE"
)
TAU_FAILURE = "ELL_NOT_STRICTLY_BELOW_TAU_MAX"
LOWER_ABSENT = "COMPETITOR_EARLIEST_LOWER_ABSENT"
ORDER_FAILURE = "ELL_NOT_STRICTLY_BELOW_COMPETITOR_EARLIEST_LOWER"
P_DERIVATIVE_OVERWRAP = "P_DERIVATIVE_OVERWRAP"
NOT_CLIPPED = "NOT_CLIPPED_FULL_P_GRAPH"
NEGATIVE_SIDE_FAILURE = "DELTA_NEGATIVE_SIDE_NOT_EXCLUDED"
POSITIVE_CHART_OVERWRAP = "DELTA_POSITIVE_OUTGOING_CHART_OVERWRAP"
POSITIVE_CHART_MATCH = "DELTA_POSITIVE_OUTGOING_CHART_MATCH"
GRAPH_CHART_OVERWRAP = "DELTA_ZERO_GRAPH_OUTGOING_CHART_OVERWRAP"
GRAPH_CHART_MATCH = "DELTA_ZERO_GRAPH_OUTGOING_CHART_MATCH"

FAILURE_ORDER = (
    ELL_NOT_POSITIVE,
    DISTANCE_NOT_POSITIVE,
    TAU_FAILURE,
    LOWER_ABSENT,
    ORDER_FAILURE,
    P_DERIVATIVE_OVERWRAP,
    NOT_CLIPPED,
    NEGATIVE_SIDE_FAILURE,
    POSITIVE_CHART_OVERWRAP,
    POSITIVE_CHART_MATCH,
    GRAPH_CHART_OVERWRAP,
    GRAPH_CHART_MATCH,
)


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


def map_counter(value: Counter[Any]) -> dict[str, int]:
    return {
        str(key): count for key, count in sorted(value.items())
    }


def fraction_map(value: dict[Any, Q]) -> dict[str, str]:
    return {
        str(key): str(item) for key, item in sorted(value.items())
    }


def nested_counter_map(
    value: dict[str, Counter[Any]],
) -> dict[str, dict[str, int]]:
    return {
        key: map_counter(counter)
        for key, counter in sorted(value.items())
    }


def progress(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


def read_regular(path: Path) -> bytes:
    absolute = Path(os.path.abspath(os.fspath(path)))
    require(absolute.parent == HERE, f"input parent:{absolute.name}")
    require(
        absolute.parent.resolve() == HERE,
        f"input parent resolution:{absolute.name}",
    )
    status = absolute.lstat()
    require(stat.S_ISREG(status.st_mode), f"input regular:{absolute.name}")
    require(not absolute.is_symlink(), f"input symlink:{absolute.name}")
    require(status.st_nlink == 1, f"input hardlink:{absolute.name}")
    require(
        0 < status.st_size <= MAX_INPUT_BYTES,
        f"input size:{absolute.name}",
    )
    descriptor = os.open(
        absolute, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    )
    try:
        opened = os.fstat(descriptor)
        require(
            (opened.st_dev, opened.st_ino)
            == (status.st_dev, status.st_ino),
            f"input race:{absolute.name}",
        )
        require(
            stat.S_ISREG(opened.st_mode)
            and opened.st_nlink == 1
            and opened.st_size == status.st_size,
            f"opened input type:{absolute.name}",
        )
        chunks: list[bytes] = []
        remaining = opened.st_size
        while remaining:
            chunk = os.read(descriptor, min(1024 * 1024, remaining))
            require(bool(chunk), f"short input:{absolute.name}")
            chunks.append(chunk)
            remaining -= len(chunk)
        require(not os.read(descriptor, 1), f"growing input:{absolute.name}")
        raw = b"".join(chunks)
    finally:
        os.close(descriptor)
    require(len(raw) == status.st_size, f"input byte count:{absolute.name}")
    return raw


def pin_probe_source(name: str, expected: str, label: str) -> None:
    require(
        hashlib.sha256(read_regular(HERE / name)).hexdigest() == expected,
        f"{label} source pin",
    )


# Pin both probe sources before either can execute.
pin_probe_source(ROUND187_NAME, ROUND187_SHA256, "Round187")
pin_probe_source(ROUND190_NAME, ROUND190_SHA256, "Round190")
if os.fspath(HERE) not in sys.path:
    sys.path.insert(0, os.fspath(HERE))
r190 = importlib.import_module(
    "cm2_round190_source_w_strict_first_axis_probe"
)
pin_probe_source(ROUND187_NAME, ROUND187_SHA256, "Round187 post-import")
pin_probe_source(ROUND190_NAME, ROUND190_SHA256, "Round190 post-import")
r187 = r190.r187
r180 = r190.r180
r176 = r190.r176


def check_chain() -> dict[str, Any]:
    require(
        Path(r190.__file__).resolve() == (HERE / ROUND190_NAME).resolve()
        and r190.ROUND187_SHA256 == ROUND187_SHA256,
        "Round190 module identity and Round187 pin",
    )
    return r190.check_delivery_chain()


def box_volume(box: Any) -> Q:
    return (
        (box.t1 - box.t0)
        * (box.p1 - box.p0)
        * (box.s1 - box.s0)
    )


def sign_name(value: arb) -> str:
    sign = r176.sign(value)
    return (
        "STRICT_POSITIVE"
        if sign > 0
        else "STRICT_NEGATIVE" if sign < 0 else "OVERWRAP"
    )


def exact_distance_evidence(
    row: Any,
    candidate: Any,
) -> dict[str, Any]:
    qx, qy, _ux, _uy, s, _rp = r176.geometry(
        row.chart_id, row.box
    )
    target = r176.TARGETS[candidate.target_id]
    ax, ay = r176.base.target_center(target, s)
    dx, dy = ax - qx, ay - qy
    radius = r176.base.arbq(
        r176.base.RADIUS[target.obstacle]
    )

    # Direct distance computation is the preferred enclosure.  Explicit
    # multiplication avoids python-flint's generic-power behavior at zero.
    direct = dx * dx + dy * dy - radius * radius
    identity = (
        candidate.ell * candidate.ell
        - candidate.discriminant
    )
    require(
        bool(direct.overlaps(identity)),
        f"distance/identity interval overlap:{row.key}",
    )
    ell_positive = bool(candidate.ell > 0)
    ell_negative = bool(candidate.ell < 0)
    distance_positive = bool(direct > 0)
    identity_positive = bool(identity > 0)
    require(not (ell_positive and ell_negative), f"ell signs:{row.key}")
    return {
        "direct_margin": direct,
        "identity_margin": identity,
        "direct_sign": sign_name(direct),
        "identity_sign": sign_name(identity),
        "ell_sign": sign_name(candidate.ell),
        "ell_positive": ell_positive,
        "ell_negative": ell_negative,
        "distance_positive": distance_positive,
        "identity_positive": identity_positive,
        "interval_enclosures_overlap": True,
        "exact_near_positive_on_Delta_nonnegative":
            ell_positive and distance_positive,
        "exact_far_negative_on_Delta_nonnegative":
            ell_negative and distance_positive,
    }


def evaluate_clipped_cell(row: Any) -> dict[str, Any]:
    records = r176.records_for(
        row.chart_id, row.box, row.active_targets
    )
    unresolved = [
        record
        for record in records
        if record.classification == "unresolved_discriminant"
    ]
    require(len(unresolved) == 1, f"unresolved target count:{row.key}")
    candidate = unresolved[0]
    original_proof, original_reason = r187.clipped_partition_proof(row)
    require(
        original_proof is None and original_reason == TARGET_FAILURE,
        f"Round187 target-tail identity:{row.key}:{original_reason}",
    )

    failures: set[str] = set()
    distance = exact_distance_evidence(row, candidate)
    if not distance["ell_positive"]:
        failures.add(ELL_NOT_POSITIVE)
    if not distance["distance_positive"]:
        failures.add(DISTANCE_NOT_POSITIVE)

    tau_ok = bool(
        candidate.ell < r176.base.arbq(r176.base.TAU_MAX)
    )
    if not tau_ok:
        failures.add(TAU_FAILURE)

    relevant_competitors = []
    absent_targets: list[str] = []
    order_failure_targets: list[str] = []
    competitor_rows: list[dict[str, Any]] = []
    for other in records:
        if (
            other.target_id == candidate.target_id
            or other.classification
            in {"no_real_intersection", "intersection_behind"}
        ):
            continue
        relevant_competitors.append(other)
        lower = r176.earliest_lower(other)
        if lower is None:
            failures.add(LOWER_ABSENT)
            absent_targets.append(other.target_id)
            competitor_rows.append({
                "target": other.target_id,
                "earliest_lower_exists": False,
                "ell_strictly_below_lower": False,
            })
            continue
        order_ok = bool(candidate.ell < lower)
        if not order_ok:
            failures.add(ORDER_FAILURE)
            order_failure_targets.append(other.target_id)
        competitor_rows.append({
            "target": other.target_id,
            "earliest_lower_exists": True,
            "ell_strictly_below_lower": order_ok,
            "lower_minus_ell_sign": sign_name(lower - candidate.ell),
        })

    derivative, lower_face, upper_face, full = r176.graph_faces(
        row, candidate
    )
    if derivative == 0:
        failures.add(P_DERIVATIVE_OVERWRAP)
    if full:
        failures.add(NOT_CLIPPED)

    negative = r176.remove_disposition(
        row, records, candidate.target_id
    )
    if negative is None or not negative.startswith("EXCLUDED"):
        failures.add(NEGATIVE_SIDE_FAILURE)

    positive_chart: str | None = None
    graph_chart: str | None = None
    if candidate.target_id != r176.FROZEN_OWNER:
        positive_disposition = "EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH"
        graph_disposition = "EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH"
    else:
        positive_chart = r176.positive_chart(row, candidate)
        if positive_chart is None:
            failures.add(POSITIVE_CHART_OVERWRAP)
            positive_disposition = "UNRESOLVED"
        elif positive_chart == r176.FROZEN_CHART:
            failures.add(POSITIVE_CHART_MATCH)
            positive_disposition = "LIVE_OUTGOING_CHART_MATCH"
        else:
            positive_disposition = "EXCLUDED_OUTGOING_CHART_MISMATCH"

        graph_chart = r187.tangent_chart(row, candidate)
        if graph_chart is None:
            failures.add(GRAPH_CHART_OVERWRAP)
            graph_disposition = "UNRESOLVED"
        elif graph_chart == r176.FROZEN_CHART:
            failures.add(GRAPH_CHART_MATCH)
            graph_disposition = "LIVE_OUTGOING_CHART_MATCH"
        else:
            graph_disposition = "EXCLUDED_OUTGOING_CHART_MISMATCH"

    ordered_failures = [
        reason for reason in FAILURE_ORDER if reason in failures
    ]
    require(
        len(ordered_failures) == len(failures),
        f"failure ordering coverage:{row.key}",
    )
    closed = not ordered_failures
    return {
        "closed": closed,
        "failures": ordered_failures,
        "candidate_target": candidate.target_id,
        "candidate_obstacle":
            r176.TARGETS[candidate.target_id].obstacle,
        "ell_sign": distance["ell_sign"],
        "direct_distance_margin_sign": distance["direct_sign"],
        "identity_margin_sign": distance["identity_sign"],
        "direct_identity_interval_overlap":
            distance["interval_enclosures_overlap"],
        "direct_distance_margin_strict_positive":
            distance["distance_positive"],
        "identity_margin_strict_positive":
            distance["identity_positive"],
        "exact_near_positive_on_Delta_nonnegative":
            distance["exact_near_positive_on_Delta_nonnegative"],
        "exact_far_negative_on_Delta_nonnegative":
            distance["exact_far_negative_on_Delta_nonnegative"],
        "TAU_condition": tau_ok,
        "relevant_competitor_count": len(relevant_competitors),
        "competitors": competitor_rows,
        "absent_lower_targets": sorted(absent_targets),
        "order_failure_targets": sorted(order_failure_targets),
        "p_derivative_sign":
            "POSITIVE" if derivative > 0 else
            "NEGATIVE" if derivative < 0 else "OVERWRAP",
        "p_lower_face_sign": r187.arb_sign_name(lower_face),
        "p_upper_face_sign": r187.arb_sign_name(upper_face),
        "full_p_graph": full,
        "Delta_negative_disposition": negative,
        "Delta_positive_disposition": positive_disposition,
        "Delta_zero_graph_disposition": graph_disposition,
        "Delta_positive_outgoing_chart":
            positive_chart if positive_chart is not None else "NOT_APPLICABLE",
        "Delta_zero_graph_outgoing_chart":
            graph_chart if graph_chart is not None else "NOT_APPLICABLE",
        "whole_closed_depth2_cell": closed,
        "proof_contract":
            "on Delta>=0, ell>0 and distance^2-R^2="
            "ell^2-Delta>0 imply near>0; Delta<0 uses candidate removal",
    }


def streaming_list_digest(rows: list[dict[str, Any]]) -> str:
    hasher = hashlib.sha256()
    hasher.update(b"[")
    for index, row in enumerate(rows):
        if index:
            hasher.update(b",")
        hasher.update(canonical(row).encode())
    hasher.update(b"]")
    return hasher.hexdigest()


def analyze_tail(residual: dict[str, Any]) -> dict[str, Any]:
    target_rows = residual["target_rows"]
    full_rows = residual["full_rows"]
    source_by_origin = residual["rebuilt"]["source_by_origin"]
    input_volume = residual["target_volume"]

    closed_count = 0
    closed_volume = Q(0)
    residual_count = 0
    residual_volume = Q(0)
    residual_reason_count: Counter[str] = Counter()
    residual_reason_volume: defaultdict[str, Q] = defaultdict(Q)
    exact_failure_combinations: Counter[str] = Counter()
    candidate_targets: Counter[str] = Counter()
    candidate_obstacles: Counter[str] = Counter()
    ell_signs: Counter[str] = Counter()
    direct_signs: Counter[str] = Counter()
    identity_signs: Counter[str] = Counter()
    direct_identity_positive_matrix: Counter[str] = Counter()
    exact_root_sign_class: Counter[str] = Counter()
    tau_conditions: Counter[str] = Counter()
    competitor_count: Counter[int] = Counter()
    competitor_target_occurrence: Counter[str] = Counter()
    competitor_order_margin_sign: Counter[str] = Counter()
    closure_by_target: Counter[str] = Counter()
    residual_by_target: Counter[str] = Counter()
    failure_by_target: dict[str, Counter[str]] = defaultdict(Counter)
    residual_by_origin: Counter[str] = Counter(
        row.origin_key for row in full_rows
    )
    closed_keys: list[str] = []
    residual_keys: list[str] = []
    evidence_rows: list[dict[str, Any]] = []

    for index, row in enumerate(target_rows, 1):
        outcome = evaluate_clipped_cell(row)
        volume = box_volume(row.box)
        candidate = outcome["candidate_target"]
        candidate_targets[candidate] += 1
        candidate_obstacles[outcome["candidate_obstacle"]] += 1
        ell_signs[outcome["ell_sign"]] += 1
        direct_signs[outcome["direct_distance_margin_sign"]] += 1
        identity_signs[outcome["identity_margin_sign"]] += 1
        matrix_key = (
            f"direct_{outcome['direct_distance_margin_strict_positive']}"
            f"__identity_{outcome['identity_margin_strict_positive']}"
        )
        direct_identity_positive_matrix[matrix_key] += 1
        if outcome["exact_near_positive_on_Delta_nonnegative"]:
            exact_root_sign_class["EXACT_NEAR_POSITIVE"] += 1
        elif outcome["exact_far_negative_on_Delta_nonnegative"]:
            exact_root_sign_class["EXACT_FAR_NEGATIVE"] += 1
        else:
            exact_root_sign_class["ROOT_SIGN_UNRESOLVED"] += 1
        tau_conditions[
            "PASS" if outcome["TAU_condition"] else "FAIL"
        ] += 1
        competitor_count[outcome["relevant_competitor_count"]] += 1
        for competitor in outcome["competitors"]:
            competitor_target_occurrence[competitor["target"]] += 1
            if competitor["earliest_lower_exists"]:
                competitor_order_margin_sign[
                    competitor["lower_minus_ell_sign"]
                ] += 1

        combination = (
            "+".join(outcome["failures"])
            if outcome["failures"] else "NONE__CLOSED"
        )
        exact_failure_combinations[combination] += 1
        if outcome["closed"]:
            closed_count += 1
            closed_volume += volume
            closed_keys.append(row.key)
            closure_by_target[candidate] += 1
        else:
            residual_count += 1
            residual_volume += volume
            residual_reason_count[combination] += 1
            residual_reason_volume[combination] += volume
            residual_keys.append(row.key)
            residual_by_origin[row.origin_key] += 1
            residual_by_target[candidate] += 1
            for failure in outcome["failures"]:
                failure_by_target[failure][candidate] += 1

        evidence_rows.append({
            "cell_key": row.key,
            "origin_key": row.origin_key,
            **outcome,
        })
        if index % 2500 == 0 or index == len(target_rows):
            progress(f"exact near cells {index}/{len(target_rows)}")

    require(
        closed_count + residual_count == len(target_rows)
        and closed_volume + residual_volume == input_volume,
        "target-cell count and exact-volume conservation",
    )
    complete_origins = sorted(
        origin
        for origin in source_by_origin
        if residual_by_origin.get(origin, 0) == 0
    )
    strict_interior_complete = sorted(
        origin
        for origin in complete_origins
        if source_by_origin[origin]["classification"]
        == r187.SOURCE_INTERIOR
    )
    seam_complete = sorted(
        set(complete_origins) - set(strict_interior_complete)
    )
    residual_origins = sorted(
        origin
        for origin in source_by_origin
        if residual_by_origin.get(origin, 0) > 0
    )
    require(
        len(complete_origins) + len(residual_origins)
        == len(source_by_origin) == EXPECTED_ORIGIN_COUNT,
        "origin partition",
    )
    full_origins = sorted({row.origin_key for row in full_rows})
    direct_dependency_insufficient = (
        direct_signs.get("OVERWRAP", 0)
        + direct_signs.get("STRICT_NEGATIVE", 0)
    )
    root_classes = map_counter(exact_root_sign_class)
    if closed_count == len(target_rows):
        verdict = "VALIDATED"
    elif closed_count:
        verdict = "PARTIAL"
    else:
        verdict = "INVALIDATED"
    next_method = (
        "CENTERED_MEAN_VALUE_OR_ONE_LEVEL_PARENT_ONLY_AXIS_COMPARISON"
        if direct_dependency_insufficient
        else (
            "EXACT_BEHIND_TARGET_REMOVAL_USING_ELL_NEGATIVE_AND_"
            "DISTANCE_MARGIN_POSITIVE"
            if exact_root_sign_class.get("EXACT_FAR_NEGATIVE", 0)
            else "FORMALIZE_EXACT_NEAR_POSITIVITY_WITH_INDEPENDENT_VERIFIER"
        )
    )
    return {
        "spike_verdict": verdict,
        "input_clipped_cell_count": len(target_rows),
        "input_clipped_exact_volume": str(input_volume),
        "whole_depth2_clipped_cell_closed_count": closed_count,
        "whole_depth2_clipped_cell_closed_volume": str(closed_volume),
        "residual_clipped_cell_count": residual_count,
        "residual_clipped_exact_volume": str(residual_volume),
        "residual_reason_count": map_counter(residual_reason_count),
        "residual_reason_exact_volume":
            fraction_map(residual_reason_volume),
        "exact_failure_combination_count":
            map_counter(exact_failure_combinations),
        "candidate_target_count": map_counter(candidate_targets),
        "candidate_obstacle_count": map_counter(candidate_obstacles),
        "ell_sign_count": map_counter(ell_signs),
        "direct_distance_margin_sign_count": map_counter(direct_signs),
        "identity_margin_sign_count": map_counter(identity_signs),
        "direct_identity_strict_positive_matrix":
            map_counter(direct_identity_positive_matrix),
        "direct_identity_interval_overlap_count": len(target_rows),
        "exact_root_sign_class_count": root_classes,
        "TAU_condition_count": map_counter(tau_conditions),
        "relevant_competitor_count_per_cell":
            map_counter(competitor_count),
        "competitor_target_occurrence":
            map_counter(competitor_target_occurrence),
        "competitor_lower_minus_ell_sign_count":
            map_counter(competitor_order_margin_sign),
        "closed_count_by_candidate_target":
            map_counter(closure_by_target),
        "residual_count_by_candidate_target":
            map_counter(residual_by_target),
        "failure_count_by_candidate_target":
            nested_counter_map(failure_by_target),
        "closed_cell_keys_sha256": digest(sorted(closed_keys)),
        "residual_cell_keys_sha256": digest(sorted(residual_keys)),
        "per_cell_evidence_rows_sha256":
            streaming_list_digest(evidence_rows),
        "full_p_holdout": {
            "cell_count": len(full_rows),
            "exact_volume": str(residual["full_volume"]),
            "origin_count": len(full_origins),
            "origin_keys": full_origins,
            "origin_keys_sha256": digest(full_origins),
            "method": "SEPARATE_FIRST_ROOT_EQUALITY_CONTINUATION",
            "probe_credit": 0,
        },
        "whole_origin_outcome": {
            "geometrically_complete_origin_count":
                len(complete_origins),
            "geometrically_complete_origin_keys":
                complete_origins,
            "geometrically_complete_origin_keys_sha256":
                digest(complete_origins),
            "strict_physical_interior_complete_origin_count":
                len(strict_interior_complete),
            "strict_physical_interior_complete_origin_keys":
                strict_interior_complete,
            "source_seam_geometrically_complete_but_held_out_count":
                len(seam_complete),
            "source_seam_geometrically_complete_but_held_out_keys":
                seam_complete,
            "residual_origin_count": len(residual_origins),
            "residual_origin_keys": residual_origins,
            "residual_origin_keys_sha256": digest(residual_origins),
            "official_whole_origin_credit": 0,
        },
        "dependency_fallback": {
            "direct_distance_interval_insufficient_cell_count":
                direct_dependency_insufficient,
            "centered_mean_value_run": False,
            "one_level_outcome_blind_axis_run": False,
            "fallback_not_run_if_direct_margin_was_already_strict":
                direct_dependency_insufficient == 0,
        },
        "recommended_next_method": next_method,
        "exact_count_and_volume_conservation": True,
    }


def build_probe() -> dict[str, Any]:
    inputs = check_chain()
    progress("reconstruct exact Round187 depth2 residual")
    residual = r190.rebuild_depth2_residual(inputs)
    require(
        len(residual["all_rows"]) == EXPECTED_TOTAL_RESIDUAL_COUNT
        and len(residual["target_rows"]) == EXPECTED_TARGET_CELL_COUNT
        and len(residual["full_rows"]) == EXPECTED_FULL_P_COUNT
        and residual["residual_volume"] == EXPECTED_TOTAL_RESIDUAL_VOLUME
        and digest([row.key for row in residual["all_rows"]])
        == EXPECTED_TOTAL_RESIDUAL_KEYS_SHA256
        and len(residual["residual_rows_by_origin"])
        == EXPECTED_ORIGIN_COUNT
        and digest(sorted(residual["residual_rows_by_origin"]))
        == EXPECTED_ORIGIN_KEYS_SHA256,
        "Round187 exact residual constants",
    )

    progress("evaluate exact near positivity and all clipped preconditions")
    analysis = analyze_tail(residual)
    result = {
        "status":
            "READ_ONLY_ZERO_PROMOTION_SOURCE_W_EXACT_NEAR_POSITIVITY_PROBE",
        "spike_verdict": analysis["spike_verdict"],
        "question":
            "Does replacing ell-radius>0 by exact ell>0 and "
            "ell^2-Delta=distance^2-R^2>0 close the Round187 clipped tail?",
        "parameters": {
            "arb_precision_bits": 192,
            "hash_seed_external": "193052",
            "Round187_extra_depth_reconstructed": 2,
            "additional_refinement_depth": 0,
        },
        "input_chain": {
            "Round187_source_sha256": ROUND187_SHA256,
            "Round190_source_sha256": ROUND190_SHA256,
            "Round190_used_only_as_probe_library": True,
            "Round187_used_only_as_probe_library": True,
        },
        "exact_Round187_depth2_residual": {
            "residual_cell_count": len(residual["all_rows"]),
            "target_positive_first_failure_cell_count":
                len(residual["target_rows"]),
            "full_p_graph_holdout_cell_count": len(residual["full_rows"]),
            "origin_count": len(residual["residual_rows_by_origin"]),
            "origin_keys_sha256": EXPECTED_ORIGIN_KEYS_SHA256,
            "total_exact_volume": str(residual["residual_volume"]),
            "target_positive_first_failure_exact_volume":
                str(residual["target_volume"]),
            "full_p_graph_holdout_exact_volume":
                str(residual["full_volume"]),
            "residual_cell_keys_sha256":
                EXPECTED_TOTAL_RESIDUAL_KEYS_SHA256,
            "exact_count_and_volume_partition_reconfirmed": True,
        },
        "exact_near_positivity_analysis": analysis,
        "mathematical_contract": {
            "Delta_nonnegative_strata":
                "ell>0 and distance^2-R^2=ell^2-Delta>0 imply "
                "ell-sqrt(Delta)>0",
            "Delta_negative_open_stratum":
                "candidate has no real intersection and is removed before "
                "recomputing disposition",
            "distance_path":
                "directly recompute dx^2+dy^2-R^2 from source and target "
                "geometry",
            "identity_cross_check":
                "direct distance and ell^2-Delta Arb enclosures must overlap",
            "lower_dimensional_nonpromotion":
                "no graph nonemptiness, incidence, or integer credit inferred",
        },
        "zero_promotion_contract": {
            "probe_only": True,
            "filesystem_writes": 0,
            "official_ledger_mutated": False,
            "probe_counts_applied_to_official_ledger": False,
            "whole_origin_integer_credit_issued": 0,
            "D02": "UNCHANGED_BLOCKED",
            "D03_negative_oracle": "UNCHANGED_UNAUTHORIZED",
            "Gate5": "UNCHANGED_10_OF_18",
            "complete_18_field_blocks": 0,
            "CM2": "UNCHANGED_NO_GO",
            "required_before_any_ledger_use":
                "formal producer plus independent non-importing verifier",
        },
    }
    return {
        "schema": SCHEMA,
        "probe_result": result,
        "probe_result_sha256": digest(result),
    }


def main() -> int:
    ctx.prec = 192
    document = build_probe()
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
