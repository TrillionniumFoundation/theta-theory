#!/usr/bin/env python3
"""Read-only exact-behind candidate-removal probe for the source-W tail.

This probe treats all 37,262 Round187 depth-2 residual cells uniformly,
including both the 37,198 clipped cells and the 64 full-p holdouts.  It does
not require a Delta graph to exist.  On each whole closed box it checks

    ell < 0 and distance^2 - R^2 = ell^2 - Delta > 0.

For Delta < 0 there is no real root.  For Delta >= 0 the inequalities imply
``far = ell + sqrt(Delta) < 0``.  Thus the candidate has no future root on
the complete box and can be deleted before independently rebuilding the
remaining-record disposition, owner, and outgoing chart.

This is diagnostic only: no formal ledger is changed, no output-path option
exists, no filesystem write is performed, progress goes to stderr, and one
final JSON document goes to stdout.
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
SCHEMA = "cm2.round194.source-w-exact-behind-target-removal-probe.v1"
MAX_INPUT_BYTES = 8 * 1024 * 1024

ROUND187_NAME = "cm2_round187_source_w_strict_first_refinement_probe.py"
ROUND187_SHA256 = (
    "6278b744f091657ff6035dc71a5656ba1ae861d3b672b591e6a77d718864c5cc"
)
ROUND190_NAME = "cm2_round190_source_w_strict_first_axis_probe.py"
ROUND190_SHA256 = (
    "722e155df1ec992fc837603997151cda79e938b241c4761c5a958ee7665ad397"
)
ROUND193_NAME = "cm2_round193_source_w_exact_near_positivity_probe.py"
ROUND193_SHA256 = (
    "fca55b9f9a28aeda65f2e4a5a2305e704f198b3f08d10891fe607f46273f3a52"
)

EXPECTED_ORIGIN_COUNT = 162
EXPECTED_ORIGIN_KEYS_SHA256 = (
    "c86ec3a7042b6aaa58eee59ec43a6ec2ebda8bd192cedfcf4c47d8c42c4615c3"
)
EXPECTED_CLIPPED_COUNT = 37198
EXPECTED_FULL_P_COUNT = 64
EXPECTED_TOTAL_COUNT = 37262
EXPECTED_TOTAL_VOLUME = Q(3297687, 838860800000)
EXPECTED_TOTAL_KEYS_SHA256 = (
    "060ac08ec0ccb026ad4cf735a4ebe5af30753a690e7fbe80a4b95f25de3be19e"
)

CLIPPED_INPUT = "ROUND187_TARGET_FIRST_CLIPPED"
FULL_P_INPUT = "ROUND187_FULL_P_HOLDOUT"

ELL_NOT_NEGATIVE = "ELL_NOT_STRICT_NEGATIVE"
DISTANCE_NOT_POSITIVE = (
    "DISTANCE_SQUARED_MINUS_RADIUS_SQUARED_NOT_STRICT_POSITIVE"
)
REDUCED_DISPOSITION_NOT_EXCLUDED = (
    "REDUCED_REMAINING_RECORD_DISPOSITION_NOT_EXCLUDED"
)
FAILURE_ORDER = (
    ELL_NOT_NEGATIVE,
    DISTANCE_NOT_POSITIVE,
    REDUCED_DISPOSITION_NOT_EXCLUDED,
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


def pin_probe(name: str, expected: str, label: str) -> None:
    require(
        hashlib.sha256(read_regular(HERE / name)).hexdigest() == expected,
        f"{label} source pin",
    )


pin_probe(ROUND187_NAME, ROUND187_SHA256, "Round187")
pin_probe(ROUND190_NAME, ROUND190_SHA256, "Round190")
pin_probe(ROUND193_NAME, ROUND193_SHA256, "Round193")
if os.fspath(HERE) not in sys.path:
    sys.path.insert(0, os.fspath(HERE))
r193 = importlib.import_module(
    "cm2_round193_source_w_exact_near_positivity_probe"
)
pin_probe(ROUND187_NAME, ROUND187_SHA256, "Round187 post-import")
pin_probe(ROUND190_NAME, ROUND190_SHA256, "Round190 post-import")
pin_probe(ROUND193_NAME, ROUND193_SHA256, "Round193 post-import")
r190 = r193.r190
r187 = r193.r187
r180 = r193.r180
r176 = r193.r176


def check_chain() -> dict[str, Any]:
    require(
        Path(r193.__file__).resolve() == (HERE / ROUND193_NAME).resolve()
        and r193.ROUND190_SHA256 == ROUND190_SHA256
        and r193.ROUND187_SHA256 == ROUND187_SHA256,
        "Round193 module identity and embedded pins",
    )
    return r193.check_chain()


def box_volume(box: Any) -> Q:
    return (
        (box.t1 - box.t0)
        * (box.p1 - box.p0)
        * (box.s1 - box.s0)
    )


def remaining_outgoing_chart(
    row: Any,
    leaf: Any,
) -> tuple[str, bool]:
    if (
        leaf.classification != "unique_first"
        or leaf.owner_target != r176.FROZEN_OWNER
    ):
        return "NOT_APPLICABLE", True
    chart, _margins = r176.outgoing_generic(row.chart_id, row.box)
    if chart is None:
        return "OVERWRAP", False
    return chart, True


def evaluate_cell(row: Any, input_class: str) -> dict[str, Any]:
    records = r176.records_for(
        row.chart_id, row.box, row.active_targets
    )
    unresolved = [
        record
        for record in records
        if record.classification == "unresolved_discriminant"
    ]
    require(len(unresolved) == 1, f"unresolved candidate:{row.key}")
    candidate = unresolved[0]

    original_proof, original_reason = r187.clipped_partition_proof(row)
    expected_reason = (
        r187.TARGET_FAILURE
        if input_class == CLIPPED_INPUT
        else "NOT_CLIPPED_FULL_P_GRAPH"
    )
    require(
        original_proof is None and original_reason == expected_reason,
        f"Round187 input class:{row.key}:{original_reason}",
    )

    distance = r193.exact_distance_evidence(row, candidate)
    failures: set[str] = set()
    if not distance["ell_negative"]:
        failures.add(ELL_NOT_NEGATIVE)
    if not distance["distance_positive"]:
        failures.add(DISTANCE_NOT_POSITIVE)

    remaining_records = [
        record
        for record in records
        if record.target_id != candidate.target_id
    ]
    remaining_leaf = r176.classify_records(
        row.chart_id, row.box, remaining_records
    )
    disposition, _margins = r176.terminal_disposition(
        row.chart_id, remaining_leaf
    )
    independently_wrapped = r176.remove_disposition(
        row, records, candidate.target_id
    )
    require(
        disposition == independently_wrapped,
        f"remaining disposition cross-check:{row.key}",
    )
    if disposition is None or not disposition.startswith("EXCLUDED"):
        failures.add(REDUCED_DISPOSITION_NOT_EXCLUDED)

    outgoing_chart, chart_resolved = remaining_outgoing_chart(
        row, remaining_leaf
    )
    if (
        remaining_leaf.classification == "unique_first"
        and remaining_leaf.owner_target == r176.FROZEN_OWNER
        and disposition is not None
    ):
        if disposition.startswith("EXCLUDED_OUTGOING_CHART_MISMATCH"):
            require(
                chart_resolved
                and outgoing_chart != r176.FROZEN_CHART,
                f"remaining excluded chart:{row.key}",
            )
        elif disposition.startswith("LIVE_FROZEN_STAGE_ONE_OWNER_CHART_MATCH"):
            require(
                chart_resolved
                and outgoing_chart == r176.FROZEN_CHART,
                f"remaining live chart:{row.key}",
            )

    ordered_failures = [
        reason for reason in FAILURE_ORDER if reason in failures
    ]
    require(
        len(ordered_failures) == len(failures),
        f"failure ordering:{row.key}",
    )
    behind_proved = (
        distance["ell_negative"] and distance["distance_positive"]
    )
    whole_closed = behind_proved and (
        disposition is not None
        and disposition.startswith("EXCLUDED")
    )
    require(
        whole_closed == (not ordered_failures),
        f"whole closure equivalence:{row.key}",
    )

    record_classes = Counter(
        record.classification for record in remaining_records
    )
    return {
        "cell_key": row.key,
        "origin_key": row.origin_key,
        "input_class": input_class,
        "candidate_target": candidate.target_id,
        "candidate_obstacle":
            r176.TARGETS[candidate.target_id].obstacle,
        "candidate_Delta_sign": r193.sign_name(
            candidate.discriminant
        ),
        "ell_sign": distance["ell_sign"],
        "direct_distance_margin_sign": distance["direct_sign"],
        "identity_margin_sign": distance["identity_sign"],
        "direct_identity_interval_overlap":
            distance["interval_enclosures_overlap"],
        "exact_far_negative_on_Delta_nonnegative":
            distance["exact_far_negative_on_Delta_nonnegative"],
        "whole_box_no_future_root_contract":
            (
                "Delta<0:no real root; Delta>=0:ell<0 and "
                "ell^2-Delta>0 imply far<0"
            ),
        "candidate_deleted_before_reclassification": True,
        "remaining_record_count": len(remaining_records),
        "remaining_record_classification_count":
            map_counter(record_classes),
        "remaining_leaf_classification":
            remaining_leaf.classification,
        "remaining_owner_target":
            (
                remaining_leaf.owner_target
                if remaining_leaf.owner_target is not None
                else "NONE"
            ),
        "remaining_active_targets":
            list(remaining_leaf.active_targets),
        "remaining_tangency_targets":
            list(remaining_leaf.tangency_targets),
        "remaining_outgoing_chart": outgoing_chart,
        "remaining_disposition": (
            disposition if disposition is not None else "UNRESOLVED"
        ),
        "failure_reasons": ordered_failures,
        "whole_closed_cell_excluded": whole_closed,
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


def analyze(
    residual: dict[str, Any],
) -> dict[str, Any]:
    classified_rows = (
        [(row, CLIPPED_INPUT) for row in residual["target_rows"]]
        + [(row, FULL_P_INPUT) for row in residual["full_rows"]]
    )
    classified_rows.sort(key=lambda item: item[0].key)
    source_by_origin = residual["rebuilt"]["source_by_origin"]

    input_count: Counter[str] = Counter()
    input_volume: defaultdict[str, Q] = defaultdict(Q)
    closed_count: Counter[str] = Counter()
    closed_volume: defaultdict[str, Q] = defaultdict(Q)
    residual_count: Counter[str] = Counter()
    residual_volume: defaultdict[str, Q] = defaultdict(Q)
    failure_combinations: Counter[str] = Counter()
    candidate_targets: Counter[str] = Counter()
    candidate_targets_by_input: dict[str, Counter[str]] = defaultdict(Counter)
    delta_signs: Counter[str] = Counter()
    ell_signs: Counter[str] = Counter()
    direct_signs: Counter[str] = Counter()
    identity_signs: Counter[str] = Counter()
    behind_counts: Counter[str] = Counter()
    remaining_leaf_classes: Counter[str] = Counter()
    remaining_owner_targets: Counter[str] = Counter()
    remaining_outgoing_charts: Counter[str] = Counter()
    remaining_dispositions: Counter[str] = Counter()
    remaining_active_count: Counter[int] = Counter()
    remaining_record_classes: Counter[str] = Counter()
    disposition_by_input: dict[str, Counter[str]] = defaultdict(Counter)
    residual_by_origin: Counter[str] = Counter()
    closed_keys: list[str] = []
    residual_keys: list[str] = []
    evidence_rows: list[dict[str, Any]] = []

    for index, (row, input_class) in enumerate(classified_rows, 1):
        evidence = evaluate_cell(row, input_class)
        volume = box_volume(row.box)
        input_count[input_class] += 1
        input_volume[input_class] += volume
        candidate = evidence["candidate_target"]
        candidate_targets[candidate] += 1
        candidate_targets_by_input[input_class][candidate] += 1
        delta_signs[evidence["candidate_Delta_sign"]] += 1
        ell_signs[evidence["ell_sign"]] += 1
        direct_signs[evidence["direct_distance_margin_sign"]] += 1
        identity_signs[evidence["identity_margin_sign"]] += 1
        behind_counts[
            "PASS"
            if evidence["exact_far_negative_on_Delta_nonnegative"]
            else "FAIL"
        ] += 1
        remaining_leaf_classes[
            evidence["remaining_leaf_classification"]
        ] += 1
        remaining_owner_targets[
            evidence["remaining_owner_target"]
        ] += 1
        remaining_outgoing_charts[
            evidence["remaining_outgoing_chart"]
        ] += 1
        remaining_dispositions[
            evidence["remaining_disposition"]
        ] += 1
        remaining_active_count[
            len(evidence["remaining_active_targets"])
        ] += 1
        for classification, count in evidence[
            "remaining_record_classification_count"
        ].items():
            remaining_record_classes[classification] += count
        disposition_by_input[input_class][
            evidence["remaining_disposition"]
        ] += 1

        failures = evidence["failure_reasons"]
        combination = (
            "+".join(failures) if failures else "NONE__CLOSED"
        )
        failure_combinations[combination] += 1
        if evidence["whole_closed_cell_excluded"]:
            closed_count[input_class] += 1
            closed_volume[input_class] += volume
            closed_keys.append(row.key)
        else:
            residual_count[input_class] += 1
            residual_volume[input_class] += volume
            residual_by_origin[row.origin_key] += 1
            residual_keys.append(row.key)
        evidence_rows.append(evidence)
        if index % 2500 == 0 or index == len(classified_rows):
            progress(
                f"exact behind removal {index}/{len(classified_rows)}"
            )

    total_input_volume = sum(input_volume.values(), Q(0))
    total_closed_volume = sum(closed_volume.values(), Q(0))
    total_residual_volume = sum(residual_volume.values(), Q(0))
    require(
        sum(input_count.values()) == EXPECTED_TOTAL_COUNT
        and sum(closed_count.values())
        + sum(residual_count.values()) == EXPECTED_TOTAL_COUNT
        and total_input_volume == EXPECTED_TOTAL_VOLUME
        and total_closed_volume + total_residual_volume
        == total_input_volume,
        "global count and exact-volume conservation",
    )
    for input_class in (CLIPPED_INPUT, FULL_P_INPUT):
        require(
            closed_count[input_class] + residual_count[input_class]
            == input_count[input_class]
            and closed_volume[input_class] + residual_volume[input_class]
            == input_volume[input_class],
            f"input-class conservation:{input_class}",
        )

    complete_origins = sorted(
        origin
        for origin in source_by_origin
        if residual_by_origin.get(origin, 0) == 0
    )
    residual_origins = sorted(
        origin
        for origin in source_by_origin
        if residual_by_origin.get(origin, 0) > 0
    )
    strict_interior_complete = sorted(
        origin
        for origin in complete_origins
        if source_by_origin[origin]["classification"]
        == r187.SOURCE_INTERIOR
    )
    seam_complete = sorted(
        origin
        for origin in complete_origins
        if source_by_origin[origin]["classification"]
        == r187.SOURCE_SEAM
    )
    full_p_origins = sorted({
        row.origin_key for row in residual["full_rows"]
    })
    full_p_strict = sorted(
        set(full_p_origins) & set(strict_interior_complete)
    )
    full_p_seam = sorted(
        set(full_p_origins) & set(seam_complete)
    )
    require(
        len(complete_origins) + len(residual_origins)
        == len(source_by_origin) == EXPECTED_ORIGIN_COUNT
        and len(strict_interior_complete) + len(seam_complete)
        == len(complete_origins),
        "origin and source-domain partition",
    )
    all_full_p_behind = (
        closed_count[FULL_P_INPUT] == EXPECTED_FULL_P_COUNT
    )
    verdict = (
        "VALIDATED"
        if sum(closed_count.values()) == EXPECTED_TOTAL_COUNT
        else "PARTIAL"
        if sum(closed_count.values())
        else "INVALIDATED"
    )
    return {
        "spike_verdict": verdict,
        "input_count_by_class": map_counter(input_count),
        "input_exact_volume_by_class": fraction_map(input_volume),
        "closed_whole_cell_count_by_class":
            map_counter(closed_count),
        "closed_whole_cell_exact_volume_by_class":
            fraction_map(closed_volume),
        "residual_cell_count_by_class": map_counter(residual_count),
        "residual_cell_exact_volume_by_class":
            fraction_map(residual_volume),
        "total_input_cell_count": sum(input_count.values()),
        "total_input_exact_volume": str(total_input_volume),
        "total_closed_whole_cell_count": sum(closed_count.values()),
        "total_closed_whole_cell_exact_volume":
            str(total_closed_volume),
        "total_residual_cell_count": sum(residual_count.values()),
        "total_residual_cell_exact_volume":
            str(total_residual_volume),
        "failure_combination_count":
            map_counter(failure_combinations),
        "candidate_target_count": map_counter(candidate_targets),
        "candidate_target_count_by_input_class":
            nested_counter_map(candidate_targets_by_input),
        "candidate_Delta_sign_count": map_counter(delta_signs),
        "ell_sign_count": map_counter(ell_signs),
        "direct_distance_margin_sign_count":
            map_counter(direct_signs),
        "identity_margin_sign_count": map_counter(identity_signs),
        "exact_behind_contract_count":
            map_counter(behind_counts),
        "remaining_leaf_classification_count":
            map_counter(remaining_leaf_classes),
        "remaining_owner_target_count":
            map_counter(remaining_owner_targets),
        "remaining_outgoing_chart_count":
            map_counter(remaining_outgoing_charts),
        "remaining_disposition_count":
            map_counter(remaining_dispositions),
        "remaining_disposition_count_by_input_class":
            nested_counter_map(disposition_by_input),
        "remaining_active_target_count_per_cell":
            map_counter(remaining_active_count),
        "remaining_record_classification_occurrence":
            map_counter(remaining_record_classes),
        "closed_cell_keys_sha256": digest(sorted(closed_keys)),
        "residual_cell_keys_sha256": digest(sorted(residual_keys)),
        "per_cell_evidence_rows_sha256":
            streaming_list_digest(evidence_rows),
        "whole_origin_and_source_domain_outcome": {
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
            "strict_physical_interior_complete_origin_keys_sha256":
                digest(strict_interior_complete),
            "source_seam_geometrically_complete_but_held_out_count":
                len(seam_complete),
            "source_seam_geometrically_complete_but_held_out_keys":
                seam_complete,
            "source_seam_geometrically_complete_keys_sha256":
                digest(seam_complete),
            "residual_origin_count": len(residual_origins),
            "residual_origin_keys": residual_origins,
            "residual_origin_keys_sha256":
                digest(residual_origins),
            "full_p_origin_count": len(full_p_origins),
            "full_p_origin_keys": full_p_origins,
            "full_p_origin_keys_sha256": digest(full_p_origins),
            "full_p_strict_interior_origin_count":
                len(full_p_strict),
            "full_p_source_seam_origin_count": len(full_p_seam),
            "official_whole_origin_credit": 0,
        },
        "rule_generality": {
            "all_64_full_p_cells_exact_behind_and_removed":
                all_full_p_behind,
            "Delta_graph_existence_or_topology_used": False,
            "clipped_vs_full_p_used_only_as_input_accounting": True,
            "eligible_next_scan_if_all_full_p_pass":
                (
                    "MIXED_AND_ROOT_EQUALITY_PRIORITY_REGISTRY"
                    if all_full_p_behind
                    else "REMAINING_FULL_P_FAILURES_FIRST"
                ),
            "generality_limit":
                "each future cell must independently prove ell<0, "
                "distance^2-R^2>0, and excluded reduced disposition",
        },
        "exact_count_and_volume_conservation": True,
    }


def build_probe() -> dict[str, Any]:
    inputs = check_chain()
    progress("reconstruct exact Round187 depth2 residual")
    residual = r190.rebuild_depth2_residual(inputs)
    require(
        len(residual["target_rows"]) == EXPECTED_CLIPPED_COUNT
        and len(residual["full_rows"]) == EXPECTED_FULL_P_COUNT
        and len(residual["all_rows"]) == EXPECTED_TOTAL_COUNT
        and residual["residual_volume"] == EXPECTED_TOTAL_VOLUME
        and digest([row.key for row in residual["all_rows"]])
        == EXPECTED_TOTAL_KEYS_SHA256
        and len(residual["residual_rows_by_origin"])
        == EXPECTED_ORIGIN_COUNT
        and digest(sorted(residual["residual_rows_by_origin"]))
        == EXPECTED_ORIGIN_KEYS_SHA256,
        "exact Round187 residual input",
    )
    progress("prove exact behind and rebuild reduced dispositions")
    analysis = analyze(residual)

    result = {
        "status":
            "READ_ONLY_ZERO_PROMOTION_SOURCE_W_EXACT_BEHIND_REMOVAL_PROBE",
        "spike_verdict": analysis["spike_verdict"],
        "question":
            "Can exact far-negative geometry remove the unresolved "
            "candidate uniformly on all clipped and full-p residual cells?",
        "parameters": {
            "arb_precision_bits": 192,
            "hash_seed_external": "194052",
            "Round187_extra_depth_reconstructed": 2,
            "additional_refinement_depth": 0,
        },
        "input_chain": {
            "Round187_source_sha256": ROUND187_SHA256,
            "Round190_source_sha256": ROUND190_SHA256,
            "Round193_source_sha256": ROUND193_SHA256,
            "all_imported_rounds_used_only_as_probe_libraries": True,
        },
        "exact_Round187_depth2_residual": {
            "clipped_cell_count": len(residual["target_rows"]),
            "full_p_holdout_cell_count": len(residual["full_rows"]),
            "total_cell_count": len(residual["all_rows"]),
            "origin_count": len(residual["residual_rows_by_origin"]),
            "origin_keys_sha256": EXPECTED_ORIGIN_KEYS_SHA256,
            "clipped_exact_volume": str(residual["target_volume"]),
            "full_p_exact_volume": str(residual["full_volume"]),
            "total_exact_volume": str(residual["residual_volume"]),
            "all_cell_keys_sha256": EXPECTED_TOTAL_KEYS_SHA256,
            "exact_count_and_volume_partition_reconfirmed": True,
        },
        "exact_behind_target_removal_analysis": analysis,
        "mathematical_contract": {
            "whole_closed_box":
                "for every point, Delta<0 gives no real root; Delta>=0 "
                "with ell<0 and ell^2-Delta>0 gives far<0",
            "candidate_future_root_conclusion":
                "candidate has no future root anywhere on the closed box",
            "reduced_reclassification":
                "delete candidate, rebuild classify_records, owner, "
                "outgoing chart, and terminal_disposition",
            "Delta_graph_existence_not_required": True,
            "Delta_graph_topology_not_required": True,
            "lower_dimensional_nonpromotion":
                "no graph incidence, nonemptiness, or integer credit inferred",
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
                "formal producer with complete dimension ledgers plus "
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
