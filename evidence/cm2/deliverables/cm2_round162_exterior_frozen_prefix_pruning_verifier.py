#!/usr/bin/env python3
"""Independent fail-closed verifier for the Round162 exterior prefix block."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
CERTIFICATE = HERE / "cm2_round162_exterior_frozen_prefix_pruning_certificate.json"
OUTPUT = HERE / "cm2_round162_exterior_frozen_prefix_pruning_verification.json"
CERTIFICATE_SCHEMA = "cm2.round162.exterior-frozen-prefix-pruning.v1"
SCHEMA = "cm2.round162.exterior-frozen-prefix-pruning.verification.v1"
STATUS = (
    "CERTIFIED_ONE_FROZEN_PREFIX_WW_OPEN_CELL_EXCLUSION__"
    "EXTERIOR_AND_D02_STILL_BLOCKED"
)
PRODUCER = "cm2_round162_exterior_frozen_prefix_pruning.py"
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
    PRODUCER:
        "279ccd29c21bc273fccf594a0fef5e658e0aead5b91e2d421ef46b556d3a63cd",
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
DEPENDENCY_PINS = {key: value for key, value in PINS.items() if key != PRODUCER}
ROUND139_RESULT_SHA256 = (
    "6e8f54c34154ea5ba3c95d4e901bc643c020a0a42e180241ae9053bb24f42236"
)
SOURCE_W_CHARTS = ("W:E", "W:W", "W:N", "W:S")
FROZEN_TARGET = "W[1,0]"

RADIUS = {"G": Q(9, 25), "W": Q(4, 25)}
EPS = Q(1, 400)
TAU_MAX = Q(3)
INV_SQRT2_LOWER = Q(707, 1000)
INV_SQRT2_UPPER = Q(708, 1000)


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


def strict_load_raw(raw: bytes) -> dict[str, Any]:
    require(not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw, "encoding")

    def reject(value: str) -> None:
        raise ValueError(value)

    def reject_float(value: str) -> None:
        raise ValueError(value)

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, "duplicate key")
            result[key] = value
        return result

    document = json.loads(
        raw.decode("utf-8"), object_pairs_hook=unique, parse_constant=reject,
        parse_float=reject_float,
    )

    def check_strings(value: Any) -> None:
        if type(value) is str:
            require(
                "\x00" not in value
                and not any(0xD800 <= ord(character) <= 0xDFFF for character in value),
                "decoded string encoding",
            )
        elif type(value) is list:
            for item in value:
                check_strings(item)
        elif type(value) is dict:
            for key, item in value.items():
                check_strings(key)
                check_strings(item)

    check_strings(document)
    require(type(document) is dict, "top object")
    return document


def strict_load(path: Path) -> dict[str, Any]:
    return strict_load_raw(path.read_bytes())


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


def displacement_bounds(source: str, target: Target) -> tuple[Q, Q, Q, Q]:
    ix, iy = target.ix, target.iy
    if source == target.obstacle:
        return Q(ix), Q(ix), Q(iy), Q(iy)
    if source == "G":
        x = Q(2 * ix + 1, 2)
        return x - EPS, x + EPS, Q(2 * iy + 1, 2), Q(2 * iy + 1, 2)
    x = Q(2 * ix - 1, 2)
    return x - EPS, x + EPS, Q(2 * iy - 1, 2), Q(2 * iy - 1, 2)


def min_square(lower: Q, upper: Q) -> Q:
    return Q(0) if lower <= 0 <= upper else min(lower * lower, upper * upper)


def maximum_abs(lower: Q, upper: Q) -> Q:
    return max(abs(lower), abs(upper))


def cell_support(cell: str, bounds: tuple[Q, Q, Q, Q]) -> Q:
    x0, x1, y0, y1 = bounds
    if cell == "E":
        along, transverse = x1, maximum_abs(y0, y1)
    elif cell == "W":
        along, transverse = -x0, maximum_abs(y0, y1)
    elif cell == "N":
        along, transverse = y1, maximum_abs(x0, x1)
    elif cell == "S":
        along, transverse = -y0, maximum_abs(x0, x1)
    else:
        raise ValueError(cell)
    cosine = Q(1) if along >= 0 else INV_SQRT2_LOWER
    return along * cosine + transverse * INV_SQRT2_UPPER


def independent_classification(
    source: str, cell: str, target: Target
) -> tuple[str, str]:
    if target.obstacle == source and (target.ix, target.iy) == (0, 0):
        return (
            "self_source",
            "same strictly convex source lift; outgoing interior rays do not re-enter it",
        )
    bounds = displacement_bounds(source, target)
    x0, x1, y0, y1 = bounds
    distance2 = min_square(x0, x1) + min_square(y0, y1)
    horizon = TAU_MAX + RADIUS[source] + RADIUS[target.obstacle]
    if distance2 >= horizon * horizon:
        return (
            "empty_horizon_center_distance",
            f"min_center_distance^2={distance2} >= "
            f"(3+R_source+R_target)^2={horizon * horizon}",
        )
    upper = cell_support(cell, bounds)
    threshold = RADIUS[source] - RADIUS[target.obstacle]
    if upper < threshold:
        return (
            "empty_outgoing_halfspace",
            f"support_upper={upper} < R_source-R_target={threshold}",
        )
    return (
        "retained_candidate",
        "not excluded by certified horizon and outgoing-halfspace necessary conditions",
    )


def independent_rows(chart_id: str) -> list[dict[str, str]]:
    source, cell = chart_id.split(":")
    return [
        {
            "target_id": target.target_id,
            "classification": independent_classification(source, cell, target)[0],
            "proof": independent_classification(source, cell, target)[1],
        }
        for target in TARGETS
    ]


def independent_candidates(chart_id: str) -> list[str]:
    return [
        row["target_id"] for row in independent_rows(chart_id)
        if row["classification"] == "retained_candidate"
    ]


def check_pins() -> None:
    for name, expected in PINS.items():
        require(
            hashlib.sha256((HERE / name).read_bytes()).hexdigest() == expected,
            f"pin:{name}",
        )


def rebuild_expected() -> dict[str, Any]:
    atlas = strict_load(HERE / GATE3_ATLAS)
    first_hit = strict_load(HERE / GATE3_FIRST_HIT)
    r139_document = strict_load(HERE / ROUND139)
    require(
        set(r139_document) == {"schema", "result", "result_sha256"}
        and r139_document["result_sha256"] == ROUND139_RESULT_SHA256
        and digest(r139_document["result"]) == ROUND139_RESULT_SHA256,
        "Round139 wrapper",
    )
    r139 = r139_document["result"]
    require(
        r139["corrected_rank3_source_contract"]["source_chart"] == "W:E"
        and r139["corrected_rank3_source_contract"]["source_target"]
        == FROZEN_TARGET,
        "Round139 source",
    )
    for rows_name in ("collision_rows", "positive_area_collision_rows"):
        row = r139[rows_name][0]
        require(
            row["collision_index"] == 1
            and row["selected_absolute_owner_id"] == FROZEN_TARGET
            and row["relative_frozen_target_id"] == FROZEN_TARGET
            and row["outgoing_chart"] == "W",
            f"Round139 prefix:{rows_name}",
        )

    require(
        atlas["schema"] == "cm2.gate3.eight-cell-symmetry-atlas.v1"
        and atlas["coverage"]["global_leaf_count"] == 143248,
        "Gate3 atlas",
    )
    hit_rows = {
        row["chart_id"]: row
        for row in first_hit["candidate_reduction"]["charts"]
    }
    charts: list[dict[str, Any]] = []
    for chart_id in SOURCE_W_CHARTS:
        atlas_row = atlas["charts"][chart_id]
        hit_row = hit_rows[chart_id]
        candidates = independent_candidates(chart_id)
        rows = independent_rows(chart_id)
        require(
            len(candidates) == atlas_row["candidate_count"] == hit_row["retained"]
            == 55,
            f"candidate count:{chart_id}",
        )
        require(
            digest(candidates) == hit_row["candidate_sha256"]
            and digest(rows) == hit_row["classification_sha256"],
            f"candidate registry:{chart_id}",
        )
        counts = atlas_row["counts"]
        require(
            sum(counts.values()) == atlas_row["leaf_count"],
            f"chart census:{chart_id}",
        )
        charts.append({
            "chart_id": chart_id,
            "candidate_count": len(candidates),
            "candidate_ids_sha256": digest(candidates),
            "classification_rows_sha256": digest(rows),
            "frozen_target_retained": FROZEN_TARGET in candidates,
            "leaf_count": atlas_row["leaf_count"],
            "counts": counts,
            "leaf_rows_sha256": atlas_row["leaf_rows_sha256"],
            "provenance": atlas_row["provenance"],
        })

    aggregate = {
        "leaf_count": sum(row["leaf_count"] for row in charts),
        "unique_first": sum(row["counts"]["unique_first"] for row in charts),
        "tangency_graph": sum(row["counts"]["tangency_graph"] for row in charts),
        "multi_candidate": sum(row["counts"]["multi_candidate"] for row in charts),
    }
    require(
        aggregate == {
            "leaf_count": 76828,
            "unique_first": 26204,
            "tangency_graph": 56,
            "multi_candidate": 50568,
        },
        "aggregate census",
    )
    ww = next(row for row in charts if row["chart_id"] == "W:W")
    target_class, witness = independent_classification(
        "W", "W", Target("W", 1, 0)
    )
    require(
        target_class == "empty_outgoing_halfspace"
        and witness == "support_upper=-707/1000 < R_source-R_target=0"
        and not ww["frozen_target_retained"],
        "exact W:W exclusion",
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
            "dependency_sha256": DEPENDENCY_PINS,
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
        "source_W_atlas": {"charts": charts, "aggregate": aggregate},
        "certified_open_cell_block": {
            "disposition": "EARLIEST_PREFIX_EXCLUDED",
            "chart_id": "W:W",
            "region":
                "open chart interior; exact exclusion extends to the closed "
                "conservative Gate3 chart cover",
            "excluded_frozen_target": FROZEN_TARGET,
            "exact_candidate_classification": target_class,
            "exact_witness": witness,
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


def validate_document(document: dict[str, Any]) -> dict[str, Any]:
    require(
        set(document) == {"schema", "result", "result_sha256"},
        "certificate wrapper",
    )
    require(document["schema"] == CERTIFICATE_SCHEMA, "certificate schema")
    require(type(document["result_sha256"]) is str, "result digest type")
    require(digest(document["result"]) == document["result_sha256"], "result digest")
    expected = rebuild_expected()
    require(canonical(document["result"]) == canonical(expected), "full result")
    return expected


def assign(document: dict[str, Any], path: tuple[Any, ...], value: Any) -> dict[str, Any]:
    mutated = copy.deepcopy(document)
    cursor: Any = mutated
    for key in path[:-1]:
        cursor = cursor[key]
    cursor[path[-1]] = value
    mutated["result_sha256"] = digest(mutated["result"])
    return mutated


def semantic_attacks(document: dict[str, Any]) -> dict[str, bool]:
    cases = {
        "frozen owner changed": assign(
            document, ("result", "frozen_prefix", "selected_owner"), "W[0,0]"
        ),
        "outgoing chart changed": assign(
            document, ("result", "frozen_prefix", "outgoing_chart"), "E"
        ),
        "disposition promoted": assign(
            document, ("result", "certified_open_cell_block", "disposition"),
            "CONNECTED_TO_KNOWN",
        ),
        "target presence invented": assign(
            document,
            ("result", "certified_open_cell_block", "frozen_target_in_candidate_list"),
            True,
        ),
        "exact witness altered": assign(
            document, ("result", "certified_open_cell_block", "exact_witness"), "0<0"
        ),
        "candidate count altered": assign(
            document, ("result", "certified_open_cell_block", "candidate_count"), 54
        ),
        "leaf count altered": assign(
            document, ("result", "certified_open_cell_block", "covered_atlas_leaf_count"),
            18929,
        ),
        "unique credit inflated": assign(
            document,
            (
                "result", "certified_open_cell_block",
                "unique_first_immediate_short_circuit_credit",
            ),
            26204,
        ),
        "excluded leaf count reduced": assign(
            document,
            (
                "result", "certified_open_cell_block",
                "frozen_prefix_excluded_leaf_count",
            ),
            6518,
        ),
        "aggregate unique altered": assign(
            document,
            ("result", "source_W_atlas", "aggregate", "unique_first"),
            26205,
        ),
        "tangency queue erased": assign(
            document,
            ("result", "global_all_signature_queue", "source_W_tangency_graph_total"),
            0,
        ),
        "multi queue erased": assign(
            document,
            ("result", "global_all_signature_queue", "source_W_multi_candidate_total"),
            0,
        ),
        "unresolved zero invented": assign(
            document,
            (
                "result", "frozen_prefix_pruning_census",
                "frozen_prefix_unresolved_leaves_zero",
            ),
            True,
        ),
        "all exterior promoted": assign(
            document,
            ("result", "strict_nonpromotion", "all_disconnected_exterior_sheets_excluded"),
            True,
        ),
        "D02 promoted": assign(
            document, ("result", "strict_nonpromotion", "D02"), "CERTIFIED"
        ),
        "bool-int confusion": assign(
            document, ("result", "frozen_prefix", "collision_index"), True
        ),
        "dependency pin altered": assign(
            document,
            ("result", "provenance", "dependency_sha256", GATE3_ATLAS),
            "0" * 64,
        ),
    }
    result: dict[str, bool] = {}
    for name, attack in cases.items():
        try:
            validate_document(attack)
        except Exception:
            result[name] = True
        else:
            result[name] = False
    return result


def strict_json_attacks(document: dict[str, Any]) -> dict[str, bool]:
    raw = canonical(document).encode()
    texts = {
        "duplicate top key": b'{"schema":"x","schema":"y","result":{},"result_sha256":"z"}',
        "UTF8 BOM": b"\xef\xbb\xbf" + raw,
        "literal NUL": raw + b"\x00",
        "float injected": raw.replace(b'"collision_index":1', b'"collision_index":1.0'),
        "NaN injected": raw.replace(b'"collision_index":1', b'"collision_index":NaN'),
        "escaped NUL": raw.replace(b'"source_chart":"W:E"', b'"source_chart":"W:\\u0000E"'),
        "Unicode surrogate": raw.replace(
            b'"source_chart":"W:E"', b'"source_chart":"W:\\ud800E"'
        ),
    }
    outcomes: dict[str, bool] = {}
    for name, payload in texts.items():
        try:
            parsed = strict_load_raw(payload)
            validate_document(parsed)
        except Exception:
            outcomes[name] = True
        else:
            outcomes[name] = False
    return outcomes


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    check_pins()
    document = strict_load(CERTIFICATE)
    expected = validate_document(document)
    semantics = semantic_attacks(document)
    strict = strict_json_attacks(document)
    require(all(semantics.values()), "semantic attack escaped")
    require(all(strict.values()), "strict JSON attack escaped")
    if args.self_test:
        print("ROUND162_EXTERIOR_FROZEN_PREFIX_SELF_TEST: PASS")
        return
    result = {
        "status": "PASS",
        "certificate_schema": CERTIFICATE_SCHEMA,
        "certificate_result_sha256": document["result_sha256"],
        "independent_candidate_registries_rebuilt": True,
        "independent_source_W_census_rebuilt": True,
        "independent_Round139_prefix_rebuilt": True,
        "certified_disposition":
            expected["certified_open_cell_block"]["disposition"],
        "semantic_attack_results": semantics,
        "semantic_attack_rejection_count": sum(semantics.values()),
        "strict_json_attack_results": strict,
        "strict_json_attack_rejection_count": sum(strict.values()),
        "strict_nonpromotion_rechecked": expected["strict_nonpromotion"],
        "producer_imported_or_executed": False,
    }
    output = {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}
    OUTPUT.write_text(
        json.dumps(output, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(canonical({
        "output": OUTPUT.name,
        "result_sha256": output["result_sha256"],
        "status": result["status"],
    }))


if __name__ == "__main__":
    main()
