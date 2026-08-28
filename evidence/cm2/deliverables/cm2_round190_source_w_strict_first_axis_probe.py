#!/usr/bin/env python3
"""Read-only Round190 diagnostic for the Round187 source-W strict-first tail.

This spike pins the complete Round180 and Round184 deliveries before importing
the final Round187 probe.  It reconstructs the exact depth-2 Round187 residual,
decomposes every TARGET_NOT_STRICT_POSITIVE_FIRST decision into explicit
failure masks, and compares one fixed t, p, or s split on the same 37,198
cells.

The post-hoc best-per-cell comparison is intentionally marked inadmissible for
certificate selection: it observes child outcomes before choosing an axis.
This program has no output-path option, performs no filesystem writes, emits
progress only on stderr, prints one final JSON document on stdout, and issues
zero promotion or official ledger credit.
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

from flint import ctx


HERE = Path(__file__).resolve().parent
SCHEMA = "cm2.round190.source-w-strict-first-axis-probe.v1"
MAX_INPUT_BYTES = 8 * 1024 * 1024

ROUND180_PINS = {
    "cm2_round180_full_multi_residual_dimension_safe_partial.py":
        "0ddb815a036a6e351929c484a00a565ce8969286bb137977ee9470577d807955",
    "cm2_round180_full_multi_residual_dimension_safe_partial_certificate.json":
        "46c6f1b2e86f9aa70d9126b28febbf97a81d6a4ac8f610dc2bb82d032a1abb70",
    "cm2_round180_full_multi_residual_dimension_safe_partial_verifier.py":
        "12e25ebe0bae92cd8bda5cc3c00c7c3c94dda01ded5042c6e7a09152f840d6a4",
    "cm2_round180_full_multi_residual_dimension_safe_partial_verification.json":
        "fb1b71c3006fcf4a10ee79d324346e2065ff2002252b28a29bd5085cab7e4caf",
    "cm2_round180_full_multi_residual_dimension_safe_partial_report.md":
        "aae414b750578f7f2c1203e51c59c57a5cf5c5d1aefa5c2cbdb63bcd256233dd",
    "cm2_round180_full_multi_residual_dimension_safe_partial_cold_replay.md":
        "b6dd550c663157d122c6e63e8c2a2974f420144d57814a874db664331b8f740a",
    "cm2_round180_full_multi_residual_dimension_safe_partial_manifest.sha256":
        "19c292b1d2e82388af891340676ccf0eb6f02f0301fe381f9102a52df0fd1aa4",
}

ROUND184_STEM = (
    "cm2_round184_source_w_upper_candidate_priority_and_clipped_delta"
)
ROUND184_PINS = {
    f"{ROUND184_STEM}.py":
        "28e2bade0186150298827228670a45da54698a8c301180a1646464a2e0bfb906",
    f"{ROUND184_STEM}_certificate.json":
        "292d80567378b2e028e0e90612b5025533f11fd23a35067fb813dfa57e76e17f",
    f"{ROUND184_STEM}_verifier.py":
        "55a4e2b44d0f8617d7b7fd0befd251a5cb206d388c23d7b395e39b9a17fa4889",
    f"{ROUND184_STEM}_verification.json":
        "7e10309c4d18f7b9101fb57df80c786ea68e4dfa440d80cb1a57f680348cbdd6",
    f"{ROUND184_STEM}_report.md":
        "21c424cd3180f01a8b7b239ef2747c63d6f2787694c173b89d0d9a35b6594ff1",
    f"{ROUND184_STEM}_cold_replay.md":
        "b57a96d7205459e4e9b72f159e22e6e2e8e514f88370d1ca41971d7a6b7727e9",
    f"{ROUND184_STEM}_manifest.sha256":
        "3c2a50663dc47479f67435109b737362895e53a2c1b4c29991fe875c5ac68cd1",
}

ROUND187_NAME = "cm2_round187_source_w_strict_first_refinement_probe.py"
ROUND187_SHA256 = (
    "6278b744f091657ff6035dc71a5656ba1ae861d3b672b591e6a77d718864c5cc"
)
ROUND184_VERIFICATION_RESULT = (
    "126bf98cd4bdc1fc7a69b2a57329b89359b74749bbbd1f43fdbccbc816add9e9"
)

EXPECTED_ORIGIN_COUNT = 162
EXPECTED_ORIGIN_KEYS_SHA256 = (
    "c86ec3a7042b6aaa58eee59ec43a6ec2ebda8bd192cedfcf4c47d8c42c4615c3"
)
EXPECTED_DEPTH2_RESIDUAL_COUNT = 37262
EXPECTED_TARGET_FAILURE_COUNT = 37198
EXPECTED_FULL_P_COUNT = 64
EXPECTED_DEPTH2_RESIDUAL_VOLUME = Q(3297687, 838860800000)
EXPECTED_DEPTH2_RESIDUAL_KEYS_SHA256 = (
    "060ac08ec0ccb026ad4cf735a4ebe5af30753a690e7fbe80a4b95f25de3be19e"
)

TARGET_FAILURE = "TARGET_NOT_STRICT_POSITIVE_FIRST"
FULL_P_FAILURE = "NOT_CLIPPED_FULL_P_GRAPH"
AXES = ("t", "p", "s")

MASK_CLEARANCE = "ELL_MINUS_RADIUS_NOT_STRICT_POSITIVE"
MASK_TAU = "ELL_NOT_STRICTLY_BELOW_TAU_MAX"
MASK_LOWER_ABSENT = "COMPETITOR_EARLIEST_LOWER_ABSENT"
MASK_ORDER = "ELL_NOT_STRICTLY_BELOW_COMPETITOR_EARLIEST_LOWER"
MASK_ORDERING = (
    MASK_CLEARANCE,
    MASK_TAU,
    MASK_LOWER_ABSENT,
    MASK_ORDER,
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
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(absolute, flags)
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


def check_pin_set(pins: dict[str, str], label: str) -> None:
    for name, expected in pins.items():
        require(
            hashlib.sha256(read_regular(HERE / name)).hexdigest() == expected,
            f"{label} pin:{name}",
        )


def preimport_pin() -> None:
    check_pin_set(ROUND180_PINS, "Round180")
    check_pin_set(ROUND184_PINS, "Round184")
    require(
        hashlib.sha256(read_regular(HERE / ROUND187_NAME)).hexdigest()
        == ROUND187_SHA256,
        "Round187 source pin",
    )


# Pin the dependency bytes before any dependency module can execute.
preimport_pin()
if os.fspath(HERE) not in sys.path:
    sys.path.insert(0, os.fspath(HERE))
r187 = importlib.import_module(
    "cm2_round187_source_w_strict_first_refinement_probe"
)
preimport_pin()
r180 = r187.r180
r176 = r180.r176


def check_delivery_chain() -> dict[str, Any]:
    require(
        Path(r187.__file__).resolve() == (HERE / ROUND187_NAME).resolve(),
        "Round187 module identity",
    )
    require(
        r187.ROUND184_PRODUCER_SHA256
        == ROUND184_PINS[f"{ROUND184_STEM}.py"]
        and r187.ROUND184_CERTIFICATE_SHA256
        == ROUND184_PINS[f"{ROUND184_STEM}_certificate.json"],
        "Round187 embedded Round184 pins",
    )
    round187_inputs = r187.check_inputs()

    manifest_name = f"{ROUND184_STEM}_manifest.sha256"
    entries: dict[str, str] = {}
    for line in read_regular(HERE / manifest_name).decode("ascii").splitlines():
        value, name = line.split("  ", 1)
        require(name not in entries, f"Round184 manifest duplicate:{name}")
        entries[name] = value
    require(
        entries
        == {
            name: expected
            for name, expected in ROUND184_PINS.items()
            if name != manifest_name
        },
        "Round184 manifest exact entries",
    )

    verification = r187.strict_load(
        HERE / f"{ROUND184_STEM}_verification.json"
    )
    require(
        verification["result_sha256"] == ROUND184_VERIFICATION_RESULT
        and digest(verification["result"]) == ROUND184_VERIFICATION_RESULT
        and verification["result"]["status"] == "PASS_PARTIAL_BOUNDED_ROUND184"
        and verification["result"]["independence_contract"][
            "producer_imported_or_executed"
        ] is False
        and verification["result"]["independence_contract"][
            "complete_expected_certificate_rebuilt"
        ] is True
        and verification["result"]["independence_contract"][
            "full_expected_certificate_byte_for_byte_equality"
        ] is True,
        "Round184 formal verification",
    )
    return round187_inputs


def box_volume(box: Any) -> Q:
    return (
        (box.t1 - box.t0)
        * (box.p1 - box.p0)
        * (box.s1 - box.s0)
    )


def streaming_list_digest(rows: list[dict[str, Any]]) -> str:
    hasher = hashlib.sha256()
    hasher.update(b"[")
    for index, row in enumerate(rows):
        if index:
            hasher.update(b",")
        hasher.update(canonical(row).encode())
    hasher.update(b"]")
    return hasher.hexdigest()


def rebuild_depth2_residual(
    inputs: dict[str, Any],
) -> dict[str, Any]:
    rebuilt = r187.rebuild_round184_target_children(inputs)
    target_rows: list[Any] = []
    full_rows: list[Any] = []
    residual_rows_by_origin: dict[str, list[Any]] = defaultdict(list)
    residual_reason_by_key: dict[str, str] = {}
    residual_volume = Q(0)

    for index, origin in enumerate(inputs["target_keys"], 1):
        for root in rebuilt["failed_by_origin"][origin]:
            pending = [(root, 0)]
            while pending:
                row, depth = pending.pop()
                direct_kind, _evidence = r187.direct_strict_terminal(row)
                if direct_kind == "EXCLUDED":
                    continue
                if direct_kind is not None:
                    reason = f"DIRECT_STRICT_{direct_kind}"
                else:
                    proof, reason = r187.clipped_partition_proof(row)
                    if proof is not None:
                        continue
                if depth < 2:
                    axis = r180.split_axis(row.box)
                    lower, upper = r176.split(row.box, axis)
                    pending.append((r187.child_frontier(row, upper), depth + 1))
                    pending.append((r187.child_frontier(row, lower), depth + 1))
                    continue
                require(
                    reason in {TARGET_FAILURE, FULL_P_FAILURE},
                    f"unexpected Round187 depth2 reason:{row.key}:{reason}",
                )
                residual_rows_by_origin[origin].append(row)
                residual_reason_by_key[row.key] = reason
                residual_volume += box_volume(row.box)
                if reason == TARGET_FAILURE:
                    target_rows.append(row)
                else:
                    full_rows.append(row)
        if index % 20 == 0 or index == len(inputs["target_keys"]):
            progress(
                f"rebuild Round187 depth2 residual {index}/"
                f"{len(inputs['target_keys'])} origins"
            )

    for rows in residual_rows_by_origin.values():
        rows.sort(key=lambda row: row.key)
    target_rows.sort(key=lambda row: row.key)
    full_rows.sort(key=lambda row: row.key)
    all_rows = sorted(target_rows + full_rows, key=lambda row: row.key)
    origin_keys = sorted(residual_rows_by_origin)
    reason_counts = Counter(residual_reason_by_key.values())
    require(
        len(all_rows) == EXPECTED_DEPTH2_RESIDUAL_COUNT
        and len(target_rows) == EXPECTED_TARGET_FAILURE_COUNT
        and len(full_rows) == EXPECTED_FULL_P_COUNT
        and reason_counts
        == Counter({
            TARGET_FAILURE: EXPECTED_TARGET_FAILURE_COUNT,
            FULL_P_FAILURE: EXPECTED_FULL_P_COUNT,
        })
        and len(origin_keys) == EXPECTED_ORIGIN_COUNT
        and digest(origin_keys) == EXPECTED_ORIGIN_KEYS_SHA256
        and residual_volume == EXPECTED_DEPTH2_RESIDUAL_VOLUME
        and digest([row.key for row in all_rows])
        == EXPECTED_DEPTH2_RESIDUAL_KEYS_SHA256,
        "exact Round187 depth2 residual",
    )
    require(
        set(origin_keys) == set(inputs["target_keys"]),
        "Round187 residual origin set",
    )
    return {
        "inputs": inputs,
        "rebuilt": rebuilt,
        "target_rows": target_rows,
        "full_rows": full_rows,
        "all_rows": all_rows,
        "residual_rows_by_origin": residual_rows_by_origin,
        "residual_reason_by_key": residual_reason_by_key,
        "target_volume": sum(
            (box_volume(row.box) for row in target_rows), Q(0)
        ),
        "full_volume": sum(
            (box_volume(row.box) for row in full_rows), Q(0)
        ),
        "residual_volume": residual_volume,
    }


def failure_mask_census(rows: list[Any]) -> dict[str, Any]:
    mask_hits: Counter[str] = Counter()
    exact_combinations: Counter[str] = Counter()
    exclusive: Counter[str] = Counter()
    cardinality: Counter[int] = Counter()
    candidate_targets: Counter[str] = Counter()
    candidate_obstacles: Counter[str] = Counter()
    candidate_target_by_combination: dict[str, Counter[str]] = defaultdict(Counter)
    total_competitors_per_cell: Counter[int] = Counter()
    relevant_competitors_per_cell: Counter[int] = Counter()
    skipped_competitors_per_cell: Counter[int] = Counter()
    failing_competitors_per_cell: Counter[int] = Counter()
    relevant_target_occurrence: Counter[str] = Counter()
    skipped_target_occurrence: Counter[str] = Counter()
    absent_lower_target_occurrence: Counter[str] = Counter()
    order_failure_target_occurrence: Counter[str] = Counter()
    clearance_signs: Counter[str] = Counter()
    tau_margin_signs: Counter[str] = Counter()
    order_margin_signs: Counter[str] = Counter()
    summary_rows: list[dict[str, Any]] = []

    for index, row in enumerate(rows, 1):
        records = r176.records_for(
            row.chart_id, row.box, row.active_targets
        )
        unresolved = [
            record
            for record in records
            if record.classification == "unresolved_discriminant"
        ]
        require(len(unresolved) == 1, f"mask candidate:{row.key}")
        candidate = unresolved[0]
        radius = r176.base.arbq(
            r176.base.RADIUS[
                r176.TARGETS[candidate.target_id].obstacle
            ]
        )
        tau_max = r176.base.arbq(r176.base.TAU_MAX)
        clearance_ok = bool(candidate.ell - radius > 0)
        tau_ok = bool(candidate.ell < tau_max)
        masks: set[str] = set()
        if not clearance_ok:
            masks.add(MASK_CLEARANCE)
        if not tau_ok:
            masks.add(MASK_TAU)

        competitors = [
            other
            for other in records
            if other.target_id != candidate.target_id
        ]
        relevant = [
            other
            for other in competitors
            if other.classification
            not in {"no_real_intersection", "intersection_behind"}
        ]
        skipped = [
            other for other in competitors if other not in relevant
        ]
        absent_targets: list[str] = []
        order_failure_targets: list[str] = []
        competitor_passes: list[bool] = []
        for other in relevant:
            relevant_target_occurrence[other.target_id] += 1
            lower = r176.earliest_lower(other)
            if lower is None:
                masks.add(MASK_LOWER_ABSENT)
                absent_targets.append(other.target_id)
                absent_lower_target_occurrence[other.target_id] += 1
                competitor_passes.append(False)
                continue
            margin = lower - candidate.ell
            margin_sign = r176.sign(margin)
            order_margin_signs[
                "STRICT_POSITIVE"
                if margin_sign > 0
                else "STRICT_NEGATIVE"
                if margin_sign < 0
                else "OVERWRAP"
            ] += 1
            order_ok = bool(candidate.ell < lower)
            competitor_passes.append(order_ok)
            if not order_ok:
                masks.add(MASK_ORDER)
                order_failure_targets.append(other.target_id)
                order_failure_target_occurrence[other.target_id] += 1
        for other in skipped:
            skipped_target_occurrence[other.target_id] += 1

        reconstructed = (
            clearance_ok
            and tau_ok
            and all(competitor_passes)
        )
        require(
            reconstructed
            == r176.target_positive_first(candidate, records)
            and reconstructed is False
            and bool(masks),
            f"failure mask equivalence:{row.key}",
        )
        ordered_masks = [
            mask for mask in MASK_ORDERING if mask in masks
        ]
        combination = "+".join(ordered_masks)
        mask_hits.update(ordered_masks)
        exact_combinations[combination] += 1
        cardinality[len(ordered_masks)] += 1
        if len(ordered_masks) == 1:
            exclusive[ordered_masks[0]] += 1
        candidate_targets[candidate.target_id] += 1
        candidate_obstacle = r176.TARGETS[
            candidate.target_id
        ].obstacle
        candidate_obstacles[candidate_obstacle] += 1
        candidate_target_by_combination[combination][
            candidate.target_id
        ] += 1
        total_competitors_per_cell[len(competitors)] += 1
        relevant_competitors_per_cell[len(relevant)] += 1
        skipped_competitors_per_cell[len(skipped)] += 1
        failing_competitors_per_cell[
            len(absent_targets) + len(order_failure_targets)
        ] += 1
        clearance_sign = r176.sign(candidate.ell - radius)
        clearance_signs[
            "STRICT_POSITIVE"
            if clearance_sign > 0
            else "STRICT_NEGATIVE"
            if clearance_sign < 0
            else "OVERWRAP"
        ] += 1
        tau_sign = r176.sign(tau_max - candidate.ell)
        tau_margin_signs[
            "STRICT_POSITIVE"
            if tau_sign > 0
            else "STRICT_NEGATIVE"
            if tau_sign < 0
            else "OVERWRAP"
        ] += 1
        summary_rows.append({
            "cell_key": row.key,
            "origin_key": row.origin_key,
            "candidate_target": candidate.target_id,
            "candidate_obstacle": candidate_obstacle,
            "failure_masks": ordered_masks,
            "total_competitor_count": len(competitors),
            "relevant_competitor_count": len(relevant),
            "skipped_nonthreat_competitor_count": len(skipped),
            "absent_lower_targets": sorted(absent_targets),
            "order_failure_targets": sorted(order_failure_targets),
        })
        if index % 5000 == 0 or index == len(rows):
            progress(f"failure masks {index}/{len(rows)} cells")

    overlap_count = sum(
        count for size, count in cardinality.items() if size > 1
    )
    require(
        sum(exact_combinations.values()) == len(rows)
        and sum(cardinality.values()) == len(rows)
        and sum(exclusive.values()) + overlap_count == len(rows),
        "failure-mask census",
    )
    return {
        "cell_count": len(rows),
        "mask_definition": {
            MASK_CLEARANCE: "not bool(candidate.ell - radius > 0)",
            MASK_TAU: "not bool(candidate.ell < TAU_MAX)",
            MASK_LOWER_ABSENT:
                "at least one relevant competitor has earliest_lower=None",
            MASK_ORDER:
                "at least one relevant competitor with earliest_lower "
                "fails bool(candidate.ell < earliest_lower)",
            "relevant_competitor":
                "other target not classified no_real_intersection or "
                "intersection_behind",
        },
        "mask_hit_count": map_counter(mask_hits),
        "exact_failure_mask_combination_count":
            map_counter(exact_combinations),
        "exclusive_single_mask_count": map_counter(exclusive),
        "overlap_cell_count": overlap_count,
        "failure_mask_cardinality_count": map_counter(cardinality),
        "candidate_target_count": map_counter(candidate_targets),
        "candidate_obstacle_count": map_counter(candidate_obstacles),
        "candidate_target_by_exact_mask":
            nested_counter_map(candidate_target_by_combination),
        "total_competitor_count_per_cell":
            map_counter(total_competitors_per_cell),
        "relevant_competitor_count_per_cell":
            map_counter(relevant_competitors_per_cell),
        "skipped_nonthreat_competitor_count_per_cell":
            map_counter(skipped_competitors_per_cell),
        "failing_competitor_count_per_cell":
            map_counter(failing_competitors_per_cell),
        "relevant_competitor_target_occurrence":
            map_counter(relevant_target_occurrence),
        "skipped_nonthreat_target_occurrence":
            map_counter(skipped_target_occurrence),
        "absent_lower_competitor_target_occurrence":
            map_counter(absent_lower_target_occurrence),
        "order_failure_competitor_target_occurrence":
            map_counter(order_failure_target_occurrence),
        "ell_minus_radius_sign_count": map_counter(clearance_signs),
        "TAU_MAX_minus_ell_sign_count": map_counter(tau_margin_signs),
        "competitor_lower_minus_ell_sign_count":
            map_counter(order_margin_signs),
        "failure_mask_rows_sha256": streaming_list_digest(summary_rows),
        "target_positive_first_boolean_equivalence_rechecked": True,
    }


def child_outcome(row: Any) -> dict[str, Any]:
    direct_kind, direct_evidence = r187.direct_strict_terminal(row)
    if direct_kind == "EXCLUDED":
        require(
            direct_evidence is not None
            and direct_evidence["whole_closed_child"]
            and direct_evidence[
                "all_owned_boundary_strata_inherit_strict_proof"
            ],
            f"direct closed contract:{row.key}",
        )
        return {
            "closed": True,
            "method": "DIRECT_STRICT_CLOSED_BOX",
            "reason": "EXCLUDED",
        }
    if direct_kind is not None:
        require(
            direct_kind in {"LIVE", "MIXED"},
            f"direct retained kind:{row.key}:{direct_kind}",
        )
        return {
            "closed": False,
            "method": "DIRECT_STRICT_CLOSED_BOX",
            "reason": f"DIRECT_STRICT_{direct_kind}",
        }
    proof, reason = r187.clipped_partition_proof(row)
    if proof is not None:
        require(
            reason == "CLOSED"
            and proof["all_three_strata_excluded"]
            and proof["whole_closed_cell_excluded"],
            f"clipped closed contract:{row.key}",
        )
        return {
            "closed": True,
            "method": "CLIPPED_DELTA_THREE_STRATUM",
            "reason": "EXCLUDED",
        }
    return {
        "closed": False,
        "method": "RETAINED",
        "reason": reason,
    }


def fixed_axis_comparison(
    rows: list[Any],
    full_rows: list[Any],
    source_by_origin: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    input_volume = sum((box_volume(row.box) for row in rows), Q(0))
    full_by_origin: Counter[str] = Counter(
        row.origin_key for row in full_rows
    )
    stats: dict[str, dict[str, Any]] = {}
    outcome_rows: dict[str, list[dict[str, Any]]] = {
        axis: [] for axis in AXES
    }
    per_cell_outcomes: list[dict[str, list[dict[str, Any]]]] = []

    for axis_index, axis_name in enumerate(AXES):
        stats[axis_name] = {
            "input_root_count": len(rows),
            "input_volume": input_volume,
            "child_count": 0,
            "closed_child_count": 0,
            "closed_child_volume": Q(0),
            "closed_child_method": Counter(),
            "residual_child_count": 0,
            "residual_child_volume": Q(0),
            "residual_reason_count": Counter(),
            "residual_reason_volume": defaultdict(Q),
            "fully_closed_root_count": 0,
            "partially_closed_root_count": 0,
            "unclosed_root_count": 0,
            "closed_root_count_by_mask": Counter(),
            "closed_child_count_by_mask": Counter(),
            "residual_child_count_by_mask": Counter(),
            "origin_residual_child_count": Counter(full_by_origin),
            "residual_keys": [],
        }

    mask_by_key: dict[str, str] = {}
    for row in rows:
        records = r176.records_for(
            row.chart_id, row.box, row.active_targets
        )
        candidate = [
            record
            for record in records
            if record.classification == "unresolved_discriminant"
        ][0]
        radius = r176.base.arbq(
            r176.base.RADIUS[
                r176.TARGETS[candidate.target_id].obstacle
            ]
        )
        masks: list[str] = []
        if not bool(candidate.ell - radius > 0):
            masks.append(MASK_CLEARANCE)
        if not bool(candidate.ell < r176.base.arbq(r176.base.TAU_MAX)):
            masks.append(MASK_TAU)
        absent = False
        order = False
        for other in records:
            if (
                other.target_id == candidate.target_id
                or other.classification
                in {"no_real_intersection", "intersection_behind"}
            ):
                continue
            lower = r176.earliest_lower(other)
            if lower is None:
                absent = True
            elif not bool(candidate.ell < lower):
                order = True
        if absent:
            masks.append(MASK_LOWER_ABSENT)
        if order:
            masks.append(MASK_ORDER)
        mask_by_key[row.key] = "+".join(masks)

    for index, row in enumerate(rows, 1):
        row_outcomes: dict[str, list[dict[str, Any]]] = {}
        parent_volume = box_volume(row.box)
        mask = mask_by_key[row.key]
        for axis_index, axis_name in enumerate(AXES):
            lower, upper = r176.split(row.box, axis_index)
            require(
                box_volume(lower) + box_volume(upper) == parent_volume,
                f"fixed-axis split volume:{axis_name}:{row.key}",
            )
            children = [
                r187.child_frontier(row, lower),
                r187.child_frontier(row, upper),
            ]
            outcomes = [child_outcome(child) for child in children]
            row_outcomes[axis_name] = outcomes
            axis = stats[axis_name]
            closed_here = sum(
                1 for outcome in outcomes if outcome["closed"]
            )
            axis["child_count"] += 2
            axis["closed_child_count"] += closed_here
            axis["closed_child_volume"] += (
                parent_volume * Q(closed_here, 2)
            )
            axis["residual_child_count"] += 2 - closed_here
            axis["residual_child_volume"] += (
                parent_volume * Q(2 - closed_here, 2)
            )
            axis["closed_child_count_by_mask"][mask] += closed_here
            axis["residual_child_count_by_mask"][mask] += 2 - closed_here
            if closed_here == 2:
                axis["fully_closed_root_count"] += 1
                axis["closed_root_count_by_mask"][mask] += 1
            elif closed_here == 1:
                axis["partially_closed_root_count"] += 1
            else:
                axis["unclosed_root_count"] += 1
            child_summaries: list[dict[str, Any]] = []
            for child, outcome in zip(children, outcomes, strict=True):
                if outcome["closed"]:
                    axis["closed_child_method"][outcome["method"]] += 1
                else:
                    reason = outcome["reason"]
                    volume = box_volume(child.box)
                    axis["residual_reason_count"][reason] += 1
                    axis["residual_reason_volume"][reason] += volume
                    axis["origin_residual_child_count"][
                        row.origin_key
                    ] += 1
                    axis["residual_keys"].append(child.key)
                child_summaries.append({
                    "key": child.key,
                    "closed": outcome["closed"],
                    "method": outcome["method"],
                    "reason": outcome["reason"],
                })
            outcome_rows[axis_name].append({
                "root_key": row.key,
                "origin_key": row.origin_key,
                "failure_mask": mask,
                "children": child_summaries,
            })
        per_cell_outcomes.append(row_outcomes)
        if index % 2500 == 0 or index == len(rows):
            progress(f"fixed t/p/s axes {index}/{len(rows)} cells")

    axis_results: dict[str, dict[str, Any]] = {}
    for axis_name in AXES:
        axis = stats[axis_name]
        require(
            axis["child_count"] == 2 * len(rows)
            and axis["closed_child_count"]
            + axis["residual_child_count"]
            == axis["child_count"]
            and axis["closed_child_volume"]
            + axis["residual_child_volume"]
            == input_volume
            and axis["fully_closed_root_count"]
            + axis["partially_closed_root_count"]
            + axis["unclosed_root_count"]
            == len(rows),
            f"fixed-axis accounting:{axis_name}",
        )
        complete_origins = sorted(
            origin
            for origin in source_by_origin
            if axis["origin_residual_child_count"].get(origin, 0) == 0
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
        require(
            len(complete_origins)
            + len({
                origin
                for origin, count
                in axis["origin_residual_child_count"].items()
                if count > 0
            })
            == len(source_by_origin),
            f"fixed-axis origin accounting:{axis_name}",
        )
        residual_keys = sorted(axis["residual_keys"])
        axis_results[axis_name] = {
            "input_target_failure_root_count": len(rows),
            "input_target_failure_volume": str(input_volume),
            "split_child_count": axis["child_count"],
            "closed_child_count": axis["closed_child_count"],
            "closed_child_volume": str(axis["closed_child_volume"]),
            "closed_child_count_by_method":
                map_counter(axis["closed_child_method"]),
            "residual_child_count": axis["residual_child_count"],
            "residual_child_volume": str(axis["residual_child_volume"]),
            "residual_reason_count":
                map_counter(axis["residual_reason_count"]),
            "residual_reason_volume":
                fraction_map(axis["residual_reason_volume"]),
            "fully_closed_split_root_count":
                axis["fully_closed_root_count"],
            "partially_closed_split_root_count":
                axis["partially_closed_root_count"],
            "unclosed_split_root_count": axis["unclosed_root_count"],
            "fully_closed_root_count_by_failure_mask":
                map_counter(axis["closed_root_count_by_mask"]),
            "closed_child_count_by_failure_mask":
                map_counter(axis["closed_child_count_by_mask"]),
            "residual_child_count_by_failure_mask":
                map_counter(axis["residual_child_count_by_mask"]),
            "Round187_full_p_holdout_count": len(full_rows),
            "geometrically_complete_origin_count": len(complete_origins),
            "geometrically_complete_origin_keys": complete_origins,
            "strict_physical_interior_complete_origin_count":
                len(strict_interior_complete),
            "source_seam_geometrically_complete_but_held_out_count":
                len(seam_complete),
            "residual_origin_count":
                len(source_by_origin) - len(complete_origins),
            "residual_child_keys_sha256": digest(residual_keys),
            "axis_outcome_rows_sha256":
                streaming_list_digest(outcome_rows[axis_name]),
            "exact_split_volume_conservation": True,
        }

    best_stats = {
        "chosen_axis_count": Counter(),
        "tie_axis_set_count": Counter(),
        "best_closed_child_count_per_root": Counter(),
        "closed_child_count": 0,
        "closed_child_volume": Q(0),
        "residual_child_count": 0,
        "residual_child_volume": Q(0),
        "fully_closed_root_count": 0,
        "partially_closed_root_count": 0,
        "unclosed_root_count": 0,
        "residual_reason_count": Counter(),
        "residual_reason_volume": defaultdict(Q),
        "origin_residual_child_count": Counter(full_by_origin),
        "selection_by_mask": defaultdict(Counter),
        "rows": [],
    }
    for row, row_outcomes in zip(rows, per_cell_outcomes, strict=True):
        closed_count = {
            axis: sum(
                1 for outcome in row_outcomes[axis] if outcome["closed"]
            )
            for axis in AXES
        }
        best_count = max(closed_count.values())
        tied = [
            axis for axis in AXES if closed_count[axis] == best_count
        ]
        chosen = tied[0]
        outcomes = row_outcomes[chosen]
        volume = box_volume(row.box)
        mask = mask_by_key[row.key]
        best_stats["chosen_axis_count"][chosen] += 1
        best_stats["tie_axis_set_count"]["+".join(tied)] += 1
        best_stats["best_closed_child_count_per_root"][best_count] += 1
        best_stats["selection_by_mask"][mask][chosen] += 1
        best_stats["closed_child_count"] += best_count
        best_stats["closed_child_volume"] += volume * Q(best_count, 2)
        best_stats["residual_child_count"] += 2 - best_count
        best_stats["residual_child_volume"] += (
            volume * Q(2 - best_count, 2)
        )
        if best_count == 2:
            best_stats["fully_closed_root_count"] += 1
        elif best_count == 1:
            best_stats["partially_closed_root_count"] += 1
        else:
            best_stats["unclosed_root_count"] += 1
        child_rows = []
        lower, upper = r176.split(row.box, AXES.index(chosen))
        for child, outcome in zip(
            (
                r187.child_frontier(row, lower),
                r187.child_frontier(row, upper),
            ),
            outcomes,
            strict=True,
        ):
            if not outcome["closed"]:
                reason = outcome["reason"]
                child_volume = box_volume(child.box)
                best_stats["residual_reason_count"][reason] += 1
                best_stats["residual_reason_volume"][reason] += child_volume
                best_stats["origin_residual_child_count"][
                    row.origin_key
                ] += 1
            child_rows.append({
                "key": child.key,
                "closed": outcome["closed"],
                "method": outcome["method"],
                "reason": outcome["reason"],
            })
        best_stats["rows"].append({
            "root_key": row.key,
            "origin_key": row.origin_key,
            "failure_mask": mask,
            "closed_child_count_by_axis": closed_count,
            "tied_best_axes": tied,
            "post_hoc_chosen_axis": chosen,
            "chosen_children": child_rows,
        })
    require(
        best_stats["closed_child_count"]
        + best_stats["residual_child_count"] == 2 * len(rows)
        and best_stats["closed_child_volume"]
        + best_stats["residual_child_volume"] == input_volume
        and best_stats["fully_closed_root_count"]
        + best_stats["partially_closed_root_count"]
        + best_stats["unclosed_root_count"] == len(rows),
        "post-hoc best-per-cell accounting",
    )
    best_complete_origins = sorted(
        origin
        for origin in source_by_origin
        if best_stats["origin_residual_child_count"].get(origin, 0) == 0
    )
    best_result = {
        "classification":
            "POST_HOC_OUTCOME_DEPENDENT_DIAGNOSTIC_ONLY__"
            "NOT_CERTIFICATE_ADMISSIBLE",
        "why_not_outcome_blind":
            "the axis is chosen after observing child closure outcomes; "
            "a formal selector must be frozen from parent-cell evidence "
            "before child proofs are evaluated",
        "tie_break": "t_then_p_then_s",
        "chosen_axis_count": map_counter(best_stats["chosen_axis_count"]),
        "tied_best_axis_set_count":
            map_counter(best_stats["tie_axis_set_count"]),
        "best_closed_child_count_per_root":
            map_counter(best_stats["best_closed_child_count_per_root"]),
        "closed_child_count": best_stats["closed_child_count"],
        "closed_child_volume": str(best_stats["closed_child_volume"]),
        "residual_child_count": best_stats["residual_child_count"],
        "residual_child_volume": str(best_stats["residual_child_volume"]),
        "fully_closed_split_root_count":
            best_stats["fully_closed_root_count"],
        "partially_closed_split_root_count":
            best_stats["partially_closed_root_count"],
        "unclosed_split_root_count": best_stats["unclosed_root_count"],
        "residual_reason_count":
            map_counter(best_stats["residual_reason_count"]),
        "residual_reason_volume":
            fraction_map(best_stats["residual_reason_volume"]),
        "axis_selection_by_failure_mask":
            nested_counter_map(best_stats["selection_by_mask"]),
        "Round187_full_p_holdout_count": len(full_rows),
        "geometrically_complete_origin_count":
            len(best_complete_origins),
        "geometrically_complete_origin_keys": best_complete_origins,
        "residual_origin_count":
            len(source_by_origin) - len(best_complete_origins),
        "post_hoc_outcome_rows_sha256":
            streaming_list_digest(best_stats["rows"]),
        "official_credit": 0,
    }

    ranking = sorted(
        AXES,
        key=lambda axis: (
            axis_results[axis]["geometrically_complete_origin_count"],
            axis_results[axis]["fully_closed_split_root_count"],
            Q(axis_results[axis]["closed_child_volume"]),
            axis_results[axis]["closed_child_count"],
            -AXES.index(axis),
        ),
        reverse=True,
    )
    return {
        "same_input_all_axes": True,
        "child_decision_order":
            "direct strict terminal first; EXCLUDED closes, LIVE/MIXED "
            "retains; otherwise Round184-equivalent clipped-Delta proof",
        "fixed_axis_results": axis_results,
        "fixed_axis_ranking": ranking,
        "recommended_fixed_axis": ranking[0],
        "post_hoc_best_per_cell": best_result,
    }


def build_probe() -> dict[str, Any]:
    inputs = check_delivery_chain()
    progress("reconstruct exact Round187 depth2 residual")
    residual = rebuild_depth2_residual(inputs)
    require(
        residual["target_volume"] + residual["full_volume"]
        == residual["residual_volume"],
        "Round187 target/full volume partition",
    )

    progress("decompose target_positive_first into explicit failure masks")
    masks = failure_mask_census(residual["target_rows"])

    progress("compare one fixed t/p/s split on identical target-failure cells")
    axes = fixed_axis_comparison(
        residual["target_rows"],
        residual["full_rows"],
        residual["rebuilt"]["source_by_origin"],
    )
    recommended = axes["recommended_fixed_axis"]
    fixed = axes["fixed_axis_results"][recommended]

    result = {
        "status":
            "READ_ONLY_ZERO_PROMOTION_SOURCE_W_STRICT_FIRST_AXIS_PROBE",
        "question":
            "Which single fixed axis best contracts the exact Round187 "
            "depth-2 target-positive-first tail, and which primitive "
            "strict-first inequalities actually fail?",
        "verdict_basis":
            "fixed-axis evidence is certificate-selection-safe as a "
            "comparison only after an axis is globally frozen; post-hoc "
            "best-per-cell evidence is diagnostic and inadmissible",
        "parameters": {
            "Round187_extra_depth_reconstructed": 2,
            "additional_fixed_split_depth": 1,
            "axes_compared": list(AXES),
            "arb_precision_bits": 192,
            "hash_seed_external": "190052",
        },
        "input_chain": {
            "Round180_manifest_sha256":
                ROUND180_PINS[
                    "cm2_round180_full_multi_residual_dimension_safe_partial"
                    "_manifest.sha256"
                ],
            "Round184_manifest_sha256":
                ROUND184_PINS[f"{ROUND184_STEM}_manifest.sha256"],
            "Round184_verification_result_sha256":
                ROUND184_VERIFICATION_RESULT,
            "Round187_source_sha256": ROUND187_SHA256,
            "Round187_used_only_as_probe_library": True,
        },
        "exact_Round187_depth2_residual": {
            "residual_cell_count": len(residual["all_rows"]),
            "target_positive_first_failure_cell_count":
                len(residual["target_rows"]),
            "full_p_graph_holdout_cell_count": len(residual["full_rows"]),
            "origin_count":
                len(residual["residual_rows_by_origin"]),
            "origin_keys_sha256": EXPECTED_ORIGIN_KEYS_SHA256,
            "total_exact_volume": str(residual["residual_volume"]),
            "target_positive_first_failure_exact_volume":
                str(residual["target_volume"]),
            "full_p_graph_holdout_exact_volume":
                str(residual["full_volume"]),
            "residual_cell_keys_sha256":
                EXPECTED_DEPTH2_RESIDUAL_KEYS_SHA256,
            "exact_count_and_volume_partition_reconfirmed": True,
        },
        "target_positive_first_failure_masks": masks,
        "one_split_fixed_axis_comparison": axes,
        "recommendation": {
            "best_fixed_axis_for_this_equal-input_spike": recommended,
            "best_fixed_axis_closed_child_count":
                fixed["closed_child_count"],
            "best_fixed_axis_fully_closed_split_root_count":
                fixed["fully_closed_split_root_count"],
            "best_fixed_axis_geometrically_complete_origin_count":
                fixed["geometrically_complete_origin_count"],
            "next_certificate_admissible_axis_criterion":
                "freeze a deterministic parent-only selector from the "
                "failure-mask class and predicted interval-width contraction "
                "of ell-radius, TAU_MAX-ell, and competitor_lower-ell; "
                "resolve ties t,p,s; then evaluate child proofs",
            "full_p_next_method":
                "separate explicit first-root-equality continuation for the "
                "64 full-p holdouts",
        },
        "zero_promotion_contract": {
            "probe_only": True,
            "filesystem_writes": 0,
            "official_ledger_mutated": False,
            "probe_counts_applied_to_official_ledger": False,
            "whole_origin_integer_credit_issued": 0,
            "post_hoc_best_per_cell_credit_issued": 0,
            "D02": "UNCHANGED_BLOCKED",
            "D03_negative_oracle": "UNCHANGED_UNAUTHORIZED",
            "Gate5": "UNCHANGED_10_OF_18",
            "complete_18_field_blocks": 0,
            "CM2": "UNCHANGED_NO_GO",
            "required_before_any_ledger_use":
                "formal producer with outcome-blind selector plus "
                "independent non-importing verifier",
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
