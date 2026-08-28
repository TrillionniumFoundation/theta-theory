#!/usr/bin/env python3
"""Fail-closed structural verifier for the CM2 Gate 3/4 evidence package.

This verifier does not prove interval or algebraic claims merely because they
are named in a JSON file.  It checks that a global event inventory has the
finite coverage, incidence, current, and same-occurrence records that a
mathematical certificate must then substantiate.  Missing data are therefore
reported as hard NOT_CERTIFIED findings.

The bundled evidence snapshot is intentionally incomplete.  Running this
file on it must exit nonzero.  ``--self-test`` checks both rejection of that
snapshot and acceptance of a tiny *structural* fixture; the latter is only a
test of the verifier and is not a CM2 certificate.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable


SCHEMA = "cm2.gates34.event-q.v1"
ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST = Path(__file__).with_name(
    "cm2-gates34-event-q-manifest-2026-07-15.json"
)


@dataclass(frozen=True)
class Finding:
    gate: int
    code: str
    detail: str


def add(out: list[Finding], gate: int, code: str, detail: str) -> None:
    out.append(Finding(gate, code, detail))


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def positive_rational(value: Any) -> bool:
    if not nonempty_string(value):
        return False
    try:
        return Fraction(value) > 0
    except (ValueError, ZeroDivisionError):
        return False


def canonical_digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def check_provenance(data: dict[str, Any], out: list[Finding]) -> None:
    for index, row in enumerate(data.get("provenance", [])):
        path_value = row.get("path")
        expected = row.get("sha256")
        if not nonempty_string(path_value) or not nonempty_string(expected):
            add(out, 3, "PROVENANCE_ROW_INCOMPLETE", f"provenance[{index}]")
            continue
        path = ROOT / path_value
        if not path.is_file():
            add(out, 3, "PROVENANCE_FILE_MISSING", path_value)
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            add(
                out,
                3,
                "PROVENANCE_HASH_MISMATCH",
                f"{path_value}: expected {expected}, got {actual}",
            )


def unique_rows(
    rows: Any, key: str, gate: int, prefix: str, out: list[Finding]
) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    if not isinstance(rows, list):
        add(out, gate, f"{prefix}_NOT_LIST", f"{prefix} must be a list")
        return result
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or not nonempty_string(row.get(key)):
            add(out, gate, f"{prefix}_ROW_ID_MISSING", f"{prefix}[{index}].{key}")
            continue
        row_id = row[key]
        if row_id in result:
            add(out, gate, f"{prefix}_DUPLICATE_ID", row_id)
        else:
            result[row_id] = row
    return result


def all_pairs(values: Iterable[str]) -> set[tuple[str, str]]:
    return {tuple(sorted(pair)) for pair in itertools.combinations(sorted(values), 2)}


def all_triples(values: Iterable[str]) -> set[tuple[str, str, str]]:
    return {tuple(sorted(triple)) for triple in itertools.combinations(sorted(values), 3)}


def target_universe(gate: dict[str, Any], out: list[Finding]) -> dict[str, dict[str, Any]]:
    """Read explicit target rows and expand certified rectangular families."""

    targets = unique_rows(gate.get("target_lifts", []), "target_id", 3, "TARGET_LIFT", out)
    families = gate.get("target_lift_families", [])
    if not isinstance(families, list):
        add(out, 3, "TARGET_FAMILY_NOT_LIST", "target_lift_families")
        return targets
    for index, family in enumerate(families):
        if not isinstance(family, dict):
            add(out, 3, "TARGET_FAMILY_ROW_INVALID", f"family[{index}]")
            continue
        family_id = family.get("family_id")
        obstacle = family.get("obstacle")
        lower = family.get("index_min")
        upper = family.get("index_max")
        if not nonempty_string(family_id) or not nonempty_string(obstacle):
            add(out, 3, "TARGET_FAMILY_ID_MISSING", f"family[{index}]")
            continue
        if (
            not isinstance(lower, list)
            or not isinstance(upper, list)
            or len(lower) != 2
            or len(upper) != 2
            or not all(isinstance(value, int) for value in lower + upper)
            or lower[0] > upper[0]
            or lower[1] > upper[1]
        ):
            add(out, 3, "TARGET_FAMILY_RANGE_INVALID", family_id)
            continue
        for field in ("center_formula", "radius", "family_certificate"):
            if not nonempty_string(family.get(field)):
                add(out, 3, "TARGET_FAMILY_FIELD_MISSING", f"{family_id}.{field}")
        for ix in range(lower[0], upper[0] + 1):
            for iy in range(lower[1], upper[1] + 1):
                target_id = f"{obstacle}[{ix},{iy}]"
                if target_id in targets:
                    add(out, 3, "TARGET_LIFT_DUPLICATE_ID", target_id)
                    continue
                targets[target_id] = {
                    "target_id": target_id,
                    "obstacle": obstacle,
                    "lift": [ix, iy],
                    "center_formula": family.get("center_formula"),
                    "radius": family.get("radius"),
                }
    return targets


def check_gate3(data: dict[str, Any], out: list[Finding]) -> set[str]:
    gate = data.get("gate3", {})
    horizon = gate.get("horizon", {})
    if not positive_rational(horizon.get("tau_min_lower")):
        add(out, 3, "TAU_MIN_NOT_CERTIFIED", "positive exact lower bound absent")
    if not positive_rational(horizon.get("tau_max_upper")):
        add(
            out,
            3,
            "TAU_MAX_NOT_CERTIFIED",
            "a numerical upper flight bound is needed to enumerate torus lifts",
        )
    if not nonempty_string(horizon.get("tau_max_certificate")):
        add(out, 3, "TAU_MAX_PROOF_MISSING", "no finite-horizon lift certificate")

    charts = unique_rows(gate.get("source_charts"), "chart_id", 3, "SOURCE_CHART", out)
    if not charts:
        add(out, 3, "SOURCE_ATLAS_EMPTY", "no solid-boundary source chart rows")
    if not nonempty_string(gate.get("source_cover_certificate")):
        add(out, 3, "SOURCE_COVER_MISSING", "chart union/disjoint-interior proof absent")
    for chart_id, chart in charts.items():
        for field in ("component", "domain", "gauge", "coverage_cell"):
            if not nonempty_string(chart.get(field)):
                add(out, 3, "SOURCE_CHART_FIELD_MISSING", f"{chart_id}.{field}")
        if not isinstance(chart.get("candidate_target_ids"), list):
            add(out, 3, "SOURCE_TARGET_LIST_MISSING", chart_id)

    targets = target_universe(gate, out)
    if not targets:
        add(out, 3, "TARGET_LIFT_SET_EMPTY", "no finite physical target-lift rows")
    if not nonempty_string(gate.get("target_lift_completeness_certificate")):
        add(out, 3, "TARGET_LIFT_COMPLETENESS_MISSING", "finite lift coverage absent")
    for target_id, target in targets.items():
        for field in ("obstacle", "lift", "center_formula", "radius"):
            if target.get(field) in (None, "", []):
                add(out, 3, "TARGET_LIFT_FIELD_MISSING", f"{target_id}.{field}")

    expected_event_keys: set[tuple[str, str]] = set()
    for chart_id, chart in charts.items():
        raw_candidate_ids = chart.get("candidate_target_ids", [])
        candidate_ids = raw_candidate_ids if isinstance(raw_candidate_ids, list) else []
        for target_id in candidate_ids:
            if target_id not in targets:
                add(out, 3, "UNKNOWN_CHART_TARGET", f"{chart_id}:{target_id}")
            else:
                expected_event_keys.add((chart_id, target_id))

    events = unique_rows(gate.get("event_rows"), "event_id", 3, "EVENT", out)
    actual_event_keys: set[tuple[str, str]] = set()
    occurrence_ids: set[str] = set()
    face_labels: set[str] = set()
    for event_id, event in events.items():
        chart_id = event.get("source_chart_id")
        target_id = event.get("target_id")
        if nonempty_string(chart_id) and nonempty_string(target_id):
            key = (chart_id, target_id)
            if key in actual_event_keys:
                add(out, 3, "EVENT_KEY_DUPLICATE", f"{chart_id}:{target_id}")
            actual_event_keys.add(key)
        else:
            add(out, 3, "EVENT_KEY_MISSING", event_id)
        required = (
            "event_equation",
            "squarefree_factor",
            "selected_root",
            "occurrence_time",
            "first_hit_certificate",
            "face_label",
            "submersion_certificate",
            "coarea_coefficient",
            "physical_trace",
            "polarity",
            "owner",
            "m_id",
            "q_id",
            "occurrence_id",
            "scalar_current_certificate",
        )
        for field in required:
            if not nonempty_string(event.get(field)):
                add(out, 3, "EVENT_FIELD_MISSING", f"{event_id}.{field}")
        if not positive_rational(event.get("submersion_lower")):
            add(out, 3, "EVENT_SUBMERSION_MARGIN_MISSING", event_id)
        label = event.get("face_label")
        if nonempty_string(label):
            if label in face_labels:
                add(out, 3, "FACE_LABEL_NOT_UNIQUE", label)
            face_labels.add(label)
        occurrence_id = event.get("occurrence_id")
        if nonempty_string(occurrence_id):
            occurrence_ids.add(occurrence_id)

    missing_events = expected_event_keys - actual_event_keys
    extra_events = actual_event_keys - expected_event_keys
    if missing_events:
        add(out, 3, "EVENT_ROWS_MISSING", repr(sorted(missing_events)))
    if extra_events:
        add(out, 3, "EVENT_ROWS_OUTSIDE_UNIVERSE", repr(sorted(extra_events)))
    if not events:
        add(out, 3, "EVENT_INVENTORY_EMPTY", "the tangency formula is only a template")

    expected_pairs: set[tuple[str, str, str]] = set()
    expected_triples: set[tuple[str, str, str, str]] = set()
    for chart_id, chart in charts.items():
        raw_candidate_ids = chart.get("candidate_target_ids", [])
        candidate_ids = raw_candidate_ids if isinstance(raw_candidate_ids, list) else []
        valid_targets = [x for x in candidate_ids if x in targets]
        expected_pairs |= {(chart_id, *pair) for pair in all_pairs(valid_targets)}
        expected_triples |= {(chart_id, *triple) for triple in all_triples(valid_targets)}

    pair_rows = gate.get("pair_incidence_rows", [])
    actual_pairs: set[tuple[str, str, str]] = set()
    if not isinstance(pair_rows, list):
        add(out, 3, "PAIR_TABLE_NOT_LIST", "pair_incidence_rows")
    else:
        allowed = {"empty", "regular_noncoincident", "duplicate_cancelled", "joint_normal_form"}
        for index, row in enumerate(pair_rows):
            ids = row.get("target_ids", []) if isinstance(row, dict) else []
            if len(ids) != 2 or not nonempty_string(row.get("source_chart_id")):
                add(out, 3, "PAIR_ROW_KEY_MISSING", f"pair[{index}]")
                continue
            key = (row["source_chart_id"], *sorted(ids))
            actual_pairs.add(key)
            if row.get("classification") not in allowed:
                add(out, 3, "PAIR_CLASSIFICATION_MISSING", repr(key))
            if not nonempty_string(row.get("certificate")):
                add(out, 3, "PAIR_CERTIFICATE_MISSING", repr(key))
    if expected_pairs - actual_pairs:
        add(out, 3, "PAIR_TABLE_INCOMPLETE", repr(sorted(expected_pairs - actual_pairs)))

    triple_rows = gate.get("triple_incidence_rows", [])
    actual_triples: set[tuple[str, str, str, str]] = set()
    if not isinstance(triple_rows, list):
        add(out, 3, "TRIPLE_TABLE_NOT_LIST", "triple_incidence_rows")
    else:
        for index, row in enumerate(triple_rows):
            ids = row.get("target_ids", []) if isinstance(row, dict) else []
            if len(ids) != 3 or not nonempty_string(row.get("source_chart_id")):
                add(out, 3, "TRIPLE_ROW_KEY_MISSING", f"triple[{index}]")
                continue
            key = (row["source_chart_id"], *sorted(ids))
            actual_triples.add(key)
            if not nonempty_string(row.get("classification")):
                add(out, 3, "TRIPLE_CLASSIFICATION_MISSING", repr(key))
            if not nonempty_string(row.get("certificate")):
                add(out, 3, "TRIPLE_CERTIFICATE_MISSING", repr(key))
    if expected_triples - actual_triples:
        add(
            out,
            3,
            "TRIPLE_TABLE_INCOMPLETE",
            repr(sorted(expected_triples - actual_triples)),
        )

    for field, code in (
        ("event_cover_certificate", "EVENT_COVER_CERTIFICATE_MISSING"),
        ("first_hit_partition_certificate", "FIRST_HIT_PARTITION_MISSING"),
        ("global_dq_certificate", "GLOBAL_DQ_CERTIFICATE_MISSING"),
        ("global_scalar_matching_certificate", "GLOBAL_SCALAR_MATCHING_MISSING"),
        ("parameter_continuation_certificate", "PARAMETER_CONTINUATION_MISSING"),
    ):
        if not nonempty_string(gate.get(field)):
            add(out, 3, code, field)
    return occurrence_ids


def check_gate4(data: dict[str, Any], gate3_occurrences: set[str], out: list[Finding]) -> None:
    gate = data.get("gate4", {})
    occurrences = unique_rows(
        gate.get("occurrences"), "occurrence_id", 4, "OCCURRENCE", out
    )
    if not occurrences:
        add(out, 4, "OCCURRENCE_REGISTRY_EMPTY", "no incidence occurrence rows")

    for occurrence_id, row in occurrences.items():
        for field in (
            "physical_incidence_digest",
            "coefficient_id",
            "m_id",
            "q_id",
            "polarity",
            "owner",
            "activation_certificate",
        ):
            if not nonempty_string(row.get(field)):
                add(out, 4, "OCCURRENCE_FIELD_MISSING", f"{occurrence_id}.{field}")
        views = row.get("views", [])
        if not isinstance(views, list):
            add(out, 4, "VIEW_LIST_MISSING", occurrence_id)
            continue
        by_orientation: dict[str, dict[str, Any]] = {}
        for view in views:
            orientation = view.get("orientation") if isinstance(view, dict) else None
            if orientation in by_orientation:
                add(out, 4, "VIEW_ORIENTATION_DUPLICATE", f"{occurrence_id}:{orientation}")
            elif orientation in {"forward", "reverse"}:
                by_orientation[orientation] = view
            else:
                add(out, 4, "VIEW_ORIENTATION_INVALID", f"{occurrence_id}:{orientation}")
        for orientation in ("forward", "reverse"):
            if orientation not in by_orientation:
                add(out, 4, "BIDIRECTIONAL_VIEW_MISSING", f"{occurrence_id}:{orientation}")
                continue
            view = by_orientation[orientation]
            for field in (
                "occurrence_id",
                "physical_incidence_digest",
                "coefficient_id",
                "m_id",
                "q_id",
                "polarity",
                "owner",
            ):
                if view.get(field) != row.get(field):
                    add(
                        out,
                        4,
                        "VIEW_BASE_RECORD_MISMATCH",
                        f"{occurrence_id}:{orientation}:{field}",
                    )
            if view.get("additive") is not False:
                add(out, 4, "VIEW_MUST_BE_NONADDITIVE", f"{occurrence_id}:{orientation}")
            for field in (
                "representation",
                "exact_current_certificate",
                "proper_family_certificate",
                "recovery_moment_certificate",
            ):
                if not nonempty_string(view.get(field)):
                    add(out, 4, "VIEW_CERTIFICATE_MISSING", f"{occurrence_id}:{orientation}:{field}")

        q_definition = row.get("q_definition", {})
        if not isinstance(q_definition, dict):
            add(out, 4, "Q_DEFINITION_MISSING", occurrence_id)
        else:
            if q_definition.get("charged_once") is not True:
                add(out, 4, "Q_NOT_CHARGED_ONCE", occurrence_id)
            if q_definition.get("formula") != "max(C_forward,C_reverse)*m":
                add(out, 4, "Q_MAX_FORMULA_MISSING", occurrence_id)
            declared_digest = q_definition.get("record_digest")
            record = {
                "occurrence_id": row.get("occurrence_id"),
                "physical_incidence_digest": row.get("physical_incidence_digest"),
                "coefficient_id": row.get("coefficient_id"),
                "m_id": row.get("m_id"),
                "q_id": row.get("q_id"),
                "polarity": row.get("polarity"),
                "owner": row.get("owner"),
            }
            if declared_digest != canonical_digest(record):
                add(out, 4, "Q_RECORD_DIGEST_MISMATCH", occurrence_id)

    missing_from_gate4 = gate3_occurrences - set(occurrences)
    if missing_from_gate4:
        add(out, 4, "GATE3_OCCURRENCES_UNREGISTERED", repr(sorted(missing_from_gate4)))

    for field, code in (
        ("prequery_orientation_policy", "PREQUERY_ORIENTATION_POLICY_MISSING"),
        ("orientation_mismatch_tail_certificate", "ORIENTATION_TAIL_MISSING"),
        ("global_bidirectional_recovery_certificate", "GLOBAL_BIDIRECTIONAL_RECOVERY_MISSING"),
        ("global_exact_q_certificate", "GLOBAL_EXACT_Q_MISSING"),
        ("global_exact_scalar_current_certificate", "GLOBAL_EXACT_CURRENT_MISSING"),
    ):
        if not nonempty_string(gate.get(field)):
            add(out, 4, code, field)


def check_manifest(data: Any) -> list[Finding]:
    out: list[Finding] = []
    if not isinstance(data, dict):
        return [Finding(3, "TOP_LEVEL_NOT_OBJECT", "manifest must be a JSON object")]
    if data.get("schema") != SCHEMA:
        add(out, 3, "SCHEMA_MISMATCH", repr(data.get("schema")))
    check_provenance(data, out)
    gate3_occurrences = check_gate3(data, out)
    check_gate4(data, gate3_occurrences, out)
    return out


def structural_fixture() -> dict[str, Any]:
    base = {
        "occurrence_id": "occ-1",
        "physical_incidence_digest": "physical-1",
        "coefficient_id": "coef-1",
        "m_id": "m-1",
        "q_id": "q-1",
        "polarity": "+",
        "owner": "owner-1",
    }
    view_common = {
        **base,
        "additive": False,
        "exact_current_certificate": "fixture-current",
        "proper_family_certificate": "fixture-proper",
        "recovery_moment_certificate": "fixture-moment",
    }
    return {
        "schema": SCHEMA,
        "provenance": [],
        "gate3": {
            "horizon": {
                "tau_min_lower": "1/10",
                "tau_max_upper": "10",
                "tau_max_certificate": "fixture-horizon",
            },
            "source_charts": [
                {
                    "chart_id": "chart-1",
                    "component": "G",
                    "domain": "fixture-domain",
                    "gauge": "fixture-gauge",
                    "coverage_cell": "fixture-cell",
                    "candidate_target_ids": ["target-1"],
                }
            ],
            "source_cover_certificate": "fixture-cover",
            "target_lifts": [
                {
                    "target_id": "target-1",
                    "obstacle": "W",
                    "lift": [0, 0],
                    "center_formula": "fixture-center",
                    "radius": "1/5",
                }
            ],
            "target_lift_completeness_certificate": "fixture-lifts",
            "event_rows": [
                {
                    "event_id": "event-1",
                    "source_chart_id": "chart-1",
                    "target_id": "target-1",
                    "event_equation": "fixture-H",
                    "squarefree_factor": "fixture-squarefree",
                    "selected_root": "fixture-root",
                    "occurrence_time": "fixture-time",
                    "first_hit_certificate": "fixture-first-hit",
                    "face_label": "face-1",
                    "submersion_certificate": "fixture-submersion",
                    "submersion_lower": "1/20",
                    "coarea_coefficient": "fixture-coarea",
                    "physical_trace": "fixture-trace",
                    "polarity": "+",
                    "owner": "owner-1",
                    "m_id": "m-1",
                    "q_id": "q-1",
                    "occurrence_id": "occ-1",
                    "scalar_current_certificate": "fixture-scalar",
                }
            ],
            "pair_incidence_rows": [],
            "triple_incidence_rows": [],
            "event_cover_certificate": "fixture-event-cover",
            "first_hit_partition_certificate": "fixture-first-hit-partition",
            "global_dq_certificate": "fixture-dq",
            "global_scalar_matching_certificate": "fixture-match",
            "parameter_continuation_certificate": "fixture-continuation",
        },
        "gate4": {
            "occurrences": [
                {
                    **base,
                    "activation_certificate": "fixture-activation",
                    "views": [
                        {**view_common, "orientation": "forward", "representation": "fixture-fw"},
                        {**view_common, "orientation": "reverse", "representation": "fixture-rev"},
                    ],
                    "q_definition": {
                        "charged_once": True,
                        "formula": "max(C_forward,C_reverse)*m",
                        "record_digest": canonical_digest(base),
                    },
                }
            ],
            "prequery_orientation_policy": "fixture-policy",
            "orientation_mismatch_tail_certificate": "fixture-tail",
            "global_bidirectional_recovery_certificate": "fixture-recovery",
            "global_exact_q_certificate": "fixture-q",
            "global_exact_scalar_current_certificate": "fixture-current",
        },
    }


def print_findings(findings: list[Finding]) -> None:
    for gate in (3, 4):
        rows = [item for item in findings if item.gate == gate]
        status = "CERTIFIED" if not rows else "NOT_CERTIFIED"
        print(f"GATE_{gate}: {status}")
        for item in rows:
            print(f"  [{item.code}] {item.detail}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--json", action="store_true", dest="json_output")
    args = parser.parse_args()

    if args.self_test:
        fixture_findings = check_manifest(structural_fixture())
        if fixture_findings:
            print("SELF_TEST: FAIL (complete structural fixture was rejected)")
            print_findings(fixture_findings)
            return 1
        snapshot = json.loads(DEFAULT_MANIFEST.read_text(encoding="utf-8"))
        snapshot_findings = check_manifest(snapshot)
        codes = {item.code for item in snapshot_findings}
        required_rejections = {
            "SOURCE_TARGET_LIST_MISSING",
            "EVENT_INVENTORY_EMPTY",
            "BIDIRECTIONAL_VIEW_MISSING",
            "GLOBAL_EXACT_Q_MISSING",
        }
        if not required_rejections <= codes:
            print("SELF_TEST: FAIL (incomplete snapshot was not rejected hard enough)")
            print_findings(snapshot_findings)
            return 1
        print("SELF_TEST: PASS")
        print("  structural complete fixture: accepted")
        print("  current evidence snapshot: rejected fail-closed")
        return 0

    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"MANIFEST_READ_ERROR: {exc}", file=sys.stderr)
        return 1
    findings = check_manifest(data)
    if args.json_output:
        print(
            json.dumps(
                [item.__dict__ for item in findings],
                indent=2,
                ensure_ascii=False,
                sort_keys=True,
            )
        )
    else:
        print_findings(findings)
    return 0 if not findings else 2


if __name__ == "__main__":
    raise SystemExit(main())
