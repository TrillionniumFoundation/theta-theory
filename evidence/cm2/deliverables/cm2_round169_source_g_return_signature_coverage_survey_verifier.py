#!/usr/bin/env python3
"""Independent verifier for the Round169 source-G coverage survey.

The verifier does not import or execute the producer.  It independently
rebuilds the rational candidate reduction, all 441,280 immutable candidate
keys, the source-G atlas/return-key census, and the complete expected
certificate document.  Semantic mutations are re-signed before validation.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parent
CERTIFICATE = (
    ROOT
    / "cm2_round169_source_g_return_signature_coverage_survey_certificate.json"
)
OUTPUT = (
    ROOT
    / "cm2_round169_source_g_return_signature_coverage_survey_verification.json"
)
PRODUCER = ROOT / "cm2_round169_source_g_return_signature_coverage_survey.py"
SCHEMA = "cm2.round169.source-g-return-signature-coverage-survey.v1"
VERIFICATION_SCHEMA = (
    "cm2.round169.source-g-return-signature-coverage-survey.verification.v1"
)
STATUS = (
    "CERTIFIED_SOURCE_G_EXACT_KEY_COVERAGE_DEFICIT_SURVEY__"
    "NO_EXTERIOR_OR_D02_PROMOTION"
)

UPSTREAM_PINS = {
    "cm2_gate3_candidate_first_hit_cert.py":
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    "cm2-gate3-first-hit-atlas-manifest-2026-07-15.json":
        "0c820a5e3481b2c18fabb14d8d0fab7ce454f9a9e68b856bb2a7bf139404f7f4",
    "cm2_gate3_eight_cell_symmetry_atlas_cert.py":
        "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    "cm2-gate3-eight-cell-symmetry-atlas-manifest-2026-07-15.json":
        "f8fda665edbb7d8b39ce495188f90ecb2b5ec4384c1eb958949627df167c4987",
    "cm2_gate5_return_word_three_norm_frontier_cert.py":
        "ddcc250f8700c6a695f96019d9f7824fe98636e20a67685fdc6a3cce77f6d695",
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json":
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866",
    "cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-"
    "2026-07-24.json":
        "64e91e6b1efcb2675982fbc453b08349b003c8be5b4d236f61e1392aaee045f0",
    "cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-"
    "verification-2026-07-24.json":
        "57093537ae3f464e276da830ee5821ffbe3576278c71adbe111b22a128f3005f",
    "cm2_round162_compact_gate3_coordinate_bridge_certificate.json":
        "7a9889bd306567d8f68b203cab54e6fd821dd303f801e61bd82d9f32e012e4fe",
    "cm2_round162_compact_gate3_coordinate_bridge_verification.json":
        "99b443650b5f74c508e25d982aa09b06632432bd9dd880f1364c69ff7afa1583",
    "cm2_round163_outgoing_chart_pruning_certificate.json":
        "90d3313004be90049efb116a44731aef2554056661ce83b85afafdf3e3738539",
    "cm2_round163_outgoing_chart_pruning_verification.json":
        "28ab965bffb0ab04d4fd839f1f7f895dbbab3a8e5be250a17fa95b7a8cc825d6",
    "cm2_round164_tangency_strata_pruning_certificate.json":
        "2f1fcb72224f39c8d4a9d9f666a8579f71d77542e31552aa7c9dbc4b7338f092",
    "cm2_round164_tangency_strata_pruning_verification.json":
        "850bd24ae60979aaaea3f6819dcab665a1f7228d0c104014bfe8cce9e91299b0",
}
EXPECTED_PRODUCER_SHA256 = (
    "2be6580fb7d3d47a7ddab05f22d7987ba28d531bb1dd5af5c0082b458e089ee9"
)
SOURCE_CHARTS = tuple(
    f"{source}:{cell}"
    for source in ("G", "W")
    for cell in ("E", "W", "N", "S")
)
G_CHARTS = ("G:E", "G:W", "G:N", "G:S")
Q = Fraction
R = {"G": Q(9, 25), "W": Q(4, 25)}
EPS = Q(1, 400)
TAU = Q(3)
LOW = Q(707, 1000)
HIGH = Q(708, 1000)


def canonical(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def fail_unless(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def decode_strict_bytes(raw: bytes) -> dict[str, Any]:
    fail_unless(
        not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        "encoding",
    )

    def duplicate_guard(
        pairs: list[tuple[str, Any]]
    ) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            fail_unless(key not in result, "duplicate key")
            result[key] = value
        return result

    def reject_number(token: str) -> None:
        raise ValueError(token)

    value = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=duplicate_guard,
        parse_constant=reject_number,
        parse_float=reject_number,
    )

    def walk(item: Any) -> None:
        if type(item) is str:
            fail_unless(
                "\x00" not in item
                and not any(
                    0xD800 <= ord(character) <= 0xDFFF
                    for character in item
                ),
                "decoded string",
            )
        elif type(item) is list:
            for child in item:
                walk(child)
        elif type(item) is dict:
            for key, child in item.items():
                walk(key)
                walk(child)

    walk(value)
    fail_unless(type(value) is dict, "top object")
    return value


def load(path: Path) -> dict[str, Any]:
    return decode_strict_bytes(path.read_bytes())


def wrapped(
    document: dict[str, Any],
    schema: str,
    result_digest: str,
) -> dict[str, Any]:
    fail_unless(
        set(document) == {"schema", "result", "result_sha256"},
        f"wrapper:{schema}",
    )
    fail_unless(document["schema"] == schema, f"schema:{schema}")
    fail_unless(
        document["result_sha256"] == result_digest
        == digest(document["result"]),
        f"digest:{schema}",
    )
    return document["result"]


def load_upstream() -> dict[str, dict[str, Any]]:
    for name, expected in UPSTREAM_PINS.items():
        fail_unless(
            hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected,
            f"pin:{name}",
        )
    names = [name for name in UPSTREAM_PINS if name.endswith(".json")]
    docs = {name: load(ROOT / name) for name in names}
    r139 = wrapped(
        docs[
            "cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-"
            "2026-07-24.json"
        ],
        "cm2.round139.rank3-minus-d0-adjacent-h1-collar-return-frontier.v1",
        "6e8f54c34154ea5ba3c95d4e901bc643c020a0a42e180241ae9053bb24f42236",
    )
    r139v = wrapped(
        docs[
            "cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-"
            "verification-2026-07-24.json"
        ],
        "cm2.round139.rank3-minus-d0-adjacent-h1-collar-return-frontier-verification.v1",
        "e96609b3ff1ba35c94e224c5d16897ed6d173fe69cc3cbf260ff85e5340165e1",
    )
    bridge = wrapped(
        docs["cm2_round162_compact_gate3_coordinate_bridge_certificate.json"],
        "cm2.round162.compact-gate3-coordinate-bridge.v1",
        "5a327f96ecc8183af76695123dcf6fc4ccbf443e4bd7427cef38090c06bcfe86",
    )
    bridge_v = wrapped(
        docs["cm2_round162_compact_gate3_coordinate_bridge_verification.json"],
        "cm2.round162.compact-gate3-coordinate-bridge.verification.v1",
        "3d74d45804c8cef12782eeda57e7f770e6d8b9f962f97d1f28c54c92b27c6421",
    )
    r163 = wrapped(
        docs["cm2_round163_outgoing_chart_pruning_certificate.json"],
        "cm2.round163.outgoing-chart-pruning.v1",
        "d64b5fab6b599a8fb4d6665c8abb902d79f86afd0370610845a5f7558d848102",
    )
    r163v = wrapped(
        docs["cm2_round163_outgoing_chart_pruning_verification.json"],
        "cm2.round163.outgoing-chart-pruning.verification.v1",
        "183b30155016229f27ba35293ad98d4b1b779af19c84dab5fec583862c8ef8a9",
    )
    r164 = wrapped(
        docs["cm2_round164_tangency_strata_pruning_certificate.json"],
        "cm2.round164.dimension-safe-tangency-graph-typing.v2",
        "0f6d7f47ac20734ed294dd04cd7720ccbb9c0a1d4236980f814dd2ea2d5e79d9",
    )
    r164v = wrapped(
        docs["cm2_round164_tangency_strata_pruning_verification.json"],
        "cm2.round164.dimension-safe-tangency-graph-typing.verification.v2",
        "bb2e51bdbbd457a5782038efc527000cbf89b73c8645fd6facd126fa453af8c4",
    )
    fail_unless(
        r139["status"]
        == "CERTIFIED_MINUS_D0_ADJACENT_H1_COLLAR_STRICT_FIRST_RETURN"
        and r139v["status"] == "PASS"
        and r139v["certificate_result_sha256"]
        == "6e8f54c34154ea5ba3c95d4e901bc643c020a0a42e180241ae9053bb24f42236"
        and bridge["scope"]["source_obstacle"] == "W"
        and bridge["scope"]["does_not_exhaust_return_signatures"] is True
        and bridge_v["status"] == "PASS"
        and r163v["status"] == "PASS"
        and r164v["status"] == "PASS"
        and r164v["full_document_exactly_matched"] is True,
        "upstream verification chain",
    )
    docs["_r139"] = r139
    docs["_bridge"] = bridge
    docs["_r163"] = r163
    docs["_r164"] = r164
    return docs


TARGETS = tuple(
    (obstacle, ix, iy)
    for obstacle in ("G", "W")
    for ix in range(-4, 5)
    for iy in range(-4, 5)
)


def target_label(target: tuple[str, int, int]) -> str:
    return f"{target[0]}[{target[1]},{target[2]}]"


def min_sq(lower: Q, upper: Q) -> Q:
    if lower <= 0 <= upper:
        return Q(0)
    return min(lower * lower, upper * upper)


def displacement(
    source: str, target: tuple[str, int, int]
) -> tuple[Q, Q, Q, Q]:
    obstacle, ix, iy = target
    if source == obstacle:
        return Q(ix), Q(ix), Q(iy), Q(iy)
    if source == "G":
        x = Q(2 * ix + 1, 2)
        y = Q(2 * iy + 1, 2)
        return x - EPS, x + EPS, y, y
    x = Q(2 * ix - 1, 2)
    y = Q(2 * iy - 1, 2)
    return x - EPS, x + EPS, y, y


def support(cell: str, box: tuple[Q, Q, Q, Q]) -> Q:
    x0, x1, y0, y1 = box
    if cell == "E":
        axial, lateral = x1, max(abs(y0), abs(y1))
    elif cell == "W":
        axial, lateral = -x0, max(abs(y0), abs(y1))
    elif cell == "N":
        axial, lateral = y1, max(abs(x0), abs(x1))
    elif cell == "S":
        axial, lateral = -y0, max(abs(x0), abs(x1))
    else:
        raise ValueError(cell)
    return (
        axial + lateral * HIGH
        if axial >= 0
        else axial * LOW + lateral * HIGH
    )


def retained(chart: str, target: tuple[str, int, int]) -> bool:
    source, cell = chart.split(":")
    obstacle, ix, iy = target
    if source == obstacle and ix == 0 and iy == 0:
        return False
    box = displacement(source, target)
    if min_sq(box[0], box[1]) + min_sq(box[2], box[3]) >= (
        TAU + R[source] + R[obstacle]
    ) ** 2:
        return False
    return support(cell, box) >= R[source] - R[obstacle]


def candidate_list(chart: str) -> tuple[str, ...]:
    return tuple(
        target_label(target) for target in TARGETS if retained(chart, target)
    )


def patterns() -> tuple[tuple[str, ...], ...]:
    rows: list[tuple[str, ...]] = []
    for x_count, y_count in itertools.product(range(5), repeat=2):
        length = x_count + y_count
        x_signs = (0,) if x_count == 0 else (-1, 1)
        y_signs = (0,) if y_count == 0 else (-1, 1)
        for x_sign, y_sign in itertools.product(x_signs, y_signs):
            for x_places in itertools.combinations(range(length), x_count):
                x_set = frozenset(x_places)
                rows.append(tuple(
                    ("X+" if x_sign > 0 else "X-")
                    if position in x_set
                    else ("Y+" if y_sign > 0 else "Y-")
                    for position in range(length)
                ))
    return tuple(rows)


def streamed(rows: Iterable[Any]) -> tuple[int, str]:
    hasher = hashlib.sha256()
    count = 0
    for row in rows:
        hasher.update(canonical(row).encode("utf-8") + b"\n")
        count += 1
    return count, hasher.hexdigest()


def key_tables() -> dict[str, Any]:
    pats = patterns()
    fail_unless(
        len(pats) == len(set(pats)) == 985
        and Counter(map(len, pats))
        == Counter({0: 1, 1: 4, 2: 12, 3: 28, 4: 60,
                    5: 120, 6: 200, 7: 280, 8: 280}),
        "independent patterns",
    )
    pairs = tuple(
        (chart, target)
        for chart in SOURCE_CHARTS
        for target in candidate_list(chart)
    )
    fail_unless(len(pairs) == len(set(pairs)) == 448, "independent pairs")
    pair_index = {pair: i for i, pair in enumerate(pairs)}
    pattern_index = {pattern: i for i, pattern in enumerate(pats)}
    count, row_hash = streamed(
        [chart, target, list(pattern), len(pattern) + 1]
        for chart, target in pairs
        for pattern in pats
    )
    fail_unless(count == 441280, "independent keys")
    return {
        "patterns": pats,
        "pairs": pairs,
        "pair_index": pair_index,
        "pattern_index": pattern_index,
        "pair_hash": digest(pairs),
        "row_hash": row_hash,
    }


def verify_key(
    key: dict[str, Any], tables: dict[str, Any]
) -> tuple[int, list[Any]]:
    fail_unless(
        set(key) == {
            "official_word_key_id",
            "ordinal_zero_based",
            "registry_row",
            "registry_row_sha256",
        },
        "official fields",
    )
    row = key["registry_row"]
    fail_unless(
        type(row) is list and len(row) == 4
        and type(row[0]) is str and type(row[1]) is str
        and type(row[2]) is list and type(row[3]) is int,
        "official row",
    )
    pattern = tuple(row[2])
    pair = (row[0], row[1])
    fail_unless(
        pair in tables["pair_index"]
        and pattern in tables["pattern_index"]
        and row[3] == len(pattern) + 1,
        "official membership",
    )
    ordinal = (
        tables["pair_index"][pair] * 985
        + tables["pattern_index"][pattern]
    )
    row_hash = digest(row)
    fail_unless(
        key["ordinal_zero_based"] == ordinal
        and key["registry_row_sha256"] == row_hash
        and key["official_word_key_id"]
        == f"gate5-word:{ordinal:06d}:{row_hash}",
        "official identifier",
    )
    return ordinal, row


def histogram(counter: Counter[int]) -> dict[str, int]:
    return {str(key): counter[key] for key in sorted(counter)}


def expected_document() -> dict[str, Any]:
    docs = load_upstream()
    first = docs["cm2-gate3-first-hit-atlas-manifest-2026-07-15.json"]
    atlas = docs["cm2-gate3-eight-cell-symmetry-atlas-manifest-2026-07-15.json"]
    words = docs[
        "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
    ]
    r139 = docs["_r139"]
    bridge = docs["_bridge"]
    r163 = docs["_r163"]
    r164 = docs["_r164"]
    tables = key_tables()

    fail_unless(
        first["candidate_reduction"]["chart_target_pair_count"] == 1296
        and first["candidate_reduction"]["retained_pair_count"] == 448
        and first["candidate_reduction"]["certified_empty_pair_count"] == 848,
        "first hit",
    )
    registry = words["result"]["immutable_candidate_key_registry"]
    fail_unless(
        tables["pair_hash"] == registry["chart_target_pair_rows_sha256"]
        and tables["row_hash"] == registry["candidate_word_key_rows_sha256"]
        and registry["candidate_return_word_key_count"] == 441280,
        "Gate5 replay",
    )
    fail_unless(
        digest(r139["collision_rows"]) == r139["collision_rows_sha256"]
        and digest(r139["positive_area_collision_rows"])
        == r139["positive_area_collision_rows_sha256"]
        and len(r139["collision_rows"])
        == len(r139["positive_area_collision_rows"]) == 1648,
        "Round139 row digests",
    )
    graph_keys = [
        verify_key(row["official_word_key"], tables)
        for row in r139["collision_rows"]
    ]
    positive_keys = [
        verify_key(row["official_word_key"], tables)
        for row in r139["positive_area_collision_rows"]
    ]
    fail_unless(
        [row[0] for row in graph_keys] == [row[0] for row in positive_keys],
        "positive key sequence",
    )
    occurrences = [
        item for item in positive_keys if item[1][0] in G_CHARTS
    ]
    unique_map = {ordinal: row for ordinal, row in occurrences}
    unique_rows = [unique_map[key] for key in sorted(unique_map)]
    fail_unless(
        len(occurrences) == 1143 and len(unique_rows) == 103,
        "witness counts",
    )

    pats = tables["patterns"]
    roof_per_pair = Counter(len(pattern) + 1 for pattern in pats)
    chart_rows: list[dict[str, Any]] = []
    total = Counter()
    for chart in G_CHARTS:
        candidates = candidate_list(chart)
        fail_unless(len(candidates) == 57, f"57:{chart}")
        atlas_row = atlas["charts"][chart]
        chart_pairs = [(chart, target) for target in candidates]
        key_count, key_hash = streamed(
            [chart, target, list(pattern), len(pattern) + 1]
            for target in candidates for pattern in pats
        )
        chart_occurrences = [
            item for item in occurrences if item[1][0] == chart
        ]
        chart_unique_map = {
            ordinal: row for ordinal, row in chart_occurrences
        }
        chart_unique = [
            chart_unique_map[key] for key in sorted(chart_unique_map)
        ]
        candidate_roof = Counter({
            roof: 57 * count for roof, count in roof_per_pair.items()
        })
        witness_roof = Counter(row[3] for row in chart_unique)
        missing_roof = Counter({
            roof: candidate_roof[roof] - witness_roof[roof]
            for roof in candidate_roof
        })
        counts = atlas_row["counts"]
        fail_unless(
            atlas_row["leaf_count"] == sum(counts.values()),
            f"atlas conservation:{chart}",
        )
        total.update(counts)
        total["leaf_count"] += atlas_row["leaf_count"]
        first_ordinal = tables["pair_index"][chart_pairs[0]] * 985
        last_ordinal = (tables["pair_index"][chart_pairs[-1]] + 1) * 985 - 1
        chart_rows.append({
            "source_chart": chart,
            "atlas_provenance": atlas_row["provenance"],
            "candidate_target_count": 57,
            "candidate_target_ids_sha256": digest(candidates),
            "candidate_chart_target_pair_count": 57,
            "candidate_chart_target_pairs_sha256": digest(chart_pairs),
            "candidate_exact_key_count": key_count,
            "candidate_exact_key_stream_sha256": key_hash,
            "candidate_exact_key_ordinal_interval_inclusive":
                [first_ordinal, last_ordinal],
            "candidate_exact_key_roof_histogram": histogram(candidate_roof),
            "atlas_leaf_count": atlas_row["leaf_count"],
            "atlas_unique_first_leaf_count": counts["unique_first"],
            "atlas_tangency_graph_leaf_count": counts["tangency_graph"],
            "atlas_multi_candidate_leaf_count": counts["multi_candidate"],
            "atlas_pair_unresolved_count":
                atlas_row["pair_rows"]["unresolved"],
            "atlas_triple_unresolved_count":
                atlas_row["triple_rows"]["unresolved"],
            "atlas_leaf_rows_sha256": atlas_row["leaf_rows_sha256"],
            "round139_positive_area_local_witness_occurrence_count":
                len(chart_occurrences),
            "round139_positive_area_local_witness_exact_key_count":
                len(chart_unique),
            "round139_positive_area_local_witness_target_pair_count":
                len({(row[0], row[1]) for row in chart_unique}),
            "round139_positive_area_local_witness_exact_key_rows_sha256":
                digest(chart_unique),
            "round139_positive_area_local_witness_roof_histogram":
                histogram(witness_roof),
            "candidate_keys_without_a_Round139_local_witness_count":
                key_count - len(chart_unique),
            "candidate_keys_without_a_Round139_local_witness_roof_histogram":
                histogram(missing_roof),
            "globally_dispositioned_exact_key_count": 0,
            "keys_without_a_global_geometric_disposition_count": key_count,
        })
    fail_unless(
        total == Counter({
            "leaf_count": 66420,
            "unique_first": 21232,
            "tangency_graph": 160,
            "multi_candidate": 45028,
        }),
        "atlas totals",
    )
    witness_pairs = {(row[0], row[1]) for row in unique_rows}
    witness_roof = Counter(row[3] for row in unique_rows)
    fail_unless(
        len(witness_pairs) == 52
        and witness_roof == Counter({1: 28, 2: 56, 3: 17, 4: 2}),
        "witness histogram",
    )
    ambient = r164["ambient_frozen_prefix_census"]
    fail_unless(
        r163["frozen_prefix"] == {
            "collision_index": 1,
            "required_owner": "W[1,0]",
            "required_outgoing_chart": "W",
        }
        and ambient["combined_recordwise_excluded_ambient_leaf_count"] == 37480
        and ambient["remaining_ambient_unresolved_leaf_count"] == 39348
        and ambient["new_full_dimensional_ambient_leaf_exclusion_count"] == 0,
        "dimension-safe W baseline",
    )

    result = {
        "status": STATUS,
        "scope": {
            "object":
                "source-G exact candidate return-signature coverage census",
            "source_charts": list(G_CHARTS),
            "parameter_window": "|s|<=1/400",
            "candidate_key":
                "(source normal chart, retained target lift, "
                "monotone clean-wall record, roof)",
            "survey_only": True,
            "adds_no_leaf_or_exact_key_exclusion": True,
            "adds_no_connected_or_cemetery_disposition": True,
        },
        "provenance": {
            "dependency_sha256": UPSTREAM_PINS,
            "exact_rational_candidate_reduction_rebuilt": True,
            "all_441280_candidate_key_rows_rebuilt": True,
            "all_1648_Round139_graph_and_positive_area_key_bindings_checked":
                True,
            "source_W_exclusions_transported_to_source_G": False,
            "reflected_return_signatures_inferred_without_a_transport": False,
            "old_artifacts_modified": False,
        },
        "source_W_37480_39348_chain_architecture_audit": {
            "candidate_reducer":
                "exact horizon plus outgoing-halfspace necessary-condition "
                "filter over 162 target lifts",
            "atlas":
                "direct 192-bit Arb on G:E,G:N,W:E,W:N plus exact Jx/Jy "
                "reflections; adaptive depth 8",
            "frozen_prefix_source":
                "Round139 collision 1 on one local R1648 cylinder",
            "frozen_prefix": r163["frozen_prefix"],
            "pruning_stack": [
                "Round162 exact W:W candidate absence and unique-owner mismatch",
                "Round163 strict outgoing-chart mismatch",
                "Round164-v2 codimension-one tangency graph typing with zero "
                "whole-leaf credit",
            ],
            "verifier_architecture": {
                "Round163":
                    "independent atlas replay; producer neither imported nor "
                    "executed",
                "Round164_v2":
                    "full expected-document equality, 36 re-signed semantic "
                    "mutations, strict JSON attacks, live off-graph regressions",
            },
            "dimension_safe_current_baseline": {
                "source_W_chart_leaf_records": 76828,
                "recordwise_excluded_ambient_leaf_count": 37480,
                "remaining_ambient_unresolved_leaf_count": 39348,
                "remaining_prefix_stage_one_match": 518,
                "remaining_outgoing_chart_seam_unresolved": 618,
                "remaining_tangency_ambient_leaf_bulk": 32,
                "remaining_multi_candidate": 38180,
            },
            "one_prefix_only": True,
            "does_not_remove_a_leaf_from_other_return_signature_searches":
                True,
            "does_not_supply_source_G_credit": True,
        },
        "source_G_existing_inputs": {
            "candidate_target_count_per_chart": 57,
            "candidate_chart_target_pair_count": 228,
            "crossing_pattern_count_per_pair": 985,
            "candidate_exact_key_count": 224580,
            "atlas_leaf_count": total["leaf_count"],
            "atlas_unique_first_leaf_count": total["unique_first"],
            "atlas_tangency_graph_leaf_count": total["tangency_graph"],
            "atlas_multi_candidate_leaf_count": total["multi_candidate"],
            "direct_atlas_charts": ["G:E", "G:N"],
            "exact_reflected_atlas_charts": ["G:W", "G:S"],
            "reflection_transports_leaf_and_target_rows": True,
            "reflection_transports_signed_wall_word_exact_keys": False,
            "reflection_transports_outgoing_chart_signature": False,
            "Round162_compact_to_Gate3_bridge_source_obstacle":
                bridge["scope"]["source_obstacle"],
            "source_G_compact_to_Gate3_bridge_present": False,
        },
        "source_G_exact_key_coverage_census": {
            "chart_rows": chart_rows,
            "chart_rows_sha256": digest(chart_rows),
            "candidate_chart_target_pair_count": 228,
            "candidate_exact_key_envelope_count": 224580,
            "candidate_exact_key_envelope_fraction": "224580/224580",
            "Round139_positive_area_local_witness_occurrence_count":
                len(occurrences),
            "Round139_positive_area_local_witness_exact_key_count":
                len(unique_rows),
            "Round139_positive_area_local_witness_exact_key_rows_sha256":
                digest(unique_rows),
            "Round139_positive_area_local_witness_chart_target_pair_count":
                len(witness_pairs),
            "Round139_positive_area_local_witness_roof_histogram":
                histogram(witness_roof),
            "Round139_positive_area_local_witness_fraction": "103/224580",
            "candidate_keys_without_a_Round139_local_witness_count": 224477,
            "global_geometric_exact_key_disposition_count": 0,
            "global_geometric_exact_key_disposition_fraction": "0/224580",
            "keys_without_a_global_geometric_disposition_count": 224580,
            "why_local_witnesses_are_not_global_dispositions":
                "the 103 keys occur along one certified positive-area local "
                "R1648 cylinder; they do not partition or exhaust any complete "
                "source-G chart-key domain",
        },
        "missing_certified_interfaces": [
            {
                "priority": 1,
                "interface": "source-G compact-to-Gate3 coordinate bridge",
                "current_state":
                    "the pinned Round162 bridge has source_obstacle=W only",
                "required_output":
                    "four source-G chart maps, seams and p=+-1 grazing faces "
                    "bound to the pinned Gate3 leaf cover",
            },
            {
                "priority": 2,
                "interface":
                    "exact signed wall-word and outgoing-chart materialization",
                "current_state":
                    "Gate3 leaves carry first-owner classes but no joined "
                    "clean-wall return key or outgoing chart disposition",
                "required_output":
                    "dimension-safe leaf/subleaf rows keyed by the immutable "
                    "Gate5 ordinal",
            },
            {
                "priority": 3,
                "interface": "source-G multi-candidate refinement",
                "current_state": "45028 ambient leaf records remain multi-candidate",
                "required_output":
                    "exact earliest-root exclusions or typed root-order event "
                    "strata without dropping codimension-one sheets",
            },
            {
                "priority": 4,
                "interface":
                    "source-G tangency/grazing/seam/corner ledger",
                "current_state":
                    "160 tangency graphs plus source grazing, chart seams and "
                    "simultaneous wall corners lack a complete exact-key join",
                "required_output":
                    "separate ambient and lower-dimensional ledgers with unique "
                    "half-open ownership and cemetery traces",
            },
            {
                "priority": 5,
                "interface":
                    "global per-key empty/nonempty/connected/excluded/cemetery "
                    "decision",
                "current_state": "0/224580 source-G keys globally dispositioned",
                "required_output":
                    "all 224580 keys accounted with zero unresolved rows",
            },
        ],
        "shortest_reproducible_extension_strategy": {
            "stage_1":
                "certify the source-G compact bridge and the Jx/Jy signed "
                "wall-word/outgoing-chart key transforms",
            "stage_2":
                "on the 21232 unique-first leaves, isolate wall crossing order "
                "and outgoing chart, splitting only at exact event surfaces",
            "stage_3":
                "reuse the cached active-target refinement architecture on "
                "the 45028 multi-candidate leaves",
            "stage_4":
                "type the 160 tangency graphs and every grazing/seam/corner "
                "stratum in a dimension-safe ledger",
            "stage_5":
                "aggregate by immutable key ordinal and require exact "
                "conservation plus zero unresolved before any exterior claim",
            "naive_cross_product_to_avoid":
                "66420 atlas leaves times 224580 keys",
        },
        "strict_nonpromotion": {
            "source_G_global_exact_key_dispositions_complete": False,
            "all_return_signatures_excluded_or_connected": False,
            "all_disconnected_exterior_sheets_excluded": False,
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate":
            "materialize a certified source-G compact/key bridge, then attach "
            "owner, wall word and outgoing chart to the 21232 unique-first "
            "leaf records before refining 45028 multi-candidate records and "
            "typing 160 tangency graphs plus grazing/seam/corner strata",
    }
    return {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def validate(
    document: dict[str, Any],
    expected: dict[str, Any] | None = None,
) -> None:
    if expected is None:
        expected = expected_document()
    fail_unless(document == expected, "full expected document equality")


def semantic_attacks(expected: dict[str, Any]) -> list[tuple[str, Any]]:
    attacks: list[tuple[str, Any]] = []

    def add(label: str, mutation: Any) -> None:
        candidate = copy.deepcopy(expected)
        mutation(candidate["result"])
        candidate["result_sha256"] = digest(candidate["result"])
        attacks.append((label, candidate))

    add("status", lambda r: r.__setitem__("status", "CERTIFIED_D02"))
    add(
        "source G key count",
        lambda r: r["source_G_existing_inputs"].__setitem__(
            "candidate_exact_key_count", 224579
        ),
    )
    add(
        "local witnesses",
        lambda r: r["source_G_exact_key_coverage_census"].__setitem__(
            "Round139_positive_area_local_witness_exact_key_count", 104
        ),
    )
    add(
        "global disposition promotion",
        lambda r: r["source_G_exact_key_coverage_census"].__setitem__(
            "global_geometric_exact_key_disposition_count", 1
        ),
    )
    add(
        "chart witness count",
        lambda r: r["source_G_exact_key_coverage_census"]["chart_rows"][0]
        .__setitem__("round139_positive_area_local_witness_exact_key_count", 26),
    )
    add(
        "chart key digest",
        lambda r: r["source_G_exact_key_coverage_census"]["chart_rows"][0]
        .__setitem__("candidate_exact_key_stream_sha256", "0" * 64),
    )
    add(
        "atlas leaves",
        lambda r: r["source_G_existing_inputs"].__setitem__(
            "atlas_leaf_count", 66419
        ),
    )
    add(
        "multi count",
        lambda r: r["source_G_existing_inputs"].__setitem__(
            "atlas_multi_candidate_leaf_count", 45027
        ),
    )
    add(
        "reflection transport",
        lambda r: r["source_G_existing_inputs"].__setitem__(
            "reflection_transports_signed_wall_word_exact_keys", True
        ),
    )
    add(
        "source G bridge",
        lambda r: r["source_G_existing_inputs"].__setitem__(
            "source_G_compact_to_Gate3_bridge_present", True
        ),
    )
    add(
        "W baseline",
        lambda r: r["source_W_37480_39348_chain_architecture_audit"]
        ["dimension_safe_current_baseline"].__setitem__(
            "remaining_ambient_unresolved_leaf_count", 39336
        ),
    )
    add(
        "whole tangency credit",
        lambda r: r["source_W_37480_39348_chain_architecture_audit"]
        ["dimension_safe_current_baseline"].__setitem__(
            "recordwise_excluded_ambient_leaf_count", 37492
        ),
    )
    add(
        "dependency pin",
        lambda r: r["provenance"]["dependency_sha256"].__setitem__(
            "cm2_round164_tangency_strata_pruning_certificate.json", "f" * 64
        ),
    )
    add(
        "survey scope",
        lambda r: r["scope"].__setitem__("survey_only", False),
    )
    add(
        "add exclusion",
        lambda r: r["scope"].__setitem__(
            "adds_no_leaf_or_exact_key_exclusion", False
        ),
    )
    add(
        "drop blocker",
        lambda r: r["missing_certified_interfaces"].pop(),
    )
    add(
        "D02",
        lambda r: r["strict_nonpromotion"].__setitem__("D02", "CERTIFIED"),
    )
    add(
        "Gate5",
        lambda r: r["strict_nonpromotion"].__setitem__(
            "global_Gate5_fields", "18/18"
        ),
    )
    add(
        "CM2",
        lambda r: r["strict_nonpromotion"].__setitem__(
            "CM2", "CERTIFIED"
        ),
    )
    add("extra result key", lambda r: r.__setitem__("forged", True))
    return attacks


def strict_attacks(expected: dict[str, Any]) -> list[tuple[str, bytes]]:
    raw = canonical(expected).encode("utf-8")
    duplicate = raw.replace(
        b'{"result":',
        b'{"schema":"duplicate","result":',
        1,
    )
    return [
        ("duplicate key", duplicate),
        ("floating number", b'{"x":1.5}'),
        ("NaN", b'{"x":NaN}'),
        ("BOM", b"\xef\xbb\xbf" + raw),
        ("NUL", b'{"x":"\\u0000"}'),
        ("top array", b"[]"),
        ("trailing document", raw + b"{}"),
    ]


def build_verification(
    certificate: dict[str, Any],
) -> dict[str, Any]:
    expected = expected_document()
    validate(certificate, expected)
    rejected: list[str] = []
    for label, attack in semantic_attacks(expected):
        try:
            validate(attack, expected)
        except Exception:
            rejected.append(label)
    fail_unless(len(rejected) == 20, "semantic attack suite")
    strict_rejected: list[str] = []
    for label, raw in strict_attacks(expected):
        try:
            candidate = decode_strict_bytes(raw)
            validate(candidate, expected)
        except Exception:
            strict_rejected.append(label)
    fail_unless(len(strict_rejected) == 7, "strict attack suite")
    result = {
        "status": "PASS",
        "certificate_schema": SCHEMA,
        "certificate_result_sha256": certificate["result_sha256"],
        "certificate_sha256":
            hashlib.sha256(CERTIFICATE.read_bytes()).hexdigest(),
        "producer_sha256": hashlib.sha256(PRODUCER.read_bytes()).hexdigest(),
        "producer_imported_or_executed": False,
        "all_162_target_classifications_per_chart_independently_rebuilt": True,
        "all_448_chart_target_pairs_independently_rebuilt": True,
        "all_441280_candidate_exact_keys_independently_rebuilt": True,
        "all_1648_Round139_key_rows_per_copy_independently_checked": True,
        "source_G_66420_leaf_aggregate_recomputed": True,
        "source_G_224580_exact_key_deficit_census_recomputed": True,
        "Round164_v2_dimension_safe_37480_39348_baseline_rechecked": True,
        "full_document_exactly_matched": True,
        "semantic_attack_suite": {
            "all_result_mutations_resigned": True,
            "attack_count": len(rejected),
            "rejected_count": len(rejected),
            "rejected_attack_names": rejected,
        },
        "strict_json_attack_suite": {
            "attack_count": len(strict_rejected),
            "rejected_count": len(strict_rejected),
            "all_rejected": True,
            "rejected_attack_names": strict_rejected,
        },
        "strict_nonpromotion_recomputed": True,
    }
    fail_unless(
        result["producer_sha256"] == EXPECTED_PRODUCER_SHA256,
        "producer pin",
    )
    return {
        "schema": VERIFICATION_SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def main() -> int:
    global CERTIFICATE
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    CERTIFICATE = arguments.certificate.resolve()
    certificate = load(CERTIFICATE)
    verification = build_verification(certificate)
    arguments.output.write_text(
        json.dumps(
            verification,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n",
        encoding="utf-8",
    )
    print("PASS")
    print(f"WROTE {arguments.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
