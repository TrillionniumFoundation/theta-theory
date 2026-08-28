#!/usr/bin/env python3
"""Round299B signed-support replay for graph-constrained Round292 faces.

The Round299A coordinate sweep deliberately left every face incident to a
REGULAR_GRAPH_CROSSING support unpromoted.  This diagnostic replays the frozen
active factor on those 26,264 faces.

For a non-square ``t^2`` endpoint, the script never substitutes a floating or
rational value for the exact physical ``t``.  It evaluates nested rational
dyadic outer enclosures of the signed square root at 96, 192, and 384 bits and
requires identical classifications.  Every accepted face also receives an
explicit strict desired-side witness inside the two-dimensional face.  The
producer remains zero-credit: it freezes evidence and exclusions but does not
decide occurrence identity versus component-edge semantics.

Run in an environment providing python-flint, for example:

    uv run --with python-flint python <this-file>
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import math
import os
import sys
import tempfile
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

from flint import __version__ as FLINT_VERSION
from flint import ctx


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import cm2_round174_source_g_unique_first_dynamic_occurrence_materialization as r174
import cm2_round179_source_g_residual_tube_arrangement as r179
import cm2_round274_source_g_reverse_rechart_tail_arrangement_probe as r274
import cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe as r287


PREFIX = "cm2_round299b_source_g_r292_signed_support_face_replay_diagnostic"
OUTPUT = HERE / f"{PREFIX}_result.json"
LEDGER = HERE / f"{PREFIX}_ledger.json.gz"

R174P = "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization.py"
R179P = "cm2_round179_source_g_residual_tube_arrangement.py"
R274P = "cm2_round274_source_g_reverse_rechart_tail_arrangement_probe.py"
R275 = "cm2_round275_source_g_complete_reverse_rechart_materialization_certificate.json"
R287P = "cm2_round287_source_g_rechart_terminal_occurrence_disposition_probe.py"
R299A = "cm2_round299_source_g_r292_complete_common_face_frontier_diagnostic_probe_ledger.json.gz"
R295A = (
    "cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_"
    "physical_witness_incidence_binding_ledger.json.gz"
)

PINS = {
    R174P: "3d329525dda6697a3a5d2a8227c94bd9c309ea7ebcc4cdd0c7fbe573c267a218",
    R179P: "8c568c58d82708a7ab549f126c1fcedfccff563d1d00e3c1f7e6545b4b0d29ab",
    R274P: "677813e132d62732900a26edc3fae5d562049d8d1fac2cea59f7c65d41735292",
    R275: "e18935169614fc8b62ead3be7f60b383396ea1d2c52e8151457241f49e770386",
    R287P: "b39849e3aee21688ccf3eb5443984e9e0e8d7a88ed2d61e059ed3485d84c780d",
    R299A: "b9de98c7ccb3051ea7af3070e1eb62ce059d21f0b22b9b3f5007c1847c667845",
    R295A: "2d9addfc9fca55366a58b29a7084c063674c3f556dd5398b038ae7d51fe97dcf",
}

SCHEMA = "cm2.round299b.source-g-r292-signed-support-face-replay-diagnostic.v1"
LEDGER_SCHEMA = SCHEMA + ".ledger.v1"
ENC = json.JSONEncoder(
    sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
)
REPLAY_BITS = (96, 192, 384)
ctx.prec = 768


def canonical(value: Any) -> bytes:
    return ENC.encode(value).encode()


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            result.update(chunk)
    return result.hexdigest()


def need(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def read_json(name: str) -> dict[str, Any]:
    path = HERE / name
    need(file_sha256(path) == PINS[name], f"pin:{name}")
    return json.loads(path.read_bytes())


def read_gzip(name: str) -> dict[str, Any]:
    path = HERE / name
    need(file_sha256(path) == PINS[name], f"pin:{name}")
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        return json.load(handle)


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def closed(payload: dict[str, Any]) -> dict[str, Any]:
    result = dict(payload)
    result["row_sha256"] = digest(result)
    return result


def deterministic_gzip_bytes(value: Any) -> bytes:
    buffer = io.BytesIO()
    with gzip.GzipFile(
        filename="", mode="wb", fileobj=buffer, compresslevel=9, mtime=0
    ) as handle:
        handle.write(canonical(value))
    return buffer.getvalue()


def atomic(path: Path, payload: bytes) -> None:
    descriptor, temporary = tempfile.mkstemp(
        prefix="." + path.name + ".", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def load_regions() -> dict[str, dict[str, Any]]:
    wrapper = read_json(R275)
    need(wrapper["result_sha256"] == digest(wrapper["result"]), "R275 result")
    result = wrapper["result"]
    rows = [
        row
        for table in ("strict_region_ledger", "arrangement_region_ledger")
        for row in result[table]["rows"]
    ]
    need(len(rows) == 13_788, "R275 region census")
    return {row["reverse_rechart_region_row_id"]: row for row in rows}


def dyadic_sqrt_outer(value: Q, bits: int) -> tuple[Q, Q]:
    need(value >= 0, "nonnegative t^2")
    numerator_root = math.isqrt(value.numerator)
    denominator_root = math.isqrt(value.denominator)
    if (
        numerator_root * numerator_root == value.numerator
        and denominator_root * denominator_root == value.denominator
    ):
        exact = Q(numerator_root, denominator_root)
        return exact, exact
    scale = 1 << bits
    scaled_numerator = value.numerator * scale * scale
    lower_integer = math.isqrt(scaled_numerator // value.denominator)
    while (
        (lower_integer + 1) * (lower_integer + 1) * value.denominator
        <= scaled_numerator
    ):
        lower_integer += 1
    while (
        lower_integer * lower_integer * value.denominator
        > scaled_numerator
    ):
        lower_integer -= 1
    return Q(lower_integer, scale), Q(lower_integer + 1, scale)


def signed_t_outer(
    lower_square: Q, upper_square: Q, sign: int, bits: int
) -> tuple[Q, Q]:
    lower_lo, _lower_hi = dyadic_sqrt_outer(lower_square, bits)
    _upper_lo, upper_hi = dyadic_sqrt_outer(upper_square, bits)
    if sign > 0:
        return lower_lo, upper_hi
    need(sign == -1, "physical t sign")
    return -upper_hi, -lower_lo


def coordinate_enclosure(
    face: tuple[Q, ...], sign: int, bits: int
) -> tuple[Q, ...]:
    return (
        *signed_t_outer(face[0], face[1], sign, bits),
        *face[2:],
    )


def graph_metadata(
    source: dict[str, Any],
    regions: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    result = []
    for side in ("left", "right"):
        if "REGULAR_GRAPH_CONSTRAINED" not in source[
            f"{side}_inherited_signed_support_state"
        ]:
            continue
        region_id = source[f"{side}_Round275_region_id"]
        region = regions[region_id]
        need(
            region.get("arrangement_classification")
            == "REGULAR_GRAPH_CROSSING",
            "graph-constrained endpoint parent",
        )
        result.append(
            {
                "endpoint_side": side,
                "region_id": region_id,
                "region": region,
                "factor_identity": (
                    region["adjacent_chart"],
                    region["owner_target"],
                    region["active_reason"],
                ),
                "desired_sign": region["active_factor_side_sign"],
            }
        )
    need(len(result) in {1, 2}, "one or two graph endpoints")
    return result


def signed_state(
    region: dict[str, Any],
    face: tuple[Q, ...],
    sign: int,
    bits: int,
) -> tuple[str, list[str], tuple[Q, ...]]:
    enclosure = coordinate_enclosure(face, sign, bits)
    state, extrema = r287.signed_region_cell_state(region, enclosure)
    return state, extrema, enclosure


def active_factor_sign(
    region: dict[str, Any],
    t_lower: Q,
    t_upper: Q,
    p: Q,
    s: Q,
) -> str:
    box = r174.atlas.AtlasBox(
        t_lower, t_upper, p, p, s, s, 0, "round299b-face-witness"
    )
    value = r274.active_dual(
        r179.interval_geometry(
            region["adjacent_chart"], region["owner_target"], box
        ),
        region["active_reason"],
    )[0]
    return r179.sign(value)


def strict_desired_witness(
    region: dict[str, Any],
    face: tuple[Q, ...],
    axis: int,
    physical_t_sign: int,
) -> dict[str, Any]:
    desired = region["active_factor_side_sign"]
    derivatives = region["strict_derivative_signs_t_p_s"]
    need(
        derivatives[0] in {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
        and derivatives[1] in {"STRICT_NEGATIVE", "STRICT_POSITIVE"}
        and derivatives[2]
        in {"STRICT_NEGATIVE", "STRICT_POSITIVE", "OVERWRAP"},
        "frozen active-factor derivative classification",
    )
    for inward_depth in range(1, 33):
        epsilon = Q(1, 1 << inward_depth)
        if axis == 0:
            t_lower, t_upper = signed_t_outer(
                face[0], face[1], physical_t_sign, REPLAY_BITS[-1]
            )
        else:
            outer_lower, outer_upper = signed_t_outer(
                face[0], face[1], physical_t_sign, REPLAY_BITS[-1]
            )
            maximize = (
                (desired == "STRICT_POSITIVE")
                == (derivatives[0] == "STRICT_POSITIVE")
            )
            t_value = (
                outer_upper - epsilon * (outer_upper - outer_lower)
                if maximize
                else outer_lower + epsilon * (outer_upper - outer_lower)
            )
            t_lower = t_upper = t_value

        coordinates: list[Q] = []
        for current_axis in (1, 2):
            lower = face[2 * current_axis]
            upper = face[2 * current_axis + 1]
            if current_axis == axis:
                value = lower
            elif derivatives[current_axis] == "OVERWRAP":
                value = (lower + upper) / 2
            else:
                maximize = (
                    (desired == "STRICT_POSITIVE")
                    == (derivatives[current_axis] == "STRICT_POSITIVE")
                )
                value = (
                    upper - epsilon * (upper - lower)
                    if maximize
                    else lower + epsilon * (upper - lower)
                )
            coordinates.append(value)
        replay_sign = active_factor_sign(
            region,
            t_lower,
            t_upper,
            coordinates[0],
            coordinates[1],
        )
        if replay_sign == desired:
            return {
                "inward_dyadic_depth": inward_depth,
                "signed_t_rational_enclosure_or_exact_point": [
                    qstr(t_lower),
                    qstr(t_upper),
                ],
                "p": qstr(coordinates[0]),
                "s": qstr(coordinates[1]),
                "strict_active_factor_sign": replay_sign,
                "desired_active_factor_sign": desired,
                "witness_is_strictly_interior_in_every_free_face_axis": True,
                "non_square_fixed_t_is_kept_inside_rational_outer_enclosure":
                    axis == 0 and t_lower != t_upper,
            }
    raise RuntimeError("strict desired-side face witness not found")


def replay_row(
    source: dict[str, Any],
    regions: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    graphs = graph_metadata(source, regions)
    face = tuple(map(Q, source["exact_positive_area_coordinate_face"]))
    axis = source["common_face_axis"]
    physical_t_sign = source["physical_t_sign"]
    same_factor = (
        len(graphs) == 2
        and graphs[0]["factor_identity"] == graphs[1]["factor_identity"]
    )
    opposite_sign = (
        same_factor
        and graphs[0]["desired_sign"] != graphs[1]["desired_sign"]
    )

    replays = []
    witness = None
    if opposite_sign:
        factor_relation = "SAME_ACTIVE_FACTOR__OPPOSITE_STRICT_DESIRED_SIDES"
        replay_state = "NOT_APPLICABLE__EXACT_STRICT_SIDE_EXCLUSION"
        disposition = (
            "NO_POSITIVE_AREA_SIGNED_SUPPORT_COMMON_FACE__"
            "COMMON_ZERO_SET_LOWER_FRONTIER_NOT_DECIDED_HERE"
        )
    else:
        factor_relation = (
            "SAME_ACTIVE_FACTOR__SAME_STRICT_DESIRED_SIDE"
            if same_factor
            else "ONE_GRAPH_ENDPOINT__OTHER_ENDPOINT_FULL_SIGNED_SUPPORT"
        )
        region = graphs[0]["region"]
        for bits in REPLAY_BITS:
            state, extrema, enclosure = signed_state(
                region, face, physical_t_sign, bits
            )
            replays.append(
                {
                    "dyadic_sqrt_outer_enclosure_bits": bits,
                    "signed_t_rational_outer_enclosure": [
                        qstr(enclosure[0]),
                        qstr(enclosure[1]),
                    ],
                    "signed_region_face_state": state,
                    "active_factor_extremal_signs": extrema,
                }
            )
        states = {row["signed_region_face_state"] for row in replays}
        extrema = {
            tuple(row["active_factor_extremal_signs"]) for row in replays
        }
        need(len(states) == len(extrema) == 1, "precision-stable face replay")
        replay_state = replays[-1]["signed_region_face_state"]
        if replay_state == "EMPTY_OPPOSITE_SIDE_COORDINATE_CELL":
            disposition = "SIGNED_SUPPORT_FACE_EMPTY__NO_PHYSICAL_COMMON_FACE"
        else:
            need(
                replay_state in {
                    "FULL_DESIRED_SIDE_SUPPORT",
                    "CLIPPED_DESIRED_SIDE_SUPPORT",
                },
                "decisive signed face state",
            )
            witness = strict_desired_witness(
                region, face, axis, physical_t_sign
            )
            disposition = (
                "POSITIVE_AREA_SIGNED_SUPPORT_COMMON_FACE_CERTIFIED__"
                "IDENTITY_VERSUS_COMPONENT_EDGE_SEMANTICS_PENDING"
            )

    payload = {
        "Round299B_signed_support_face_replay_row_id":
            "round299b-signed-support-face-replay:"
            + digest(source["Round299_R292_coordinate_common_face_row_id"]),
        "source_Round299_R292_coordinate_common_face_row_id":
            source["Round299_R292_coordinate_common_face_row_id"],
        "source_Round299_row_sha256": source["row_sha256"],
        "endpoint_pair_kind": source["endpoint_pair_kind"],
        "same_Round287_support_union": source["same_Round287_support_union"],
        "same_complete_10_field_return_signature":
            source["same_complete_10_field_return_signature"],
        "unordered_nonself_formal_occurrence_endpoint_pair":
            source["unordered_nonself_formal_occurrence_endpoint_pair"],
        "common_face_axis": axis,
        "exact_positive_area_coordinate_face_t2_p_s":
            source["exact_positive_area_coordinate_face"],
        "physical_t_sign": physical_t_sign,
        "graph_endpoint_count": len(graphs),
        "graph_endpoint_regions": [
            {
                "endpoint_side": graph["endpoint_side"],
                "Round275_region_id": graph["region_id"],
                "active_factor_identity": list(graph["factor_identity"]),
                "active_factor_desired_sign": graph["desired_sign"],
            }
            for graph in graphs
        ],
        "active_factor_relation": factor_relation,
        "precision_replays": replays,
        "precision_stable_signed_region_face_state": replay_state,
        "strict_desired_side_face_witness": witness,
        "signed_support_face_disposition": disposition,
        "formal_occurrence_identity_collapse_credit": 0,
        "formal_component_edge_credit": 0,
        "formal_DSU_rank_reduction_credit": 0,
        "formal_maximality_credit": 0,
    }
    return closed(payload)


def build() -> tuple[dict[str, Any], dict[str, Any]]:
    for name in (R174P, R179P, R274P, R287P):
        need(file_sha256(HERE / name) == PINS[name], f"pin:{name}")
    regions = load_regions()
    source_document = read_gzip(R299A)
    need(
        source_document["row_count"] == 43_092
        and digest(source_document["rows"]) == source_document["rows_sha256"],
        "R299A source ledger",
    )
    source_rows = [
        row
        for row in source_document["rows"]
        if row["coordinate_face_physical_replay_status"].startswith(
            "OUTER_COORDINATE_COMMON_FACE_ONLY"
        )
    ]
    need(len(source_rows) == 26_264, "graph-constrained face census")
    rows = [replay_row(source, regions) for source in source_rows]
    rows.sort(key=lambda row: row["Round299B_signed_support_face_replay_row_id"])

    disposition = Counter(
        row["signed_support_face_disposition"] for row in rows
    )
    relation_state = Counter(
        (
            row["active_factor_relation"],
            row["precision_stable_signed_region_face_state"],
        )
        for row in rows
    )
    accepted_rows = [
        row for row in rows
        if row["signed_support_face_disposition"].startswith(
            "POSITIVE_AREA_SIGNED_SUPPORT_COMMON_FACE_CERTIFIED"
        )
    ]
    excluded_rows = [row for row in rows if row not in accepted_rows]
    accepted_pairs = {
        tuple(row["unordered_nonself_formal_occurrence_endpoint_pair"])
        for row in accepted_rows
        if row["unordered_nonself_formal_occurrence_endpoint_pair"] is not None
    }
    excluded_pairs = {
        tuple(row["unordered_nonself_formal_occurrence_endpoint_pair"])
        for row in excluded_rows
        if row["unordered_nonself_formal_occurrence_endpoint_pair"] is not None
    }
    full_pairs = {
        tuple(row["unordered_nonself_formal_occurrence_endpoint_pair"])
        for row in source_document["rows"]
        if row["coordinate_face_physical_replay_status"].startswith(
            "BOTH_ENDPOINT_CELLS_FULL"
        )
        and row["unordered_nonself_formal_occurrence_endpoint_pair"] is not None
    }
    combined_accepted_pairs = full_pairs | accepted_pairs

    lower_document = read_gzip(R295A)
    lower_pairs = {
        tuple(row["target_Round294_registry_occurrence_ids"])
        for row in lower_document["rows"]
        if row["target_Round294_registry_reference_count"] == 2
    }
    need(len(lower_pairs) == 111_524, "R295A lower pair census")

    need(
        disposition
        == {
            "POSITIVE_AREA_SIGNED_SUPPORT_COMMON_FACE_CERTIFIED__"
            "IDENTITY_VERSUS_COMPONENT_EDGE_SEMANTICS_PENDING": 13_120,
            "SIGNED_SUPPORT_FACE_EMPTY__NO_PHYSICAL_COMMON_FACE": 4_800,
            "NO_POSITIVE_AREA_SIGNED_SUPPORT_COMMON_FACE__"
            "COMMON_ZERO_SET_LOWER_FRONTIER_NOT_DECIDED_HERE": 8_344,
        },
        "signed replay disposition census",
    )
    need(
        relation_state
        == {
            (
                "ONE_GRAPH_ENDPOINT__OTHER_ENDPOINT_FULL_SIGNED_SUPPORT",
                "FULL_DESIRED_SIDE_SUPPORT",
            ): 4_788,
            (
                "ONE_GRAPH_ENDPOINT__OTHER_ENDPOINT_FULL_SIGNED_SUPPORT",
                "EMPTY_OPPOSITE_SIDE_COORDINATE_CELL",
            ): 4_788,
            (
                "SAME_ACTIVE_FACTOR__SAME_STRICT_DESIRED_SIDE",
                "CLIPPED_DESIRED_SIDE_SUPPORT",
            ): 8_320,
            (
                "SAME_ACTIVE_FACTOR__SAME_STRICT_DESIRED_SIDE",
                "FULL_DESIRED_SIDE_SUPPORT",
            ): 12,
            (
                "SAME_ACTIVE_FACTOR__SAME_STRICT_DESIRED_SIDE",
                "EMPTY_OPPOSITE_SIDE_COORDINATE_CELL",
            ): 12,
            (
                "SAME_ACTIVE_FACTOR__OPPOSITE_STRICT_DESIRED_SIDES",
                "NOT_APPLICABLE__EXACT_STRICT_SIDE_EXCLUSION",
            ): 8_344,
        },
        "factor relation/state census",
    )
    need(
        len(accepted_pairs) == 12_704
        and len(excluded_pairs) == 12_756
        and len(full_pairs) == 12_776
        and len(full_pairs & accepted_pairs) == 28
        and len(combined_accepted_pairs) == 25_452,
        "canonical pair census",
    )
    need(
        not accepted_pairs & lower_pairs
        and not excluded_pairs & lower_pairs,
        "R299B disjoint from R295A lower pair universe",
    )

    ledger = {
        "schema": LEDGER_SCHEMA,
        "status": "PASS_ZERO_CREDIT__SIGNED_SUPPORT_FACE_REPLAY_COMPLETE",
        "row_count": len(rows),
        "rows": rows,
        "rows_sha256": digest(rows),
        "row_ids_sha256": digest(
            [row["Round299B_signed_support_face_replay_row_id"] for row in rows]
        ),
        "row_hashes_sha256": digest([row["row_sha256"] for row in rows]),
        "every_row_closed_by_own_SHA256": True,
    }
    result = {
        "schema": SCHEMA,
        "status": "PASS_ZERO_CREDIT__GRAPH_CONSTRAINED_FACE_BOXES_RESOLVED",
        "input_file_pins": PINS,
        "runtime": {
            "python_flint_version": FLINT_VERSION,
            "arb_precision_bits": ctx.prec,
            "dyadic_sqrt_outer_enclosure_replay_bits": list(REPLAY_BITS),
        },
        "census": {
            "input_graph_constrained_coordinate_face_count": len(rows),
            "signed_support_face_disposition_histogram":
                dict(sorted(disposition.items())),
            "active_factor_relation_state_histogram": {
                "|".join(key): value for key, value in sorted(relation_state.items())
            },
            "accepted_graph_face_raw_count": len(accepted_rows),
            "accepted_graph_face_nonself_raw_count": sum(
                row["unordered_nonself_formal_occurrence_endpoint_pair"] is not None
                for row in accepted_rows
            ),
            "accepted_graph_face_distinct_nonself_pair_count":
                len(accepted_pairs),
            "excluded_graph_face_raw_count": len(excluded_rows),
            "excluded_graph_face_distinct_nonself_pair_count":
                len(excluded_pairs),
            "full_face_distinct_nonself_pair_count": len(full_pairs),
            "full_graph_accepted_pair_intersection_count":
                len(full_pairs & accepted_pairs),
            "combined_full_and_graph_accepted_distinct_pair_count":
                len(combined_accepted_pairs),
            "accepted_pair_R295A_lower_intersection_count":
                len(accepted_pairs & lower_pairs),
            "excluded_pair_R295A_lower_intersection_count":
                len(excluded_pairs & lower_pairs),
            "every_accepted_graph_face_has_strict_desired_side_witness":
                all(
                    row["strict_desired_side_face_witness"] is not None
                    for row in accepted_rows
                ),
            "four_pair_mixed_accept_reject_witness_rule":
                "EXISTS_ACCEPTED_FACE_WINS_FOR_EDGE_EXISTENCE;"
                "REJECTED_FACE_ROWS_REMAIN_AS_LOCAL_EXCLUSIONS",
        },
        "ledger": {
            "filename": LEDGER.name,
            "row_count": len(rows),
            "rows_sha256": ledger["rows_sha256"],
        },
        "strict_nonpromotion": {
            "formal_occurrence_identity_collapse_credit": 0,
            "formal_component_edge_credit": 0,
            "formal_DSU_rank_reduction_credit": 0,
            "formal_maximality_credit": 0,
            "CM2": "NO_GO_PENDING_SEMANTIC_PROMOTION_AND_GLOBAL_FRONTIER",
        },
    }
    # The exact count is asserted separately so an accepted witness cannot be
    # accidentally overwritten by another rejected face for the same pair.
    mixed_pairs = accepted_pairs & excluded_pairs
    need(len(mixed_pairs) == 4, "four mixed accept/reject endpoint pairs")
    result["census"]["distinct_pair_with_both_accept_and_reject_face_count"] = 4
    result["result_sha256"] = digest(result)
    return ledger, result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path, default=LEDGER)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    ledger, result = build()
    ledger_bytes = deterministic_gzip_bytes(ledger)
    result["ledger"]["file_sha256"] = hashlib.sha256(ledger_bytes).hexdigest()
    result["result_sha256"] = digest(
        {key: value for key, value in result.items() if key != "result_sha256"}
    )
    atomic(arguments.ledger, ledger_bytes)
    atomic(arguments.output, canonical(result) + b"\n")


if __name__ == "__main__":
    main()
