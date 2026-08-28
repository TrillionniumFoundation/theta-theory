#!/usr/bin/env python3
"""Round162: first strict exterior pruning block for one frozen R1648 prefix.

This certificate is deliberately narrow.  It combines the pinned Gate3
source-W conservative atlas with the pinned Round139 first collision.  The
Round139 prefix requires target W[1,0] and outgoing target chart W.  Exact
candidate reduction proves that W[1,0] is absent on the source-W / chart-W
cell, so the open chart interior cannot carry that frozen prefix.

No claim is made about another return signature, chart-boundary gluing,
disconnected exterior sheets as a whole, or D02.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "cm2_round162_exterior_frozen_prefix_pruning_certificate.json"
SCHEMA = "cm2.round162.exterior-frozen-prefix-pruning.v1"
STATUS = (
    "CERTIFIED_ONE_FROZEN_PREFIX_WW_OPEN_CELL_EXCLUSION__"
    "EXTERIOR_AND_D02_STILL_BLOCKED"
)

GATE3_ATLAS = "cm2-gate3-eight-cell-symmetry-atlas-manifest-2026-07-15.json"
GATE3_FIRST_HIT = "cm2-gate3-first-hit-atlas-manifest-2026-07-15.json"
GATE3_ATLAS_SOURCE = "cm2_gate3_eight_cell_symmetry_atlas_cert.py"
GATE3_CANDIDATE_SOURCE = "cm2_gate3_candidate_first_hit_cert.py"
ROUND139 = (
    "cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-"
    "2026-07-24.json"
)
ROUND139_SOURCE = (
    "cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier.py"
)

PINS = {
    GATE3_ATLAS:
        "f8fda665edbb7d8b39ce495188f90ecb2b5ec4384c1eb958949627df167c4987",
    GATE3_FIRST_HIT:
        "0c820a5e3481b2c18fabb14d8d0fab7ce454f9a9e68b856bb2a7bf139404f7f4",
    GATE3_ATLAS_SOURCE:
        "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    GATE3_CANDIDATE_SOURCE:
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    ROUND139:
        "64e91e6b1efcb2675982fbc453b08349b003c8be5b4d236f61e1392aaee045f0",
    ROUND139_SOURCE:
        "462ffcb41ba24771ce655ddb3ad5f18d5a22c8d0cb443ec1791ea9272d3d512b",
}
ROUND139_RESULT_SHA256 = (
    "6e8f54c34154ea5ba3c95d4e901bc643c020a0a42e180241ae9053bb24f42236"
)

RADIUS = {"G": Q(9, 25), "W": Q(4, 25)}
EPS = Q(1, 400)
TAU_MAX = Q(3)
INV_SQRT2_LOWER = Q(707, 1000)
INV_SQRT2_UPPER = Q(708, 1000)
SOURCE_W_CHARTS = ("W:E", "W:W", "W:N", "W:S")
FROZEN_TARGET = "W[1,0]"


def canonical(value: Any) -> str:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False,
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def strict_load(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    require(not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw, "encoding")

    def reject(value: str) -> None:
        raise ValueError(value)

    def reject_float(value: str) -> None:
        raise ValueError(value)

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in out, "duplicate key")
            out[key] = value
        return out

    value = json.loads(
        raw.decode("utf-8"), object_pairs_hook=unique, parse_constant=reject,
        parse_float=reject_float,
    )
    require(type(value) is dict, "top object")
    return value


@dataclass(frozen=True)
class Target:
    obstacle: str
    ix: int
    iy: int

    @property
    def target_id(self) -> str:
        return f"{self.obstacle}[{self.ix},{self.iy}]"


TARGETS = tuple(
    Target(obstacle, ix, iy)
    for obstacle in ("G", "W")
    for ix in range(-4, 5)
    for iy in range(-4, 5)
)


def vector_interval(source: str, target: Target) -> tuple[Q, Q, Q, Q]:
    ix, iy = target.ix, target.iy
    if source == "G" and target.obstacle == "G":
        return Q(ix), Q(ix), Q(iy), Q(iy)
    if source == "G" and target.obstacle == "W":
        x = Q(2 * ix + 1, 2)
        return x - EPS, x + EPS, Q(2 * iy + 1, 2), Q(2 * iy + 1, 2)
    if source == "W" and target.obstacle == "G":
        x = Q(2 * ix - 1, 2)
        return x - EPS, x + EPS, Q(2 * iy - 1, 2), Q(2 * iy - 1, 2)
    return Q(ix), Q(ix), Q(iy), Q(iy)


def square_min_abs(lower: Q, upper: Q) -> Q:
    if lower <= 0 <= upper:
        return Q(0)
    return min(lower * lower, upper * upper)


def absmax(lower: Q, upper: Q) -> Q:
    return max(abs(lower), abs(upper))


def support_upper(cell: str, x0: Q, x1: Q, y0: Q, y1: Q) -> Q:
    if cell == "E":
        a_upper, b_abs = x1, absmax(y0, y1)
    elif cell == "W":
        a_upper, b_abs = -x0, absmax(y0, y1)
    elif cell == "N":
        a_upper, b_abs = y1, absmax(x0, x1)
    elif cell == "S":
        a_upper, b_abs = -y0, absmax(x0, x1)
    else:
        raise ValueError(cell)
    if a_upper >= 0:
        return a_upper + b_abs * INV_SQRT2_UPPER
    return a_upper * INV_SQRT2_LOWER + b_abs * INV_SQRT2_UPPER


def classify(source: str, cell: str, target: Target) -> tuple[str, str]:
    if target.obstacle == source and target.ix == 0 and target.iy == 0:
        return (
            "self_source",
            "same strictly convex source lift; outgoing interior rays do not re-enter it",
        )
    x0, x1, y0, y1 = vector_interval(source, target)
    distance2 = square_min_abs(x0, x1) + square_min_abs(y0, y1)
    threshold = TAU_MAX + RADIUS[source] + RADIUS[target.obstacle]
    if distance2 >= threshold * threshold:
        return "empty_horizon_center_distance", (
            f"min_center_distance^2={distance2} >= "
            f"(3+R_source+R_target)^2={threshold * threshold}"
        )
    upper = support_upper(cell, x0, x1, y0, y1)
    outgoing_threshold = RADIUS[source] - RADIUS[target.obstacle]
    if upper < outgoing_threshold:
        return "empty_outgoing_halfspace", (
            f"support_upper={upper} < R_source-R_target={outgoing_threshold}"
        )
    return (
        "retained_candidate",
        "not excluded by certified horizon and outgoing-halfspace necessary conditions",
    )


def classification_rows(chart_id: str) -> list[dict[str, str]]:
    source, cell = chart_id.split(":")
    rows = []
    for target in TARGETS:
        classification, proof = classify(source, cell, target)
        rows.append({
            "target_id": target.target_id,
            "classification": classification,
            "proof": proof,
        })
    return rows


def candidate_ids(chart_id: str) -> list[str]:
    return [
        row["target_id"] for row in classification_rows(chart_id)
        if row["classification"] == "retained_candidate"
    ]


def check_pins() -> None:
    for name, expected in PINS.items():
        require(
            hashlib.sha256((HERE / name).read_bytes()).hexdigest() == expected,
            f"pin:{name}",
        )


def build_result() -> dict[str, Any]:
    check_pins()
    atlas = strict_load(HERE / GATE3_ATLAS)
    first_hit = strict_load(HERE / GATE3_FIRST_HIT)
    round139_document = strict_load(HERE / ROUND139)

    require(
        set(round139_document) == {"schema", "result", "result_sha256"},
        "Round139 wrapper",
    )
    require(
        digest(round139_document["result"]) == ROUND139_RESULT_SHA256
        == round139_document["result_sha256"],
        "Round139 result digest",
    )
    r139 = round139_document["result"]
    require(
        r139["corrected_rank3_source_contract"]["source_chart"] == "W:E"
        and r139["corrected_rank3_source_contract"]["source_target"]
        == FROZEN_TARGET,
        "Round139 source",
    )
    first_rows = (
        r139["collision_rows"][0],
        r139["positive_area_collision_rows"][0],
    )
    require(
        all(
            row["collision_index"] == 1
            and row["selected_absolute_owner_id"] == FROZEN_TARGET
            and row["relative_frozen_target_id"] == FROZEN_TARGET
            and row["outgoing_chart"] == "W"
            for row in first_rows
        ),
        "Round139 frozen first prefix",
    )

    require(
        atlas["schema"] == "cm2.gate3.eight-cell-symmetry-atlas.v1"
        and atlas["coverage"]["global_leaf_count"] == 143248,
        "Gate3 atlas contract",
    )
    hit_charts = {
        row["chart_id"]: row
        for row in first_hit["candidate_reduction"]["charts"]
    }
    per_chart: list[dict[str, Any]] = []
    for chart_id in SOURCE_W_CHARTS:
        manifest_row = atlas["charts"][chart_id]
        ids = candidate_ids(chart_id)
        classification = classification_rows(chart_id)
        hit_row = hit_charts[chart_id]
        counts = manifest_row["counts"]
        require(
            len(ids) == manifest_row["candidate_count"] == hit_row["retained"]
            == 55,
            f"candidate count:{chart_id}",
        )
        require(
            digest(ids) == hit_row["candidate_sha256"]
            and digest(classification) == hit_row["classification_sha256"],
            f"candidate digest:{chart_id}",
        )
        require(
            counts["unique_first"] + counts["tangency_graph"]
            + counts["multi_candidate"] == manifest_row["leaf_count"],
            f"leaf census:{chart_id}",
        )
        per_chart.append({
            "chart_id": chart_id,
            "candidate_count": len(ids),
            "candidate_ids_sha256": digest(ids),
            "classification_rows_sha256": digest(classification),
            "frozen_target_retained": FROZEN_TARGET in ids,
            "leaf_count": manifest_row["leaf_count"],
            "counts": counts,
            "leaf_rows_sha256": manifest_row["leaf_rows_sha256"],
            "provenance": manifest_row["provenance"],
        })

    aggregate = {
        "leaf_count": sum(row["leaf_count"] for row in per_chart),
        "unique_first": sum(row["counts"]["unique_first"] for row in per_chart),
        "tangency_graph": sum(
            row["counts"]["tangency_graph"] for row in per_chart
        ),
        "multi_candidate": sum(
            row["counts"]["multi_candidate"] for row in per_chart
        ),
    }
    require(
        aggregate == {
            "leaf_count": 76828,
            "unique_first": 26204,
            "tangency_graph": 56,
            "multi_candidate": 50568,
        },
        "source-W aggregate",
    )

    ww = next(row for row in per_chart if row["chart_id"] == "W:W")
    target = Target("W", 1, 0)
    target_classification, target_witness = classify("W", "W", target)
    require(
        target_classification == "empty_outgoing_halfspace"
        and target_witness
        == "support_upper=-707/1000 < R_source-R_target=0"
        and not ww["frozen_target_retained"],
        "W:W frozen-target exclusion",
    )

    return {
        "status": STATUS,
        "scope": {
            "signature_scope":
                "only the pinned Round139 frozen first-collision prefix",
            "source_scope":
                "Gate3 source obstacle W, four conservative chart covers",
            "parameter_domain": atlas["coverage"]["domain"],
            "not_all_return_signatures": True,
            "not_full_exterior_sheet_exhaustion": True,
            "not_D02_closure": True,
        },
        "provenance": {
            "dependency_sha256": PINS,
            "Round139_result_sha256": ROUND139_RESULT_SHA256,
            "old_artifacts_modified": False,
            "candidate_registry_rebuilt_with_exact_rationals": True,
            "source_W_census_rebuilt_from_pinned_chart_rows": True,
        },
        "frozen_prefix": {
            "source_chart": "W:E",
            "collision_index": 1,
            "selected_owner": FROZEN_TARGET,
            "relative_target": FROZEN_TARGET,
            "outgoing_chart": "W",
            "Round139_local_and_positive_rows_agree": True,
            "prefix_length_used": 1,
        },
        "source_W_atlas": {
            "charts": per_chart,
            "aggregate": aggregate,
        },
        "certified_open_cell_block": {
            "disposition": "EARLIEST_PREFIX_EXCLUDED",
            "chart_id": "W:W",
            "region":
                "open chart interior; exact exclusion extends to the closed "
                "conservative Gate3 chart cover",
            "excluded_frozen_target": FROZEN_TARGET,
            "exact_candidate_classification": target_classification,
            "exact_witness": target_witness,
            "candidate_list_complete_for_tau_less_than": "3",
            "candidate_count": 55,
            "frozen_target_in_candidate_list": False,
            "covered_atlas_leaf_count": ww["leaf_count"],
            "covered_atlas_counts": ww["counts"],
            "frozen_prefix_excluded_leaf_count": 18930,
            "unique_first_immediate_short_circuit_credit": 6518,
            "proof":
                "the required first owner is absent before any root ordering; "
                "therefore the frozen prefix cannot occur in this open cell",
        },
        "frozen_prefix_pruning_census": {
            "source_W_leaf_count": 76828,
            "W_W_excluded_leaf_count": 18930,
            "remaining_outside_W_W_leaf_count": 57898,
            "remaining_outside_W_W_unique_first": 19686,
            "remaining_outside_W_W_tangency_graph": 32,
            "remaining_outside_W_W_multi_candidate": 38180,
            "frozen_prefix_unresolved_leaves_zero": False,
        },
        "global_all_signature_queue": {
            "source_W_unique_first_total": 26204,
            "source_W_tangency_graph_total": 56,
            "source_W_multi_candidate_total": 50568,
            "W_W_tangency_cells_relevant_to_boundary_gluing_or_other_signatures":
                24,
            "W_W_multi_cells_relevant_to_other_signatures": 12388,
            "all_signature_unresolved_leaves_zero": False,
        },
        "strict_nonpromotion": {
            "all_disconnected_exterior_sheets_excluded": False,
            "all_chart_and_grazing_strata_glued_or_typed": False,
            "all_return_signatures_excluded_or_connected": False,
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate": (
            "rebuild owner and outgoing-chart prefixes on the remaining "
            "source-W unique leaves; type the 56 tangency strata; subdivide "
            "the 50,568 multi-candidate leaves; then extend the same "
            "earliest-prefix census across the four compact angular charts "
            "until unresolved leaves are zero"
        ),
    }


def main() -> None:
    result = build_result()
    document = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    OUTPUT.write_text(
        json.dumps(document, indent=2, sort_keys=True, ensure_ascii=False)
        + "\n",
        encoding="utf-8",
    )
    print(canonical({
        "output": OUTPUT.name,
        "result_sha256": document["result_sha256"],
        "status": result["status"],
    }))


if __name__ == "__main__":
    main()
