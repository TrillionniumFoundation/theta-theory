#!/usr/bin/env python3
"""Round169: fail-closed source-G return-signature coverage survey.

This is an exact-key audit, not an exterior-pruning certificate.  It
independently rebuilds the finite Gate-5 candidate-key grammar from the
exact rational Gate-3 target reduction, cross-checks the pinned source-G
Gate-3 atlas census, and inventories the exact keys that occur on the one
positive-area Round139 R1648 cylinder.

The important distinction is between:

* a syntactically complete candidate-key envelope;
* a local positive-area witness for one key; and
* a global geometric disposition of that key on the complete source chart.

Only the first item and a small set of local witnesses are presently
certified.  No source-W exclusion is transported to source-G, no reflected
wall word is inferred without a certified key transport, and no Gate/D02
credit is added.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
OUTPUT = (
    HERE
    / "cm2_round169_source_g_return_signature_coverage_survey_certificate.json"
)
SCHEMA = "cm2.round169.source-g-return-signature-coverage-survey.v1"
STATUS = (
    "CERTIFIED_SOURCE_G_EXACT_KEY_COVERAGE_DEFICIT_SURVEY__"
    "NO_EXTERIOR_OR_D02_PROMOTION"
)

FIRST_HIT_SOURCE = "cm2_gate3_candidate_first_hit_cert.py"
FIRST_HIT_MANIFEST = "cm2-gate3-first-hit-atlas-manifest-2026-07-15.json"
ATLAS_SOURCE = "cm2_gate3_eight_cell_symmetry_atlas_cert.py"
ATLAS_MANIFEST = "cm2-gate3-eight-cell-symmetry-atlas-manifest-2026-07-15.json"
KEY_SOURCE = "cm2_gate5_return_word_three_norm_frontier_cert.py"
KEY_MANIFEST = "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
ROUND139_CERTIFICATE = (
    "cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-"
    "2026-07-24.json"
)
ROUND139_VERIFICATION = (
    "cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-"
    "verification-2026-07-24.json"
)
ROUND162_BRIDGE = "cm2_round162_compact_gate3_coordinate_bridge_certificate.json"
ROUND162_BRIDGE_VERIFICATION = (
    "cm2_round162_compact_gate3_coordinate_bridge_verification.json"
)
ROUND163_CERTIFICATE = "cm2_round163_outgoing_chart_pruning_certificate.json"
ROUND163_VERIFICATION = "cm2_round163_outgoing_chart_pruning_verification.json"
ROUND164_CERTIFICATE = "cm2_round164_tangency_strata_pruning_certificate.json"
ROUND164_VERIFICATION = "cm2_round164_tangency_strata_pruning_verification.json"

PINS = {
    FIRST_HIT_SOURCE:
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    FIRST_HIT_MANIFEST:
        "0c820a5e3481b2c18fabb14d8d0fab7ce454f9a9e68b856bb2a7bf139404f7f4",
    ATLAS_SOURCE:
        "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    ATLAS_MANIFEST:
        "f8fda665edbb7d8b39ce495188f90ecb2b5ec4384c1eb958949627df167c4987",
    KEY_SOURCE:
        "ddcc250f8700c6a695f96019d9f7824fe98636e20a67685fdc6a3cce77f6d695",
    KEY_MANIFEST:
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866",
    ROUND139_CERTIFICATE:
        "64e91e6b1efcb2675982fbc453b08349b003c8be5b4d236f61e1392aaee045f0",
    ROUND139_VERIFICATION:
        "57093537ae3f464e276da830ee5821ffbe3576278c71adbe111b22a128f3005f",
    ROUND162_BRIDGE:
        "7a9889bd306567d8f68b203cab54e6fd821dd303f801e61bd82d9f32e012e4fe",
    ROUND162_BRIDGE_VERIFICATION:
        "99b443650b5f74c508e25d982aa09b06632432bd9dd880f1364c69ff7afa1583",
    ROUND163_CERTIFICATE:
        "90d3313004be90049efb116a44731aef2554056661ce83b85afafdf3e3738539",
    ROUND163_VERIFICATION:
        "28ab965bffb0ab04d4fd839f1f7f895dbbab3a8e5be250a17fa95b7a8cc825d6",
    ROUND164_CERTIFICATE:
        "2f1fcb72224f39c8d4a9d9f666a8579f71d77542e31552aa7c9dbc4b7338f092",
    ROUND164_VERIFICATION:
        "850bd24ae60979aaaea3f6819dcab665a1f7228d0c104014bfe8cce9e91299b0",
}

ROUND139_RESULT_SHA256 = (
    "6e8f54c34154ea5ba3c95d4e901bc643c020a0a42e180241ae9053bb24f42236"
)
ROUND139_VERIFICATION_RESULT_SHA256 = (
    "e96609b3ff1ba35c94e224c5d16897ed6d173fe69cc3cbf260ff85e5340165e1"
)
ROUND162_BRIDGE_RESULT_SHA256 = (
    "5a327f96ecc8183af76695123dcf6fc4ccbf443e4bd7427cef38090c06bcfe86"
)
ROUND162_BRIDGE_VERIFICATION_RESULT_SHA256 = (
    "3d74d45804c8cef12782eeda57e7f770e6d8b9f962f97d1f28c54c92b27c6421"
)
ROUND163_RESULT_SHA256 = (
    "d64b5fab6b599a8fb4d6665c8abb902d79f86afd0370610845a5f7558d848102"
)
ROUND163_VERIFICATION_RESULT_SHA256 = (
    "183b30155016229f27ba35293ad98d4b1b779af19c84dab5fec583862c8ef8a9"
)
ROUND164_RESULT_SHA256 = (
    "0f6d7f47ac20734ed294dd04cd7720ccbb9c0a1d4236980f814dd2ea2d5e79d9"
)
ROUND164_VERIFICATION_RESULT_SHA256 = (
    "bb2e51bdbbd457a5782038efc527000cbf89b73c8645fd6facd126fa453af8c4"
)

SOURCE_CHARTS = tuple(
    f"{source}:{cell}"
    for source in ("G", "W")
    for cell in ("E", "W", "N", "S")
)
SOURCE_G_CHARTS = ("G:E", "G:W", "G:N", "G:S")
RADIUS = {"G": Q(9, 25), "W": Q(4, 25)}
EPS = Q(1, 400)
TAU_MAX = Q(3)
INV_SQRT2_LOWER = Q(707, 1000)
INV_SQRT2_UPPER = Q(708, 1000)
MAX_CROSSINGS_PER_AXIS = 4


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


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def strict_load(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    require(
        not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        f"encoding:{path.name}",
    )

    def reject(value: str) -> None:
        raise ValueError(value)

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, f"duplicate key:{key}")
            result[key] = value
        return result

    value = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=unique,
        parse_constant=reject,
        parse_float=reject,
    )

    def strings(item: Any) -> None:
        if type(item) is str:
            require(
                "\x00" not in item
                and not any(
                    0xD800 <= ord(character) <= 0xDFFF
                    for character in item
                ),
                "decoded string encoding",
            )
        elif type(item) is list:
            for child in item:
                strings(child)
        elif type(item) is dict:
            for key, child in item.items():
                strings(key)
                strings(child)

    strings(value)
    require(type(value) is dict, f"top object:{path.name}")
    return value


def check_wrapper(
    document: dict[str, Any],
    schema: str,
    result_sha256: str,
    status: str | None = None,
) -> dict[str, Any]:
    require(
        set(document) == {"schema", "result", "result_sha256"},
        f"wrapper:{schema}",
    )
    require(document["schema"] == schema, f"schema:{schema}")
    require(
        document["result_sha256"] == result_sha256
        == digest(document["result"]),
        f"result digest:{schema}",
    )
    if status is not None:
        require(document["result"]["status"] == status, f"status:{schema}")
    return document["result"]


def load_inputs() -> dict[str, dict[str, Any]]:
    for name, expected in PINS.items():
        require(
            hashlib.sha256((HERE / name).read_bytes()).hexdigest() == expected,
            f"pin:{name}",
        )
    loaded = {
        name: strict_load(HERE / name)
        for name in (
            FIRST_HIT_MANIFEST,
            ATLAS_MANIFEST,
            KEY_MANIFEST,
            ROUND139_CERTIFICATE,
            ROUND139_VERIFICATION,
            ROUND162_BRIDGE,
            ROUND162_BRIDGE_VERIFICATION,
            ROUND163_CERTIFICATE,
            ROUND163_VERIFICATION,
            ROUND164_CERTIFICATE,
            ROUND164_VERIFICATION,
        )
    }
    check_wrapper(
        loaded[ROUND139_CERTIFICATE],
        "cm2.round139.rank3-minus-d0-adjacent-h1-collar-return-frontier.v1",
        ROUND139_RESULT_SHA256,
        "CERTIFIED_MINUS_D0_ADJACENT_H1_COLLAR_STRICT_FIRST_RETURN",
    )
    r139v = check_wrapper(
        loaded[ROUND139_VERIFICATION],
        "cm2.round139.rank3-minus-d0-adjacent-h1-collar-return-frontier-verification.v1",
        ROUND139_VERIFICATION_RESULT_SHA256,
        "PASS",
    )
    require(
        r139v["certificate_result_sha256"] == ROUND139_RESULT_SHA256,
        "Round139 verification binding",
    )
    bridge = check_wrapper(
        loaded[ROUND162_BRIDGE],
        "cm2.round162.compact-gate3-coordinate-bridge.v1",
        ROUND162_BRIDGE_RESULT_SHA256,
        "CERTIFIED_COMPACT_TO_GATE3_SOURCE_W_COORDINATE_COVER__"
        "DYNAMICAL_EXTERIOR_CENSUS_AND_D02_STILL_BLOCKED",
    )
    bridge_v = check_wrapper(
        loaded[ROUND162_BRIDGE_VERIFICATION],
        "cm2.round162.compact-gate3-coordinate-bridge.verification.v1",
        ROUND162_BRIDGE_VERIFICATION_RESULT_SHA256,
        "PASS",
    )
    require(
        bridge_v["certificate_result_sha256"] == ROUND162_BRIDGE_RESULT_SHA256
        and bridge["scope"]["source_obstacle"] == "W"
        and bridge["scope"]["does_not_exhaust_return_signatures"] is True,
        "Round162 bridge scope",
    )
    r163 = check_wrapper(
        loaded[ROUND163_CERTIFICATE],
        "cm2.round163.outgoing-chart-pruning.v1",
        ROUND163_RESULT_SHA256,
        "CERTIFIED_FROZEN_PREFIX_OUTGOING_CHART_PRUNING__"
        "EXTERIOR_AND_D02_STILL_BLOCKED",
    )
    r163v = check_wrapper(
        loaded[ROUND163_VERIFICATION],
        "cm2.round163.outgoing-chart-pruning.verification.v1",
        ROUND163_VERIFICATION_RESULT_SHA256,
        "PASS",
    )
    require(
        r163v["certificate_result_sha256"] == ROUND163_RESULT_SHA256,
        "Round163 verification binding",
    )
    r164 = check_wrapper(
        loaded[ROUND164_CERTIFICATE],
        "cm2.round164.dimension-safe-tangency-graph-typing.v2",
        ROUND164_RESULT_SHA256,
        "CERTIFIED_DIMENSION_SAFE_OUTSIDE_W_W_TANGENCY_GRAPH_TYPING__"
        "NO_WHOLE_LEAF_PRUNING__D02_STILL_BLOCKED",
    )
    r164v = check_wrapper(
        loaded[ROUND164_VERIFICATION],
        "cm2.round164.dimension-safe-tangency-graph-typing.verification.v2",
        ROUND164_VERIFICATION_RESULT_SHA256,
        "PASS",
    )
    require(
        r164v["certificate_result_sha256"] == ROUND164_RESULT_SHA256
        and r164v["full_document_exactly_matched"] is True,
        "Round164 verification binding",
    )
    loaded["_bridge_result"] = bridge
    loaded["_round163_result"] = r163
    loaded["_round164_result"] = r164
    return loaded


def targets() -> tuple[tuple[str, int, int], ...]:
    return tuple(
        (obstacle, ix, iy)
        for obstacle in ("G", "W")
        for ix in range(-4, 5)
        for iy in range(-4, 5)
    )


TARGETS = targets()


def target_id(target: tuple[str, int, int]) -> str:
    obstacle, ix, iy = target
    return f"{obstacle}[{ix},{iy}]"


def vector_interval(
    source: str, target: tuple[str, int, int]
) -> tuple[Q, Q, Q, Q]:
    obstacle, ix, iy = target
    if source == "G" and obstacle == "G":
        return Q(ix), Q(ix), Q(iy), Q(iy)
    if source == "G" and obstacle == "W":
        x = Q(2 * ix + 1, 2)
        return x - EPS, x + EPS, Q(2 * iy + 1, 2), Q(2 * iy + 1, 2)
    if source == "W" and obstacle == "G":
        x = Q(2 * ix - 1, 2)
        return x - EPS, x + EPS, Q(2 * iy - 1, 2), Q(2 * iy - 1, 2)
    return Q(ix), Q(ix), Q(iy), Q(iy)


def square_min_abs(lower: Q, upper: Q) -> Q:
    if lower <= 0 <= upper:
        return Q(0)
    return min(lower * lower, upper * upper)


def absmax(lower: Q, upper: Q) -> Q:
    return max(abs(lower), abs(upper))


def support_upper(
    cell: str, x0: Q, x1: Q, y0: Q, y1: Q
) -> Q:
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


def classification(
    chart_id: str, target: tuple[str, int, int]
) -> str:
    source, cell = chart_id.split(":")
    obstacle, ix, iy = target
    if obstacle == source and ix == 0 and iy == 0:
        return "self_source"
    x0, x1, y0, y1 = vector_interval(source, target)
    distance2 = (
        square_min_abs(x0, x1) + square_min_abs(y0, y1)
    )
    threshold = TAU_MAX + RADIUS[source] + RADIUS[obstacle]
    if distance2 >= threshold * threshold:
        return "empty_horizon_center_distance"
    if support_upper(cell, x0, x1, y0, y1) < (
        RADIUS[source] - RADIUS[obstacle]
    ):
        return "empty_outgoing_halfspace"
    return "retained_candidate"


def candidate_ids(chart_id: str) -> tuple[str, ...]:
    return tuple(
        target_id(target)
        for target in TARGETS
        if classification(chart_id, target) == "retained_candidate"
    )


def crossing_patterns() -> tuple[tuple[str, ...], ...]:
    result: list[tuple[str, ...]] = []
    for nx in range(MAX_CROSSINGS_PER_AXIS + 1):
        for ny in range(MAX_CROSSINGS_PER_AXIS + 1):
            length = nx + ny
            x_signs = (0,) if nx == 0 else (-1, 1)
            y_signs = (0,) if ny == 0 else (-1, 1)
            for sx in x_signs:
                for sy in y_signs:
                    for positions in itertools.combinations(range(length), nx):
                        x_positions = set(positions)
                        x_token = "X+" if sx > 0 else "X-"
                        y_token = "Y+" if sy > 0 else "Y-"
                        result.append(tuple(
                            x_token if index in x_positions else y_token
                            for index in range(length)
                        ))
    return tuple(result)


def stream_digest(rows: Iterable[Any]) -> tuple[int, str]:
    hasher = hashlib.sha256()
    count = 0
    for row in rows:
        hasher.update(canonical(row).encode("utf-8"))
        hasher.update(b"\n")
        count += 1
    return count, hasher.hexdigest()


def registry_tables() -> dict[str, Any]:
    patterns = crossing_patterns()
    require(len(patterns) == 985 and len(set(patterns)) == 985, "patterns")
    expected_pattern_histogram = {
        0: 1,
        1: 4,
        2: 12,
        3: 28,
        4: 60,
        5: 120,
        6: 200,
        7: 280,
        8: 280,
    }
    require(
        dict(sorted(Counter(map(len, patterns)).items()))
        == expected_pattern_histogram,
        "pattern histogram",
    )
    pairs = tuple(
        (chart_id, target)
        for chart_id in SOURCE_CHARTS
        for target in candidate_ids(chart_id)
    )
    require(len(pairs) == 448 and len(set(pairs)) == 448, "pair count")
    pair_index = {pair: index for index, pair in enumerate(pairs)}
    pattern_index = {
        pattern: index for index, pattern in enumerate(patterns)
    }
    word_count, word_sha256 = stream_digest(
        [
            chart_id,
            target,
            list(pattern),
            len(pattern) + 1,
        ]
        for chart_id, target in pairs
        for pattern in patterns
    )
    require(word_count == 441280, "word count")
    return {
        "patterns": patterns,
        "pattern_index": pattern_index,
        "pairs": pairs,
        "pair_index": pair_index,
        "pair_sha256": digest(pairs),
        "word_sha256": word_sha256,
    }


def expected_key(
    row: list[Any],
    tables: dict[str, Any],
) -> tuple[int, str, str]:
    require(
        type(row) is list
        and len(row) == 4
        and type(row[0]) is str
        and type(row[1]) is str
        and type(row[2]) is list
        and all(type(token) is str for token in row[2])
        and type(row[3]) is int,
        "official row shape",
    )
    chart, target, tokens, roof = row
    pattern = tuple(tokens)
    require((chart, target) in tables["pair_index"], "official pair")
    require(pattern in tables["pattern_index"], "official pattern")
    require(roof == len(pattern) + 1, "official roof")
    ordinal = (
        tables["pair_index"][(chart, target)] * len(tables["patterns"])
        + tables["pattern_index"][pattern]
    )
    row_sha256 = digest(row)
    return ordinal, f"gate5-word:{ordinal:06d}:{row_sha256}", row_sha256


def round139_witnesses(
    round139: dict[str, Any],
    tables: dict[str, Any],
) -> dict[str, Any]:
    require(
        digest(round139["collision_rows"])
        == round139["collision_rows_sha256"],
        "Round139 collision rows",
    )
    require(
        digest(round139["positive_area_collision_rows"])
        == round139["positive_area_collision_rows_sha256"],
        "Round139 positive rows",
    )
    require(
        len(round139["collision_rows"])
        == len(round139["positive_area_collision_rows"])
        == 1648,
        "Round139 row count",
    )

    def audit(rows: list[dict[str, Any]]) -> list[tuple[int, list[Any]]]:
        result: list[tuple[int, list[Any]]] = []
        for collision in rows:
            key = collision["official_word_key"]
            require(
                set(key) == {
                    "official_word_key_id",
                    "ordinal_zero_based",
                    "registry_row",
                    "registry_row_sha256",
                },
                "official key fields",
            )
            ordinal, identifier, row_sha256 = expected_key(
                key["registry_row"], tables
            )
            require(
                key["ordinal_zero_based"] == ordinal
                and key["official_word_key_id"] == identifier
                and key["registry_row_sha256"] == row_sha256,
                "official key binding",
            )
            result.append((ordinal, key["registry_row"]))
        return result

    graph_rows = audit(round139["collision_rows"])
    positive_rows = audit(round139["positive_area_collision_rows"])
    require(
        [ordinal for ordinal, _row in graph_rows]
        == [ordinal for ordinal, _row in positive_rows],
        "Round139 key sequence equality",
    )
    source_g_occurrences = [
        (ordinal, row)
        for ordinal, row in positive_rows
        if row[0] in SOURCE_G_CHARTS
    ]
    unique = {
        ordinal: row for ordinal, row in source_g_occurrences
    }
    require(len(unique) == 103, "source-G witness keys")
    unique_rows = [
        unique[ordinal] for ordinal in sorted(unique)
    ]
    return {
        "occurrences": source_g_occurrences,
        "unique": unique,
        "unique_rows": unique_rows,
        "unique_rows_sha256": digest(unique_rows),
    }


def histogram_strings(values: Counter[int]) -> dict[str, int]:
    return {
        str(key): values[key]
        for key in sorted(values)
    }


def build_result() -> dict[str, Any]:
    loaded = load_inputs()
    first = loaded[FIRST_HIT_MANIFEST]
    atlas = loaded[ATLAS_MANIFEST]
    key_manifest = loaded[KEY_MANIFEST]
    round139 = loaded[ROUND139_CERTIFICATE]["result"]
    r163 = loaded["_round163_result"]
    r164 = loaded["_round164_result"]
    bridge = loaded["_bridge_result"]

    require(
        first["schema"] == "cm2.gate3.first-hit-atlas.v1"
        and first["candidate_reduction"]["chart_target_pair_count"] == 1296
        and first["candidate_reduction"]["retained_pair_count"] == 448
        and first["candidate_reduction"]["certified_empty_pair_count"] == 848,
        "first-hit manifest",
    )
    require(
        atlas["schema"] == "cm2.gate3.eight-cell-symmetry-atlas.v1"
        and atlas["coverage"]["global_leaf_count"] == 143248
        and atlas["coverage"]["every_leaf_spans_full_s_window"] is True,
        "atlas manifest",
    )
    registry = key_manifest["result"]["immutable_candidate_key_registry"]
    require(
        key_manifest["schema"]
        == "cm2.gate5.return-word-three-norm-frontier.manifest.v1"
        and key_manifest["verdict"]["regular_return_word_candidate_key_envelope"]
        == "CERTIFIED"
        and key_manifest["verdict"]["physical_homogeneous_operator_registry"]
        == "NOT_CERTIFIED"
        and registry["candidate_return_word_key_count"] == 441280
        and registry["retained_chart_target_pair_count"] == 448
        and registry["crossing_pattern_count_per_pair"] == 985,
        "key manifest",
    )

    tables = registry_tables()
    require(
        tables["pair_sha256"] == registry["chart_target_pair_rows_sha256"]
        and tables["word_sha256"] == registry["candidate_word_key_rows_sha256"],
        "global exact key replay",
    )
    witnesses = round139_witnesses(round139, tables)

    reflection = atlas["reflection_certificate"]
    require(
        reflection["quarter_turn_used"] is False
        and atlas["charts"]["G:E"]["provenance"] == "direct_192_bit_Arb"
        and atlas["charts"]["G:N"]["provenance"] == "direct_192_bit_Arb"
        and atlas["charts"]["G:W"]["provenance"]
        == "exact_reflection_of_G:E"
        and atlas["charts"]["G:S"]["provenance"]
        == "exact_reflection_of_G:N",
        "source-G atlas provenance",
    )

    patterns = tables["patterns"]
    candidate_roof_histogram = Counter(len(pattern) + 1 for pattern in patterns)
    chart_rows: list[dict[str, Any]] = []
    source_g_leaf_total = Counter()
    source_g_pair_count = 0
    source_g_key_count = 0
    for chart_id in SOURCE_G_CHARTS:
        candidates = candidate_ids(chart_id)
        require(len(candidates) == 57, f"candidate count:{chart_id}")
        atlas_row = atlas["charts"][chart_id]
        require(
            atlas_row["candidate_count"] == len(candidates),
            f"atlas candidate count:{chart_id}",
        )
        chart_pairs = [
            (chart_id, candidate) for candidate in candidates
        ]
        chart_key_count, chart_key_sha256 = stream_digest(
            [
                chart_id,
                candidate,
                list(pattern),
                len(pattern) + 1,
            ]
            for candidate in candidates
            for pattern in patterns
        )
        chart_witness_occurrences = [
            (ordinal, row)
            for ordinal, row in witnesses["occurrences"]
            if row[0] == chart_id
        ]
        chart_witness_unique = {
            ordinal: row
            for ordinal, row in chart_witness_occurrences
        }
        witness_rows = [
            chart_witness_unique[ordinal]
            for ordinal in sorted(chart_witness_unique)
        ]
        candidate_by_roof = Counter({
            roof: len(candidates) * count
            for roof, count in candidate_roof_histogram.items()
        })
        witness_by_roof = Counter(row[3] for row in witness_rows)
        unwitnessed_by_roof = Counter({
            roof: candidate_by_roof[roof] - witness_by_roof[roof]
            for roof in candidate_by_roof
        })
        counts = atlas_row["counts"]
        require(
            atlas_row["leaf_count"]
            == counts["unique_first"]
            + counts["tangency_graph"]
            + counts["multi_candidate"],
            f"atlas conservation:{chart_id}",
        )
        source_g_leaf_total.update(counts)
        source_g_leaf_total["leaf_count"] += atlas_row["leaf_count"]
        source_g_pair_count += len(chart_pairs)
        source_g_key_count += chart_key_count
        first_ordinal = tables["pair_index"][chart_pairs[0]] * len(patterns)
        last_ordinal = (
            (tables["pair_index"][chart_pairs[-1]] + 1) * len(patterns) - 1
        )
        chart_rows.append({
            "source_chart": chart_id,
            "atlas_provenance": atlas_row["provenance"],
            "candidate_target_count": len(candidates),
            "candidate_target_ids_sha256": digest(candidates),
            "candidate_chart_target_pair_count": len(chart_pairs),
            "candidate_chart_target_pairs_sha256": digest(chart_pairs),
            "candidate_exact_key_count": chart_key_count,
            "candidate_exact_key_stream_sha256": chart_key_sha256,
            "candidate_exact_key_ordinal_interval_inclusive": [
                first_ordinal,
                last_ordinal,
            ],
            "candidate_exact_key_roof_histogram":
                histogram_strings(candidate_by_roof),
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
                len(chart_witness_occurrences),
            "round139_positive_area_local_witness_exact_key_count":
                len(witness_rows),
            "round139_positive_area_local_witness_target_pair_count":
                len({(row[0], row[1]) for row in witness_rows}),
            "round139_positive_area_local_witness_exact_key_rows_sha256":
                digest(witness_rows),
            "round139_positive_area_local_witness_roof_histogram":
                histogram_strings(witness_by_roof),
            "candidate_keys_without_a_Round139_local_witness_count":
                chart_key_count - len(witness_rows),
            "candidate_keys_without_a_Round139_local_witness_roof_histogram":
                histogram_strings(unwitnessed_by_roof),
            "globally_dispositioned_exact_key_count": 0,
            "keys_without_a_global_geometric_disposition_count":
                chart_key_count,
        })

    require(
        source_g_pair_count == 228
        and source_g_key_count == 224580
        and source_g_leaf_total == Counter({
            "leaf_count": 66420,
            "unique_first": 21232,
            "tangency_graph": 160,
            "multi_candidate": 45028,
        }),
        "source-G totals",
    )
    unique_witness_rows = witnesses["unique_rows"]
    unique_witness_pairs = {
        (row[0], row[1]) for row in unique_witness_rows
    }
    witness_roof_histogram = Counter(row[3] for row in unique_witness_rows)
    require(
        len(witnesses["occurrences"]) == 1143
        and len(unique_witness_rows) == 103
        and len(unique_witness_pairs) == 52
        and witness_roof_histogram == Counter({1: 28, 2: 56, 3: 17, 4: 2}),
        "Round139 source-G witness totals",
    )

    ambient = r164["ambient_frozen_prefix_census"]
    require(
        r163["frozen_prefix"] == {
            "collision_index": 1,
            "required_owner": "W[1,0]",
            "required_outgoing_chart": "W",
        }
        and ambient["combined_recordwise_excluded_ambient_leaf_count"]
        == 37480
        and ambient["remaining_ambient_unresolved_leaf_count"] == 39348
        and ambient["new_full_dimensional_ambient_leaf_exclusion_count"] == 0
        and ambient["component_sum"] == 39348,
        "source-W baseline",
    )

    return {
        "status": STATUS,
        "scope": {
            "object":
                "source-G exact candidate return-signature coverage census",
            "source_charts": list(SOURCE_G_CHARTS),
            "parameter_window": "|s|<=1/400",
            "candidate_key":
                "(source normal chart, retained target lift, "
                "monotone clean-wall record, roof)",
            "survey_only": True,
            "adds_no_leaf_or_exact_key_exclusion": True,
            "adds_no_connected_or_cemetery_disposition": True,
        },
        "provenance": {
            "dependency_sha256": PINS,
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
            "candidate_chart_target_pair_count": source_g_pair_count,
            "crossing_pattern_count_per_pair": len(patterns),
            "candidate_exact_key_count": source_g_key_count,
            "atlas_leaf_count": source_g_leaf_total["leaf_count"],
            "atlas_unique_first_leaf_count":
                source_g_leaf_total["unique_first"],
            "atlas_tangency_graph_leaf_count":
                source_g_leaf_total["tangency_graph"],
            "atlas_multi_candidate_leaf_count":
                source_g_leaf_total["multi_candidate"],
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
            "candidate_chart_target_pair_count": source_g_pair_count,
            "candidate_exact_key_envelope_count": source_g_key_count,
            "candidate_exact_key_envelope_fraction": "224580/224580",
            "Round139_positive_area_local_witness_occurrence_count":
                len(witnesses["occurrences"]),
            "Round139_positive_area_local_witness_exact_key_count":
                len(unique_witness_rows),
            "Round139_positive_area_local_witness_exact_key_rows_sha256":
                witnesses["unique_rows_sha256"],
            "Round139_positive_area_local_witness_chart_target_pair_count":
                len(unique_witness_pairs),
            "Round139_positive_area_local_witness_roof_histogram":
                histogram_strings(witness_roof_histogram),
            "Round139_positive_area_local_witness_fraction":
                "103/224580",
            "candidate_keys_without_a_Round139_local_witness_count":
                source_g_key_count - len(unique_witness_rows),
            "global_geometric_exact_key_disposition_count": 0,
            "global_geometric_exact_key_disposition_fraction": "0/224580",
            "keys_without_a_global_geometric_disposition_count":
                source_g_key_count,
            "why_local_witnesses_are_not_global_dispositions":
                "the 103 keys occur along one certified positive-area local "
                "R1648 cylinder; they do not partition or exhaust any complete "
                "source-G chart-key domain",
        },
        "missing_certified_interfaces": [
            {
                "priority": 1,
                "interface":
                    "source-G compact-to-Gate3 coordinate bridge",
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
                "interface":
                    "source-G multi-candidate refinement",
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


def build() -> dict[str, Any]:
    result = build_result()
    return {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    arguments.output.write_text(
        json.dumps(
            build(),
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"WROTE {arguments.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
