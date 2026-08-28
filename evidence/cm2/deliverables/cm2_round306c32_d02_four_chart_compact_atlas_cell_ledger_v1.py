#!/usr/bin/env python3
"""Materialize the exact four-chart compact s=0 cell and face ledger.

This producer pulls the pinned source-W Gate3 atlas back to the compact
physical cylinder, applies the audited Round165 618-to-622 replacement, clips
the rational guard band to |t| <= 1/sqrt(2), and emits deterministic ledgers
for cells, intra-chart adjacencies, source-chart seams, grazing faces, corners,
and inherited first-collision event graphs.

The artifact is deliberately nonpromotional.  It does not turn source-W
record conservation into R1648 component connectivity, component exits, or a
complete Round144 terminal census.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import os
import shutil
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Callable, Iterable, TypeVar


ROOT = Path(__file__).resolve().parents[1]
DELIVERABLES = ROOT / "deliverables"
sys.path.insert(0, str(DELIVERABLES))

import cm2_gate3_eight_cell_symmetry_atlas_cert as atlas  # noqa: E402
import cm2_round165_adaptive_typed_seam_census as round165  # noqa: E402


SCHEMA = "cm2.round306c32.d02-four-chart-compact-atlas-cell-ledger.v1"
ROW_SCHEMA = "cm2.round306c32.d02-four-chart-compact-atlas-cell.v1"
EXPECTED_BRIDGE_RESULT = (
    "5a327f96ecc8183af76695123dcf6fc4ccbf443e4bd7427cef38090c06bcfe86"
)
EXPECTED_ROUND165_RESULT = (
    "93e2899d0a9a79a82e1b193158f3733e891e2c5b4c9ce83f970aff40bf75c270"
)
EXPECTED_ROUND165_TERMINAL_ROWS = (
    "c60844dfea7f97813baa75be8ae08b7c91ffed9de12b486b7898273d18a56d04"
)
EXPECTED_FORMAL_LEDGER_OBJECT = (
    "34d485901b6458f7e0614361a220d3e475ee0827be64aa19e8955b29e09d1c97"
)
SOURCE_CHARTS = ("W:E", "W:W", "W:N", "W:S")
COMPACT_CHARTS = ("E", "N", "W", "S")
NEG_A = "NEG_INV_SQRT_2"
POS_A = "POS_INV_SQRT_2"


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def file_sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def strict_json(path: Path) -> dict[str, Any]:
    def pairs(values: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in values:
            require(key not in result, f"duplicate JSON key:{path}:{key}")
            result[key] = value
        return result

    def reject_float(value: str) -> None:
        raise RuntimeError(f"floating JSON number:{path}:{value}")

    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=pairs,
        parse_float=reject_float,
    )
    require(type(value) is dict, f"top-level object:{path}")
    return value


def closed_row(value: dict[str, Any]) -> dict[str, Any]:
    require("row_sha256" not in value, "row already closed")
    return {**value, "row_sha256": digest(value)}


@dataclass(frozen=True)
class Bound:
    kind: str
    rational: Q | None = None

    @classmethod
    def from_lower(cls, value: Q) -> "Bound":
        if value < 0 and value * value > Q(1, 2):
            return cls(NEG_A)
        require(value * value < Q(1, 2), f"invalid lower endpoint:{value}")
        return cls("RATIONAL", value)

    @classmethod
    def from_upper(cls, value: Q) -> "Bound":
        if value > 0 and value * value > Q(1, 2):
            return cls(POS_A)
        require(value * value < Q(1, 2), f"invalid upper endpoint:{value}")
        return cls("RATIONAL", value)

    def order_key(self) -> tuple[int, Q]:
        if self.kind == NEG_A:
            return (-1, Q(0))
        if self.kind == POS_A:
            return (1, Q(0))
        require(self.rational is not None, "rational bound")
        return (0, self.rational)

    def expression(self) -> tuple[Q, Q]:
        if self.kind == NEG_A:
            return (Q(0), Q(-1))
        if self.kind == POS_A:
            return (Q(0), Q(1))
        require(self.rational is not None, "rational expression")
        return (self.rational, Q(0))

    def descriptor(self) -> dict[str, Any]:
        if self.kind == "RATIONAL":
            require(self.rational is not None, "rational descriptor")
            return {"kind": "RATIONAL", "value": str(self.rational)}
        sign = "-" if self.kind == NEG_A else "+"
        interval = ["-708/1000", "-707/1000"] if sign == "-" else [
            "707/1000", "708/1000",
        ]
        return {
            "kind": "ALGEBRAIC",
            "value": f"{sign}1/sqrt(2)",
            "minimal_polynomial": "2*x^2-1",
            "isolating_interval": interval,
        }


Endpoint = Q | Bound
T = TypeVar("T", Q, Bound)


def endpoint_key(value: Endpoint) -> tuple[int, Q]:
    if isinstance(value, Bound):
        return value.order_key()
    return (0, value)


def endpoint_descriptor(value: Endpoint) -> dict[str, Any]:
    if isinstance(value, Bound):
        return value.descriptor()
    return {"kind": "RATIONAL", "value": str(value)}


def endpoint_lt(left: Endpoint, right: Endpoint) -> bool:
    return endpoint_key(left) < endpoint_key(right)


def endpoint_max(left: T, right: T) -> T:
    return right if endpoint_lt(left, right) else left


def endpoint_min(left: T, right: T) -> T:
    return left if endpoint_lt(left, right) else right


def span_expression(lower: Endpoint, upper: Endpoint) -> tuple[Q, Q]:
    if isinstance(lower, Bound):
        lower_constant, lower_a = lower.expression()
    else:
        lower_constant, lower_a = lower, Q(0)
    if isinstance(upper, Bound):
        upper_constant, upper_a = upper.expression()
    else:
        upper_constant, upper_a = upper, Q(0)
    return (upper_constant - lower_constant, upper_a - lower_a)


def add_expression(
    left: tuple[Q, Q], right: tuple[Q, Q],
) -> tuple[Q, Q]:
    return (left[0] + right[0], left[1] + right[1])


def scale_expression(value: tuple[Q, Q], factor: Q) -> tuple[Q, Q]:
    return (value[0] * factor, value[1] * factor)


def expression_descriptor(value: tuple[Q, Q]) -> dict[str, str]:
    return {
        "rational_constant": str(value[0]),
        "one_over_sqrt_2_coefficient": str(value[1]),
    }


@dataclass(frozen=True)
class Cell:
    cell_id: str
    origin_key: str
    gate3_chart: str
    compact_chart: str
    t0: Bound
    t1: Bound
    p0: Q
    p1: Q
    source_kind: str
    source_classification: str
    event: dict[str, Any] | None


@dataclass(frozen=True)
class Segment:
    lower: Endpoint
    upper: Endpoint
    cell: Cell


class LedgerWriter:
    def __init__(self, path: Path, order: str):
        self.path = path
        self.order = order
        self.count = 0
        self.sequence = hashlib.sha256()
        self.raw: io.BufferedWriter | None = None
        self.stream: gzip.GzipFile | None = None

    def __enter__(self) -> "LedgerWriter":
        self.raw = self.path.open("wb")
        self.stream = gzip.GzipFile(
            filename="", mode="wb", fileobj=self.raw, compresslevel=6, mtime=0,
        )
        return self

    def write(self, value: dict[str, Any]) -> dict[str, Any]:
        require(self.stream is not None, "ledger writer open")
        row = closed_row(value)
        payload = canonical_bytes(row) + b"\n"
        self.stream.write(payload)
        self.sequence.update((row["row_sha256"] + "\n").encode("ascii"))
        self.count += 1
        return row

    def __exit__(self, *_args: object) -> None:
        require(self.stream is not None and self.raw is not None, "ledger close")
        self.stream.close()
        self.raw.close()

    def descriptor(self) -> dict[str, Any]:
        return {
            "filename": self.path.name,
            "order": self.order,
            "row_count": self.count,
            "row_hash_line_sequence_sha256": self.sequence.hexdigest(),
            "sha256": file_sha256(self.path),
            "size": self.path.stat().st_size,
        }


def validate_inputs(formal_ledger_path: Path) -> dict[str, Any]:
    bridge_path = (
        DELIVERABLES / "cm2_round162_compact_gate3_coordinate_bridge_certificate.json"
    )
    round165_path = (
        DELIVERABLES / "cm2_round165_adaptive_typed_seam_census_certificate.json"
    )
    bridge = strict_json(bridge_path)
    round165_doc = strict_json(round165_path)
    formal = strict_json(formal_ledger_path)
    require(bridge.get("result_sha256") == EXPECTED_BRIDGE_RESULT, "bridge result pin")
    require(digest(bridge["result"]) == EXPECTED_BRIDGE_RESULT, "bridge self hash")
    bridge_result = bridge["result"]
    require(
        bridge_result["exact_coordinate_bridge"][
            "four_compact_seams_supply_exact_overlap_gluing"
        ] is True,
        "bridge seam gluing",
    )
    require(
        bridge_result["exact_coordinate_bridge"][
            "q_plus_minus_one_are_the_only_source_grazing_strata"
        ] is True,
        "bridge grazing",
    )
    require(round165_doc.get("result_sha256") == EXPECTED_ROUND165_RESULT, "Round165 pin")
    require(digest(round165_doc["result"]) == EXPECTED_ROUND165_RESULT, "Round165 self hash")
    adaptive = round165_doc["result"]["adaptive_seam_census"]
    require(adaptive["terminal_record_count"] == 622, "Round165 terminal count")
    require(
        adaptive["terminal_rows_sha256"] == EXPECTED_ROUND165_TERMINAL_ROWS
        and digest(adaptive["terminal_rows"]) == EXPECTED_ROUND165_TERMINAL_ROWS,
        "Round165 terminal rows",
    )
    refined = round165_doc["result"]["refined_recordwise_census"]
    require(
        refined["round163_total_source_W_records"] == 76828
        and refined["round163_seam_parent_records_replaced"] == 618
        and refined["refined_total_records"] == 76832,
        "Round165 conservation",
    )
    formal_copy = dict(formal)
    formal_object = formal_copy.pop("object_sha256", None)
    require(
        formal_object == EXPECTED_FORMAL_LEDGER_OBJECT
        and digest(formal_copy) == EXPECTED_FORMAL_LEDGER_OBJECT,
        "formal ledger object",
    )
    require(
        formal.get("status") == "PASS_CONSOLIDATED_SOURCE_W_FORMAL_LEDGER__REMAINDER_0"
        and formal["current_state"] == {
            "conservative_live": 2020,
            "excluded": 74812,
            "remaining": 0,
            "remaining_partition": {"compact_q": 0},
            "resolved_nonexcluded": 2020,
            "total": 76832,
        },
        "formal source-W zero",
    )
    return {
        "bridge": bridge,
        "round165": round165_doc,
        "formal": formal,
        "paths": {
            "bridge": bridge_path,
            "round165": round165_path,
            "formal": formal_ledger_path,
        },
    }


def rational_box(value: dict[str, Any]) -> tuple[Q, Q, Q, Q, Q, Q]:
    return (
        Q(value["t"][0]), Q(value["t"][1]),
        Q(value["p"][0]), Q(value["p"][1]),
        Q(value["s"][0]), Q(value["s"][1]),
    )


def cell_identifier(
    origin_key: str, t0: Bound, t1: Bound, p0: Q, p1: Q,
) -> str:
    key = {
        "schema": ROW_SCHEMA,
        "origin_key": origin_key,
        "physical_t": [t0.descriptor(), t1.descriptor()],
        "p": [str(p0), str(p1)],
        "s": "0",
    }
    return "c32-compact-cell:" + digest(key)


def clipping_class(t0: Bound, t1: Bound) -> str:
    if t0.kind == NEG_A and t1.kind == POS_A:
        return "BOTH_GUARD_BANDS_CLIPPED"
    if t0.kind == NEG_A:
        return "NEGATIVE_GUARD_BAND_CLIPPED"
    if t1.kind == POS_A:
        return "POSITIVE_GUARD_BAND_CLIPPED"
    return "STRICTLY_INSIDE_TRUE_COMPACT_CHART_IMAGE"


def compact_map(chart: str) -> dict[str, str]:
    sign = "t" if chart in {"E", "S"} else "-t"
    monotonicity = "INCREASING" if chart in {"E", "S"} else "DECREASING"
    return {
        "t_of_z": "2*z/(1+z^2)" if sign == "t" else "-2*z/(1+z^2)",
        "z_of_t": f"{sign}/(1+sqrt(1-t^2))",
        "p_of_q": "2*q/(1+q^2)",
        "q_of_p": "p/(1+sqrt(1-p^2))",
        "t_to_z_monotonicity": monotonicity,
        "p_to_q_monotonicity": "INCREASING",
    }


def build_cells(
    documents: dict[str, Any], workers: int, writer: LedgerWriter,
) -> tuple[list[Cell], dict[str, Any]]:
    atlases = round165.build_atlases(workers)
    require(
        {chart: len(atlases[chart]) for chart in SOURCE_CHARTS}
        == {"W:E": 18930, "W:W": 18930, "W:N": 19484, "W:S": 19484},
        "atlas chart census",
    )
    terminal_rows = documents["round165"]["result"]["adaptive_seam_census"][
        "terminal_rows"
    ]
    terminal_by_parent: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in terminal_rows:
        terminal_by_parent[row["parent_leaf_key"]].append(row)
    require(len(terminal_by_parent) == 618, "Round165 parent registry")

    raw_rows: list[dict[str, Any]] = []
    base_classifications: Counter[str] = Counter()
    for chart in SOURCE_CHARTS:
        for leaf in atlases[chart]:
            origin_key = f"{chart}:{leaf.box.path}"
            if origin_key in terminal_by_parent:
                continue
            base_row = atlas.leaf_row(chart, leaf)
            base_classifications[leaf.classification] += 1
            raw_rows.append({
                "origin_key": origin_key,
                "gate3_chart": chart,
                "box": {
                    "t": [str(leaf.box.t0), str(leaf.box.t1)],
                    "p": [str(leaf.box.p0), str(leaf.box.p1)],
                    "s": [str(leaf.box.s0), str(leaf.box.s1)],
                },
                "source_kind": "ROUND162_GATE3_BASE_LEAF",
                "source_classification": leaf.classification,
                "owner_target": leaf.owner_target,
                "active_candidates": list(leaf.active_targets),
                "tangencies": list(leaf.tangency_targets),
                "source_row_sha256": digest(base_row),
                "source_parent_key": None,
                "event_payload": (
                    {
                        "event_kind": "GATE3_PHYSICAL_FIRST_TANGENCY_GRAPH",
                        "target_ids": list(leaf.tangency_targets),
                        "source_row_sha256": digest(base_row),
                    }
                    if leaf.classification == "tangency_graph" else None
                ),
            })
    terminal_classifications: Counter[str] = Counter()
    for row in terminal_rows:
        terminal_classifications[row["classification"]] += 1
        typed = row.get("typed_seam")
        raw_rows.append({
            "origin_key": row["leaf_key"],
            "gate3_chart": row["chart_id"],
            "box": row["box"],
            "source_kind": "ROUND165_REFINED_TERMINAL",
            "source_classification": row["classification"],
            "owner_target": "W[1,0]",
            "active_candidates": ["W[1,0]"],
            "tangencies": [],
            "source_row_sha256": digest(row),
            "source_parent_key": row["parent_leaf_key"],
            "event_payload": (
                {
                    "event_kind": "ROUND165_TYPED_OUTGOING_CHART_SEAM_GRAPH",
                    "seam_id": typed["seam_id"],
                    "graph_kind": typed["graph_kind"],
                    "typed_seam_sha256": digest(typed),
                    "source_row_sha256": digest(row),
                }
                if typed is not None else None
            ),
        })
    raw_rows.sort(key=lambda row: row["origin_key"])
    require(len(raw_rows) == 76832, "refined source record count")
    require(len({row["origin_key"] for row in raw_rows}) == 76832, "unique origin keys")

    cells: list[Cell] = []
    clipping: Counter[str] = Counter()
    per_chart: Counter[str] = Counter()
    area_by_chart: dict[str, tuple[Q, Q]] = {
        chart: (Q(0), Q(0)) for chart in COMPACT_CHARTS
    }
    event_count = 0
    for raw in raw_rows:
        t0_raw, t1_raw, p0, p1, s0, s1 = rational_box(raw["box"])
        require(s0 < 0 < s1, f"s=0 product slice:{raw['origin_key']}")
        require(t0_raw < t1_raw and p0 < p1, f"positive box:{raw['origin_key']}")
        require(
            not (
                (t1_raw < 0 and t1_raw * t1_raw >= Q(1, 2))
                or (t0_raw > 0 and t0_raw * t0_raw >= Q(1, 2))
            ),
            f"guard-only leaf:{raw['origin_key']}",
        )
        t0 = Bound.from_lower(t0_raw)
        t1 = Bound.from_upper(t1_raw)
        require(endpoint_lt(t0, t1), f"clipped width:{raw['origin_key']}")
        compact_chart_id = raw["gate3_chart"].split(":")[1]
        cell_id = cell_identifier(raw["origin_key"], t0, t1, p0, p1)
        clipping_value = clipping_class(t0, t1)
        clipping[clipping_value] += 1
        per_chart[compact_chart_id] += 1
        width = span_expression(t0, t1)
        area = scale_expression(width, p1 - p0)
        area_by_chart[compact_chart_id] = add_expression(
            area_by_chart[compact_chart_id], area,
        )
        if raw["event_payload"] is not None:
            event_count += 1
        cell = Cell(
            cell_id=cell_id,
            origin_key=raw["origin_key"],
            gate3_chart=raw["gate3_chart"],
            compact_chart=compact_chart_id,
            t0=t0,
            t1=t1,
            p0=p0,
            p1=p1,
            source_kind=raw["source_kind"],
            source_classification=raw["source_classification"],
            event=raw["event_payload"],
        )
        writer.write({
            "schema": ROW_SCHEMA,
            "cell_id": cell_id,
            "origin_key": raw["origin_key"],
            "gate3_chart": raw["gate3_chart"],
            "compact_chart": compact_chart_id,
            "dimension": 2,
            "physical_slice": "s=0",
            "gate3_product_box": raw["box"],
            "physical_t_interval": [t0.descriptor(), t1.descriptor()],
            "physical_p_interval": [str(p0), str(p1)],
            "compact_preimage": {
                "definition": "inverse image under the exact monotone chart maps",
                "coordinate_map": compact_map(compact_chart_id),
                "z_domain": "[-(sqrt(2)-1),sqrt(2)-1]",
                "q_domain": "[-1,1]",
            },
            "guard_band_clipping": clipping_value,
            "source_lineage": {
                "kind": raw["source_kind"],
                "classification": raw["source_classification"],
                "owner_target": raw["owner_target"],
                "active_candidates": raw["active_candidates"],
                "tangencies": raw["tangencies"],
                "source_row_sha256": raw["source_row_sha256"],
                "source_parent_key": raw["source_parent_key"],
            },
            "inherited_event_graph": raw["event_payload"],
            "round144_terminal_classification": "UNASSIGNED_PENDING_R1648_COMPONENT_CROSSWALK",
            "formal_credit": {
                "D02": 0,
                "D03": 0,
                "D04": 0,
                "Gate5_fields": 0,
            },
        })
        cells.append(cell)
    require(per_chart == Counter({"E": 18934, "W": 18930, "N": 19484, "S": 19484}), "physical chart count")
    for chart in COMPACT_CHARTS:
        require(area_by_chart[chart] == (Q(0), Q(4)), f"chart area:{chart}")
    total_area = (Q(0), Q(0))
    for value in area_by_chart.values():
        total_area = add_expression(total_area, value)
    require(total_area == (Q(0), Q(16)), "four-chart area")
    return cells, {
        "base_classifications": dict(sorted(base_classifications.items())),
        "round165_terminal_classifications": dict(sorted(terminal_classifications.items())),
        "clipping": dict(sorted(clipping.items())),
        "per_chart": dict(sorted(per_chart.items())),
        "area_by_chart": {
            chart: expression_descriptor(area_by_chart[chart])
            for chart in COMPACT_CHARTS
        },
        "total_area": expression_descriptor(total_area),
        "inherited_event_graph_cell_count": event_count,
    }


def segment_sort_key(value: Segment) -> tuple[tuple[int, Q], tuple[int, Q], str]:
    return (endpoint_key(value.lower), endpoint_key(value.upper), value.cell.cell_id)


def validate_side(segments: list[Segment], label: str) -> tuple[Q, Q]:
    require(bool(segments), f"empty side:{label}")
    ordered = sorted(segments, key=segment_sort_key)
    total = (Q(0), Q(0))
    previous: Endpoint | None = None
    for segment in ordered:
        require(endpoint_lt(segment.lower, segment.upper), f"positive segment:{label}")
        if previous is not None:
            require(not endpoint_lt(segment.lower, previous), f"overlap side:{label}")
        total = add_expression(total, span_expression(segment.lower, segment.upper))
        previous = segment.upper
    return total


def matched_segments(
    negative: list[Segment], positive: list[Segment], label: str,
) -> list[tuple[Endpoint, Endpoint, Cell, Cell]]:
    negative = sorted(negative, key=segment_sort_key)
    positive = sorted(positive, key=segment_sort_key)
    negative_total = validate_side(negative, label + ":negative")
    positive_total = validate_side(positive, label + ":positive")
    require(negative_total == positive_total, f"side measure:{label}")
    i = 0
    j = 0
    matched: list[tuple[Endpoint, Endpoint, Cell, Cell]] = []
    overlap_total = (Q(0), Q(0))
    while i < len(negative) and j < len(positive):
        left = negative[i]
        right = positive[j]
        lower = endpoint_max(left.lower, right.lower)
        upper = endpoint_min(left.upper, right.upper)
        if endpoint_lt(lower, upper):
            matched.append((lower, upper, left.cell, right.cell))
            overlap_total = add_expression(
                overlap_total, span_expression(lower, upper),
            )
        left_end = endpoint_key(left.upper)
        right_end = endpoint_key(right.upper)
        if left_end <= right_end:
            i += 1
        if right_end <= left_end:
            j += 1
    require(
        overlap_total == negative_total == positive_total,
        f"gap-free matching:{label}",
    )
    return matched


def write_adjacency(
    cells: list[Cell], output: Path,
) -> tuple[dict[str, Any], dict[tuple[str, str], list[Segment]], dict[tuple[str, Q], list[Segment]]]:
    vertical: dict[tuple[str, Q], dict[str, list[Segment]]] = defaultdict(
        lambda: {"negative": [], "positive": []},
    )
    horizontal: dict[tuple[str, Q], dict[str, list[Segment]]] = defaultdict(
        lambda: {"negative": [], "positive": []},
    )
    seam_sides: dict[tuple[str, str], list[Segment]] = defaultdict(list)
    grazing_sides: dict[tuple[str, Q], list[Segment]] = defaultdict(list)
    for cell in cells:
        if cell.t0.kind == NEG_A:
            seam_sides[(cell.compact_chart, NEG_A)].append(
                Segment(cell.p0, cell.p1, cell),
            )
        else:
            require(cell.t0.rational is not None, "left rational")
            vertical[(cell.compact_chart, cell.t0.rational)]["positive"].append(
                Segment(cell.p0, cell.p1, cell),
            )
        if cell.t1.kind == POS_A:
            seam_sides[(cell.compact_chart, POS_A)].append(
                Segment(cell.p0, cell.p1, cell),
            )
        else:
            require(cell.t1.rational is not None, "right rational")
            vertical[(cell.compact_chart, cell.t1.rational)]["negative"].append(
                Segment(cell.p0, cell.p1, cell),
            )
        if cell.p0 == -1:
            grazing_sides[(cell.compact_chart, Q(-1))].append(
                Segment(cell.t0, cell.t1, cell),
            )
        else:
            horizontal[(cell.compact_chart, cell.p0)]["positive"].append(
                Segment(cell.t0, cell.t1, cell),
            )
        if cell.p1 == 1:
            grazing_sides[(cell.compact_chart, Q(1))].append(
                Segment(cell.t0, cell.t1, cell),
            )
        else:
            horizontal[(cell.compact_chart, cell.p1)]["negative"].append(
                Segment(cell.t0, cell.t1, cell),
            )

    writer = LedgerWriter(output, "CHART_AXIS_COORDINATE_SPAN_CELL_IDS")
    counts: Counter[str] = Counter()
    with writer:
        for (chart, coordinate), sides in sorted(
            vertical.items(), key=lambda item: (item[0][0], item[0][1]),
        ):
            matches = matched_segments(
                sides["negative"], sides["positive"],
                f"vertical:{chart}:{coordinate}",
            )
            for lower, upper, negative, positive in matches:
                face_key = {
                    "chart": chart,
                    "axis": "t",
                    "coordinate": str(coordinate),
                    "span": [str(lower), str(upper)],
                    "negative_cell": negative.cell_id,
                    "positive_cell": positive.cell_id,
                }
                writer.write({
                    "face_id": "c32-intra-face:" + digest(face_key),
                    "classification": "INTRA_CHART_CELL_ADJACENCY",
                    "compact_chart": chart,
                    "axis": "t",
                    "coordinate": endpoint_descriptor(coordinate),
                    "span": [endpoint_descriptor(lower), endpoint_descriptor(upper)],
                    "negative_cell_id": negative.cell_id,
                    "positive_cell_id": positive.cell_id,
                    "dimension": 1,
                })
                counts[f"{chart}:t"] += 1
        for (chart, coordinate), sides in sorted(
            horizontal.items(), key=lambda item: (item[0][0], item[0][1]),
        ):
            matches = matched_segments(
                sides["negative"], sides["positive"],
                f"horizontal:{chart}:{coordinate}",
            )
            for lower, upper, negative, positive in matches:
                face_key = {
                    "chart": chart,
                    "axis": "p",
                    "coordinate": str(coordinate),
                    "span": [endpoint_descriptor(lower), endpoint_descriptor(upper)],
                    "negative_cell": negative.cell_id,
                    "positive_cell": positive.cell_id,
                }
                writer.write({
                    "face_id": "c32-intra-face:" + digest(face_key),
                    "classification": "INTRA_CHART_CELL_ADJACENCY",
                    "compact_chart": chart,
                    "axis": "p",
                    "coordinate": endpoint_descriptor(coordinate),
                    "span": [endpoint_descriptor(lower), endpoint_descriptor(upper)],
                    "negative_cell_id": negative.cell_id,
                    "positive_cell_id": positive.cell_id,
                    "dimension": 1,
                })
                counts[f"{chart}:p"] += 1
    return ({**writer.descriptor(), "by_chart_axis": dict(sorted(counts.items()))}, seam_sides, grazing_sides)


SEAMS = (
    ("E_TO_N", ("E", POS_A, "z=+kappa"), ("N", POS_A, "z=-kappa")),
    ("N_TO_W", ("N", NEG_A, "z=+kappa"), ("W", POS_A, "z=-kappa")),
    ("W_TO_S", ("W", NEG_A, "z=+kappa"), ("S", NEG_A, "z=-kappa")),
    ("S_TO_E", ("S", POS_A, "z=+kappa"), ("E", NEG_A, "z=-kappa")),
)


def write_seams(
    seam_sides: dict[tuple[str, str], list[Segment]], output: Path,
) -> tuple[dict[str, Any], dict[str, list[tuple[Endpoint, Endpoint, Cell, Cell]]]]:
    writer = LedgerWriter(output, "CYCLIC_SEAM_P_SPAN_CELL_IDS")
    matches_by_seam: dict[str, list[tuple[Endpoint, Endpoint, Cell, Cell]]] = {}
    counts: Counter[str] = Counter()
    with writer:
        for seam_id, left, right in SEAMS:
            matches = matched_segments(
                seam_sides[(left[0], left[1])],
                seam_sides[(right[0], right[1])],
                "source-seam:" + seam_id,
            )
            matches_by_seam[seam_id] = matches
            total = (Q(0), Q(0))
            for lower, upper, left_cell, right_cell in matches:
                total = add_expression(total, span_expression(lower, upper))
                key = {
                    "seam": seam_id,
                    "span": [str(lower), str(upper)],
                    "left": left_cell.cell_id,
                    "right": right_cell.cell_id,
                }
                writer.write({
                    "face_id": "c32-source-seam:" + digest(key),
                    "classification": "SOURCE_CHART_TRANSFER_SEAM",
                    "terminal": False,
                    "seam_id": seam_id,
                    "left_chart": left[0],
                    "left_compact_endpoint": left[2],
                    "left_cell_id": left_cell.cell_id,
                    "right_chart": right[0],
                    "right_compact_endpoint": right[2],
                    "right_cell_id": right_cell.cell_id,
                    "physical_p_span": [
                        endpoint_descriptor(lower), endpoint_descriptor(upper),
                    ],
                    "exact_state_gluing_inherited_from_round162": True,
                    "dimension": 1,
                })
                counts[seam_id] += 1
            require(total == (Q(2), Q(0)), f"full seam span:{seam_id}")
    return ({**writer.descriptor(), "by_seam": dict(sorted(counts.items()))}, matches_by_seam)


def write_grazing(
    grazing_sides: dict[tuple[str, Q], list[Segment]], output: Path,
) -> dict[str, Any]:
    writer = LedgerWriter(output, "CHART_GRAZING_SIGN_T_SPAN_CELL_ID")
    counts: Counter[str] = Counter()
    with writer:
        for (chart, value), segments in sorted(
            grazing_sides.items(), key=lambda item: (item[0][0], item[0][1]),
        ):
            total = validate_side(segments, f"grazing:{chart}:{value}")
            require(total == (Q(0), Q(2)), f"grazing chart coverage:{chart}:{value}")
            for segment in sorted(segments, key=segment_sort_key):
                key = {
                    "chart": chart,
                    "p": str(value),
                    "span": [
                        endpoint_descriptor(segment.lower),
                        endpoint_descriptor(segment.upper),
                    ],
                    "cell": segment.cell.cell_id,
                }
                writer.write({
                    "face_id": "c32-grazing-face:" + digest(key),
                    "classification": "SOURCE_GRAZING_OR_CEMETERY",
                    "terminal_for_compact_geometry": True,
                    "compact_chart": chart,
                    "physical_p": str(value),
                    "compact_q": str(value),
                    "physical_t_span": [
                        endpoint_descriptor(segment.lower),
                        endpoint_descriptor(segment.upper),
                    ],
                    "incident_cell_id": segment.cell.cell_id,
                    "dimension": 1,
                    "round144_dynamic_cemetery_credit": 0,
                })
                counts[f"{chart}:p={value}"] += 1
    return {**writer.descriptor(), "by_chart_sign": dict(sorted(counts.items()))}


def corner_cell(matches: list[tuple[Endpoint, Endpoint, Cell, Cell]], value: Q) -> tuple[Cell, Cell]:
    selected = [
        (left, right)
        for lower, upper, left, right in matches
        if (value == -1 and lower == value) or (value == 1 and upper == value)
    ]
    require(len(selected) == 1, f"corner incidence:{value}")
    return selected[0]


def write_corners(
    matches_by_seam: dict[str, list[tuple[Endpoint, Endpoint, Cell, Cell]]],
    output: Path,
) -> dict[str, Any]:
    writer = LedgerWriter(output, "CYCLIC_SEAM_GRAZING_SIGN")
    with writer:
        for seam_id, *_rest in SEAMS:
            for value in (Q(-1), Q(1)):
                left, right = corner_cell(matches_by_seam[seam_id], value)
                key = {
                    "seam": seam_id,
                    "p": str(value),
                    "left": left.cell_id,
                    "right": right.cell_id,
                }
                writer.write({
                    "corner_id": "c32-source-corner:" + digest(key),
                    "classification": "SOURCE_GRAZING_CHART_GLUE_CORNER",
                    "terminal_for_compact_geometry": True,
                    "seam_id": seam_id,
                    "physical_p": str(value),
                    "compact_q": str(value),
                    "left_cell_id": left.cell_id,
                    "right_cell_id": right.cell_id,
                    "dimension": 0,
                    "round144_dynamic_cemetery_credit": 0,
                })
    require(writer.count == 8, "eight quotient corners")
    return writer.descriptor()


def write_events(cells: list[Cell], output: Path) -> dict[str, Any]:
    writer = LedgerWriter(output, "EVENT_KIND_CHART_ORIGIN_KEY")
    counts: Counter[str] = Counter()
    event_cells = sorted(
        (cell for cell in cells if cell.event is not None),
        key=lambda cell: (
            str(cell.event["event_kind"]), cell.compact_chart, cell.origin_key,
        ),
    )
    with writer:
        for cell in event_cells:
            require(cell.event is not None, "event payload")
            event_key = {
                "cell_id": cell.cell_id,
                "origin_key": cell.origin_key,
                "event": cell.event,
            }
            writer.write({
                "event_face_id": "c32-inherited-event:" + digest(event_key),
                "classification": "INHERITED_FIRST_COLLISION_TYPED_EVENT_GRAPH",
                "compact_chart": cell.compact_chart,
                "origin_key": cell.origin_key,
                "incident_cell_id": cell.cell_id,
                "event_payload": cell.event,
                "dimension": 1,
                "round144_R1648_event_family_credit": 0,
                "reason": "first-collision event typing is not a complete R1648 component-exit proof",
            })
            counts[str(cell.event["event_kind"])] += 1
    require(sum(counts.values()) == 336, "inherited event graph count")
    return {**writer.descriptor(), "by_event_kind": dict(sorted(counts.items()))}


def write_gap_ledger(output: Path) -> dict[str, Any]:
    writer = LedgerWriter(output, "ROUND144_REQUIRED_LEDGER_CLASS")
    rows = (
        (
            "COMPONENT_EXIT",
            "MISSING_FULL_R1648_COMPONENT_EXIT_REGISTRY",
            "bind every nonexcluded compact cell or stratum to a validated maximal-component exit",
        ),
        (
            "EVENT_FAMILY",
            "MISSING_COMPLETE_COMPETING_EVENT_FRONTIER",
            "upgrade inherited first-collision graphs to all R1648 event families with earliest-event margins",
        ),
        (
            "CONNECTED_COMPONENT",
            "MISSING_COMPACT_ATLAS_TO_ROUND161_CORRIDOR_CONNECTIVITY",
            "attach compact cells to the known 75-slab component through certified face paths",
        ),
        (
            "DISCONNECTED_EXTERIOR_SHEET",
            "MISSING_PER_ORIGIN_FINAL_DISPOSITION_CROSSWALK",
            "materialize row-level 74812 excluded and 2020 nonexcluded assignments, then exhaust every exterior sheet",
        ),
    )
    with writer:
        for ledger_class, blocker, required_next in rows:
            writer.write({
                "ledger_class": ledger_class,
                "status": blocker,
                "unresolved": True,
                "required_next": required_next,
                "formal_credit": 0,
            })
    return writer.descriptor()


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_bytes(canonical_bytes(value) + b"\n")


def make_result(
    inputs: dict[str, Any], cell_stats: dict[str, Any],
    ledgers: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    formal = inputs["formal"]
    paths = inputs["paths"]
    result: dict[str, Any] = {
        "schema": SCHEMA,
        "status": (
            "PASS_EXACT_FOUR_CHART_COMPACT_S0_CELL_ADJACENCY_SEAM_GRAZING_"
            "CORNER_AND_INHERITED_EVENT_LEDGER__D02_STILL_BLOCKED"
        ),
        "versioned_compact_atlas": {
            "source_obstacle": "W",
            "physical_domain": "S^1_A x [-1,1]_p",
            "compact_charts": list(COMPACT_CHARTS),
            "physical_slice": "s=0",
            "source_W_refined_origin_count": 76832,
            "compact_cell_count": 76832,
            "guard_band_only_cells": 0,
            "guard_band_clipped_cells": (
                cell_stats["clipping"].get("NEGATIVE_GUARD_BAND_CLIPPED", 0)
                + cell_stats["clipping"].get("POSITIVE_GUARD_BAND_CLIPPED", 0)
            ),
            "Round165_parent_records_replaced": 618,
            "Round165_terminal_records_installed": 622,
            "record_delta": 4,
            "cell_census_by_chart": cell_stats["per_chart"],
            "guard_band_clipping_census": cell_stats["clipping"],
            "physical_area_by_chart_in_basis_1_and_1_over_sqrt_2": cell_stats[
                "area_by_chart"
            ],
            "physical_total_area_in_basis_1_and_1_over_sqrt_2": cell_stats[
                "total_area"
            ],
            "cell_area_identity": "4 charts * 4/sqrt(2) = 8*sqrt(2)",
        },
        "source_classification_census": {
            "untouched_base": cell_stats["base_classifications"],
            "Round165_terminals": cell_stats["round165_terminal_classifications"],
            "inherited_first_collision_event_graph_cells": cell_stats[
                "inherited_event_graph_cell_count"
            ],
        },
        "ledgers": ledgers,
        "formal_source_W_zero_authority": {
            "path": str(paths["formal"].relative_to(ROOT)),
            "file_sha256": file_sha256(paths["formal"]),
            "object_sha256": formal["object_sha256"],
            "current_state": formal["current_state"],
            "aggregate_conservation_is_not_a_row_level_D02_component_crosswalk": True,
        },
        "round144_terminal_census": {
            "required_classes": [
                "CONNECTED_TO_KNOWN",
                "TYPED_EVENT_GRAPH",
                "EARLIEST_PREFIX_EXCLUDED",
                "SOURCE_GRAZING_OR_CEMETERY",
            ],
            "row_level_dynamic_assignments_materialized": False,
            "CONNECTED_TO_KNOWN": 0,
            "TYPED_EVENT_GRAPH": 0,
            "EARLIEST_PREFIX_EXCLUDED": 0,
            "SOURCE_GRAZING_OR_CEMETERY_cell_or_sheet": 0,
            "UNRESOLVED_COMPACT_CELLS": 76832,
            "geometric_grazing_faces_typed_without_dynamic_cemetery_credit": (
                ledgers["grazing"]["row_count"]
            ),
            "geometric_grazing_corners_typed_without_dynamic_cemetery_credit": 8,
            "unresolved_zero": False,
        },
        "strict_nonpromotion": {
            "D02": "BLOCKED_PENDING_COMPONENT_EXIT_AND_EXTERIOR_TERMINAL_CENSUS",
            "D03": "UNAUTHORIZED",
            "D04": "NOT_MINTED",
            "Gate5": "10/18",
            "complete_global_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "required_next": (
            "materialize the row-level final-disposition crosswalk, attach every "
            "nonexcluded stratum to the known Round161 component or a complete "
            "typed event/cemetery exit, and independently prove the four-class "
            "Round144 terminal census has unresolved=0"
        ),
        "provenance": {
            "bridge_result_sha256": inputs["bridge"]["result_sha256"],
            "Round165_result_sha256": inputs["round165"]["result_sha256"],
            "formal_source_W_ledger_object_sha256": formal["object_sha256"],
            "dependency_file_sha256": {
                str(path.relative_to(ROOT)): file_sha256(path)
                for path in (
                    paths["bridge"], paths["round165"], paths["formal"],
                    DELIVERABLES / "cm2_gate3_eight_cell_symmetry_atlas_cert.py",
                    DELIVERABLES / "cm2_round165_adaptive_typed_seam_census.py",
                )
            },
        },
    }
    result["object_sha256"] = digest(result)
    return result


def build(output: Path, formal_ledger: Path, workers: int) -> dict[str, Any]:
    require(workers in {1, 2}, "workers must be 1 or 2")
    require(not output.exists(), f"output exists:{output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    stage = output.with_name(output.name + f".stage-{os.getpid()}")
    require(not stage.exists(), f"stage exists:{stage}")
    stage.mkdir()
    try:
        inputs = validate_inputs(formal_ledger.resolve())
        cell_writer = LedgerWriter(
            stage / "compact_cells.jsonl.gz", "LEXICOGRAPHIC_SOURCE_W_ORIGIN_KEY",
        )
        with cell_writer:
            cells, cell_stats = build_cells(inputs, workers, cell_writer)
        adjacency, seam_sides, grazing_sides = write_adjacency(
            cells, stage / "intra_chart_adjacency.jsonl.gz",
        )
        seams, seam_matches = write_seams(
            seam_sides, stage / "source_chart_seams.jsonl.gz",
        )
        grazing = write_grazing(
            grazing_sides, stage / "source_grazing_faces.jsonl.gz",
        )
        corners = write_corners(
            seam_matches, stage / "source_grazing_corners.jsonl.gz",
        )
        events = write_events(cells, stage / "inherited_event_faces.jsonl.gz")
        gaps = write_gap_ledger(stage / "round144_component_exit_exterior_gaps.jsonl.gz")
        ledgers = {
            "cells": cell_writer.descriptor(),
            "intra_chart_adjacency": adjacency,
            "source_chart_seams": seams,
            "grazing": grazing,
            "corners": corners,
            "inherited_event_faces": events,
            "component_exit_exterior_gaps": gaps,
        }
        result = make_result(inputs, cell_stats, ledgers)
        write_json(stage / "result.json", result)
        manifest_members = sorted(
            path for path in stage.iterdir() if path.name != "root_manifest.sha256"
        )
        manifest = "".join(
            f"{file_sha256(path)}  {path.name}\n" for path in manifest_members
        )
        (stage / "root_manifest.sha256").write_text(manifest, encoding="utf-8")
        marker = {
            "status": "PASS_FOUNDATION_ONLY__D02_NOT_PROMOTED",
            "result_object_sha256": result["object_sha256"],
            "root_manifest_sha256": file_sha256(stage / "root_manifest.sha256"),
        }
        write_json(stage / "FOUNDATION_ONLY.lock", marker)
        os.replace(stage, output)
        return result
    except BaseException:
        shutil.rmtree(stage, ignore_errors=True)
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--formal-ledger", type=Path, required=True)
    parser.add_argument("--atlas-workers", type=int, default=2)
    args = parser.parse_args()
    result = build(args.output.resolve(), args.formal_ledger, args.atlas_workers)
    print(canonical_bytes({
        "status": result["status"],
        "object_sha256": result["object_sha256"],
        "output": str(args.output.resolve()),
    }).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
