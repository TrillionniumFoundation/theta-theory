#!/usr/bin/env python3
"""Round173: exact Jx/Jy transport of source-G Gate-5 return signatures.

This producer independently rebuilds the frozen 448-pair/985-word Gate-5
candidate registry, extracts its 224,580 source-G keys, and derives the exact
Klein-four action in the source-G rebased lift induced by

    Jx(x,y,s,p) = (-x,y,-s,-p),
    Jy(x,y,s,p) = (x,-y,s,-p).

The pinned atlas sometimes writes the same torus reflections as ``1-x`` or
``1-y`` before source-lift rebasing.  The integer deck translation that puts
the reflected source back at G[0,0] changes those formulas to ``-x`` and
``-y`` here.  Consequently an official local integer wall k maps to -k.

The action includes source charts, target lifts, signed wall tokens and their
order, roofs, immutable Gate-5 ordinals, strict outgoing charts, and the
half-open seam owner rule.  It is a transport dictionary, not a dynamical
row census: no source-G leaf is assigned an owner, wall word, outgoing chart,
or exact-key disposition here.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import os
import stat
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
OUTPUT = (
    HERE
    / "cm2_round173_source_g_exact_return_signature_transport_certificate.json"
)
SCHEMA = "cm2.round173.source-g-exact-return-signature-transport.v1"
STATUS = (
    "CERTIFIED_SOURCE_G_JX_JY_EXACT_RETURN_SIGNATURE_TRANSPORT_DICTIONARY__"
    "NO_DYNAMIC_ROW_OR_D02_PROMOTION"
)

ROUND169_PRODUCER = "cm2_round169_source_g_return_signature_coverage_survey.py"
ROUND169_CERTIFICATE = (
    "cm2_round169_source_g_return_signature_coverage_survey_certificate.json"
)
ROUND169_VERIFIER = (
    "cm2_round169_source_g_return_signature_coverage_survey_verifier.py"
)
ROUND169_VERIFICATION = (
    "cm2_round169_source_g_return_signature_coverage_survey_verification.json"
)
ROUND171_PRODUCER = "cm2_round171_compact_gate3_source_g_coordinate_bridge.py"
ROUND171_CERTIFICATE = (
    "cm2_round171_compact_gate3_source_g_coordinate_bridge_certificate.json"
)
ROUND171_VERIFIER = (
    "cm2_round171_compact_gate3_source_g_coordinate_bridge_verifier.py"
)
ROUND171_VERIFICATION = (
    "cm2_round171_compact_gate3_source_g_coordinate_bridge_verification.json"
)
GATE5_SOURCE = "cm2_gate5_return_word_three_norm_frontier_cert.py"
GATE5_VERIFIER = "cm2_gate5_return_word_three_norm_frontier_verifier.py"
GATE5_MANIFEST = (
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
)
GATE3_ATLAS_SOURCE = "cm2_gate3_eight_cell_symmetry_atlas_cert.py"
GATE3_ATLAS_MANIFEST = (
    "cm2-gate3-eight-cell-symmetry-atlas-manifest-2026-07-15.json"
)
FIRST_HIT_SOURCE = "cm2_gate3_candidate_first_hit_cert.py"
FIRST_HIT_MANIFEST = "cm2-gate3-first-hit-atlas-manifest-2026-07-15.json"
SEAM_SOURCE = "cm2_gate3_chart_seam_quotient_cert.py"
SEAM_VERIFIER = "cm2_gate3_chart_seam_quotient_verifier.py"
SEAM_MANIFEST = "cm2-gate3-chart-seam-quotient-manifest-2026-07-15.json"

PINS = {
    ROUND169_PRODUCER:
        "2be6580fb7d3d47a7ddab05f22d7987ba28d531bb1dd5af5c0082b458e089ee9",
    ROUND169_CERTIFICATE:
        "87c5b5f5467aa19b3bafce9e20c10371877012af65937983ced43fcccb22c2fb",
    ROUND169_VERIFIER:
        "ed5d26a532f184702551da526e5ffbc0feafbf1e8c89eb55d260b15428aaab67",
    ROUND169_VERIFICATION:
        "90c207dd952329d0547ec0440e35cffa57d7b11f98ed17869f3a07df6ce3161f",
    ROUND171_PRODUCER:
        "bcaba20978ebb5386d64bcf248d254c54c8ac79d9c9c7eb023be278ab7e05c75",
    ROUND171_CERTIFICATE:
        "1fb4827b42569d41602765445d0333c76b2ef97615873fc406563ac0e18af7a5",
    ROUND171_VERIFIER:
        "aee7b3cc3f1468b6a46e7a90e1bb219bd609bddfe54075c6c73e124d98eda7e0",
    ROUND171_VERIFICATION:
        "effdfd4306dbf7bd70df1e9b5ed9166a58dc00a5d333b0f2f2a5f0cb930ccce9",
    GATE5_SOURCE:
        "ddcc250f8700c6a695f96019d9f7824fe98636e20a67685fdc6a3cce77f6d695",
    GATE5_VERIFIER:
        "0384acdd1f912b0d4b3bee84ff530358d9693893d1c5c64a1deabaede8e0867b",
    GATE5_MANIFEST:
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866",
    GATE3_ATLAS_SOURCE:
        "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    GATE3_ATLAS_MANIFEST:
        "f8fda665edbb7d8b39ce495188f90ecb2b5ec4384c1eb958949627df167c4987",
    FIRST_HIT_SOURCE:
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    FIRST_HIT_MANIFEST:
        "0c820a5e3481b2c18fabb14d8d0fab7ce454f9a9e68b856bb2a7bf139404f7f4",
    SEAM_SOURCE:
        "fa00d4c14ee24b8f3fbc7f345deef13deb272080a886b68d2aa2f9c92a456fe1",
    SEAM_VERIFIER:
        "3eb5b5525eab0d2e4935374e6d9fa453717de13634613afa579cd1ae30dbcea6",
    SEAM_MANIFEST:
        "1fb40060336f04f28a7cac19a70abdd3692ced272825b2f1f6b6ae005f00518b",
}
ROUND169_RESULT_SHA256 = (
    "8cf83c0ef48aea3a6023546a2df52398241d7baf113e9b78a917c7de4e3d68d6"
)
ROUND169_VERIFICATION_RESULT_SHA256 = (
    "4c89a30e89f4fd0b599264a52c8a81f535c4c9df6c60682e6f60594744decdb1"
)
ROUND171_RESULT_SHA256 = (
    "ffac0e2e16829c1a3ffc4783af2c224288265d02cf53c1d041aaf02013b52957"
)
ROUND171_VERIFICATION_RESULT_SHA256 = (
    "60e9d4038c63bba14c0bd95478f63840735d8283f9cdfdefb1405ee2ed7defe3"
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
PATTERN_COUNT = 985
SOURCE_G_PAIR_COUNT = 228
SOURCE_G_KEY_COUNT = SOURCE_G_PAIR_COUNT * PATTERN_COUNT
GENERATORS = ("Jx", "Jy")


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


def safe_input(path: Path) -> None:
    require(path.exists(), f"missing input:{path.name}")
    require(not path.is_symlink(), f"input symlink:{path.name}")
    information = path.stat()
    require(stat.S_ISREG(information.st_mode), f"input regular:{path.name}")
    require(information.st_nlink == 1, f"input hardlink:{path.name}")
    require(not path.parent.is_symlink(), f"input parent:{path.name}")


def strict_decode(raw: bytes) -> dict[str, Any]:
    require(
        not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        "raw encoding",
    )

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, f"duplicate key:{key}")
            result[key] = value
        return result

    def reject(token: str) -> None:
        raise ValueError(token)

    value = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=unique,
        parse_constant=reject,
        parse_float=reject,
    )

    def walk(item: Any) -> None:
        if type(item) is str:
            require(
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
    require(type(value) is dict, "top object")
    return value


def strict_load(path: Path) -> dict[str, Any]:
    safe_input(path)
    return strict_decode(path.read_bytes())


def wrapped(
    document: dict[str, Any],
    schema: str,
    result_sha256: str,
    status: str,
) -> dict[str, Any]:
    require(
        set(document) == {"schema", "result", "result_sha256"},
        f"wrapper:{schema}",
    )
    require(document["schema"] == schema, f"schema:{schema}")
    require(
        document["result_sha256"] == result_sha256
        == digest(document["result"]),
        f"digest:{schema}",
    )
    require(document["result"]["status"] == status, f"status:{schema}")
    return document["result"]


def load_inputs() -> dict[str, Any]:
    for name, expected in PINS.items():
        path = HERE / name
        safe_input(path)
        require(
            hashlib.sha256(path.read_bytes()).hexdigest() == expected,
            f"pin:{name}",
        )
    r169 = wrapped(
        strict_load(HERE / ROUND169_CERTIFICATE),
        "cm2.round169.source-g-return-signature-coverage-survey.v1",
        ROUND169_RESULT_SHA256,
        "CERTIFIED_SOURCE_G_EXACT_KEY_COVERAGE_DEFICIT_SURVEY__"
        "NO_EXTERIOR_OR_D02_PROMOTION",
    )
    r169v = wrapped(
        strict_load(HERE / ROUND169_VERIFICATION),
        "cm2.round169.source-g-return-signature-coverage-survey.verification.v1",
        ROUND169_VERIFICATION_RESULT_SHA256,
        "PASS",
    )
    r171 = wrapped(
        strict_load(HERE / ROUND171_CERTIFICATE),
        "cm2.round171.compact-gate3-source-g-coordinate-bridge.v1",
        ROUND171_RESULT_SHA256,
        "CERTIFIED_COMPACT_TO_GATE3_SOURCE_G_COORDINATE_COVER__"
        "NO_RETURN_KEY_OR_D02_PROMOTION",
    )
    r171v = wrapped(
        strict_load(HERE / ROUND171_VERIFICATION),
        "cm2.round171.compact-gate3-source-g-coordinate-bridge.verification.v1",
        ROUND171_VERIFICATION_RESULT_SHA256,
        "PASS",
    )
    require(
        r169v["certificate_result_sha256"] == ROUND169_RESULT_SHA256
        and r169v["full_document_exactly_matched"] is True
        and r169v["producer_imported_or_executed"] is False,
        "Round169 verification",
    )
    require(
        r171v["certificate_result_sha256"] == ROUND171_RESULT_SHA256
        and r171v["full_document_exactly_matched"] is True
        and r171v["producer_imported_or_executed"] is False,
        "Round171 verification",
    )
    gate5 = strict_load(HERE / GATE5_MANIFEST)
    atlas = strict_load(HERE / GATE3_ATLAS_MANIFEST)
    first_hit = strict_load(HERE / FIRST_HIT_MANIFEST)
    seam = strict_load(HERE / SEAM_MANIFEST)
    require(
        gate5["schema"]
        == "cm2.gate5.return-word-three-norm-frontier.manifest.v1"
        and gate5["certificate_sha256"] == PINS[GATE5_SOURCE]
        and gate5["verifier_sha256"] == PINS[GATE5_VERIFIER],
        "Gate5 wrapper",
    )
    registry = gate5["result"]["immutable_candidate_key_registry"]
    grammar = gate5["result"]["crossing_grammar"]
    completion = gate5["result"]["completion"]
    require(
        registry["retained_chart_target_pair_count"] == 448
        and registry["crossing_pattern_count_per_pair"] == PATTERN_COUNT
        and registry["candidate_return_word_key_count"] == 441280
        and registry["complete_physical_operator_block_count"] == 0
        and grammar["crossing_pattern_count"] == PATTERN_COUNT
        and completion["complete_regular_return_word_candidate_key_envelope"]
        is True
        and completion["immutable_complete_return_word_operator_registry"]
        is False
        and gate5["verdict"]["gate5"] == "NOT_CERTIFIED",
        "Gate5 frontier",
    )
    require(
        first_hit["schema"] == "cm2.gate3.first-hit-atlas.v1"
        and first_hit["candidate_reduction"]["chart_target_pair_count"] == 1296
        and first_hit["candidate_reduction"]["retained_pair_count"] == 448
        and first_hit["candidate_reduction"]["certified_empty_pair_count"] == 848,
        "first-hit frontier",
    )
    require(
        atlas["schema"] == "cm2.gate3.eight-cell-symmetry-atlas.v1"
        and atlas["coverage"]["global_leaf_count"] == 143248
        and atlas["reflection_certificate"]["row_digests"][
            "G:E->G:W"
        ] == "46da8d49fbfc1493e1229bd4bd7c1a9dae9035a286bd97d58484ac312e4a4683"
        and atlas["reflection_certificate"]["row_digests"][
            "G:N->G:S"
        ] == "e91640f12bebd3a49b385aa190a6758f62aa10f1b87135eee5fd833e4a3aa5b9",
        "Gate3 reflection atlas",
    )
    require(
        seam["schema"] == "cm2.gate3.chart-seam-quotient.manifest.v1"
        and seam["verdict"]["eight_chart_seam_ownership"] == "CERTIFIED"
        and seam["result"]["unique_half_open_owner_rule"][
            "diagonal_tie"
        ] == "E or W owns; N or S excludes"
        and seam["result"]["scope_limits"][
            "all_eight_chart_seams_have_unique_owner"
        ] is True,
        "half-open seam quotient",
    )
    return {
        "round169": r169,
        "round171": r171,
        "gate5": gate5,
        "atlas": atlas,
        "first_hit": first_hit,
        "seam": seam,
    }


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


def parse_target(value: str) -> tuple[str, int, int]:
    require(
        len(value) >= 6
        and value[0] in "GW"
        and value[1] == "["
        and value[-1] == "]"
        and value.count(",") == 1,
        "target syntax",
    )
    left, right = value[2:-1].split(",")
    return value[0], int(left), int(right)


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
    distance2 = square_min_abs(x0, x1) + square_min_abs(y0, y1)
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


def rebuild_registry(
    gate5: dict[str, Any],
) -> dict[str, Any]:
    patterns = crossing_patterns()
    require(len(patterns) == PATTERN_COUNT, "pattern count")
    require(len(set(patterns)) == PATTERN_COUNT, "pattern uniqueness")
    require(
        dict(sorted(Counter(map(len, patterns)).items()))
        == {
            0: 1,
            1: 4,
            2: 12,
            3: 28,
            4: 60,
            5: 120,
            6: 200,
            7: 280,
            8: 280,
        },
        "pattern histogram",
    )
    pairs = tuple(
        (chart, target)
        for chart in SOURCE_CHARTS
        for target in candidate_ids(chart)
    )
    require(len(pairs) == 448 and len(set(pairs)) == 448, "pair registry")
    source_g_pairs = tuple(pair for pair in pairs if pair[0].startswith("G:"))
    require(
        len(source_g_pairs) == SOURCE_G_PAIR_COUNT
        and pairs[:SOURCE_G_PAIR_COUNT] == source_g_pairs
        and all(len(candidate_ids(chart)) == 57 for chart in SOURCE_G_CHARTS),
        "source-G prefix",
    )
    word_count, word_sha256 = stream_digest(
        [
            chart,
            target,
            list(pattern),
            len(pattern) + 1,
        ]
        for chart, target in pairs
        for pattern in patterns
    )
    source_count, source_sha256 = stream_digest(
        [
            chart,
            target,
            list(pattern),
            len(pattern) + 1,
        ]
        for chart, target in source_g_pairs
        for pattern in patterns
    )
    registry = gate5["result"]["immutable_candidate_key_registry"]
    grammar = gate5["result"]["crossing_grammar"]
    require(
        digest(pairs) == registry["chart_target_pair_rows_sha256"]
        and digest(patterns) == grammar["crossing_pattern_rows_sha256"]
        and word_count == 441280
        and word_sha256 == registry["candidate_word_key_rows_sha256"]
        and source_count == SOURCE_G_KEY_COUNT,
        "registry digest",
    )
    return {
        "patterns": patterns,
        "pattern_index": {
            pattern: index for index, pattern in enumerate(patterns)
        },
        "pairs": pairs,
        "source_g_pairs": source_g_pairs,
        "source_g_pair_index": {
            pair: index for index, pair in enumerate(source_g_pairs)
        },
        "source_g_key_rows_sha256": source_sha256,
    }


def chart_map(generator: str, chart_id: str) -> str:
    source, cell = chart_id.split(":")
    require(source == "G", "source-G chart")
    if generator == "Jx":
        cell = {"E": "W", "W": "E", "N": "N", "S": "S"}[cell]
    elif generator == "Jy":
        cell = {"E": "E", "W": "W", "N": "S", "S": "N"}[cell]
    else:
        raise ValueError(generator)
    return f"G:{cell}"


def target_map(generator: str, value: str) -> str:
    obstacle, ix, iy = parse_target(value)
    if generator == "Jx":
        ix = -ix if obstacle == "G" else -ix - 1
    elif generator == "Jy":
        iy = -iy if obstacle == "G" else -iy - 1
    else:
        raise ValueError(generator)
    return target_id((obstacle, ix, iy))


def source_g_target_displacement(
    value: str,
) -> tuple[Q, Q, Q, Q]:
    """Return dx=a+b*s, dy=c+d*s from G[0,0] to a target centre."""

    obstacle, ix, iy = parse_target(value)
    if obstacle == "G":
        return Q(ix), Q(0), Q(iy), Q(0)
    return Q(ix) + Q(1, 2), Q(1), Q(iy) + Q(1, 2), Q(0)


def check_target_displacement_identity(
    generator: str,
    source_target: str,
    destination_target: str,
) -> None:
    a, b, c, d = source_g_target_displacement(source_target)
    aa, bb, cc, dd = source_g_target_displacement(destination_target)
    if generator == "Jx":
        # Substitute s'=-s into the destination affine displacement.
        require(
            (aa, -bb, cc, -dd) == (-a, -b, c, d),
            "Jx target affine displacement",
        )
    elif generator == "Jy":
        # Here s'=s.
        require(
            (aa, bb, cc, dd) == (a, b, -c, -d),
            "Jy target affine displacement",
        )
    else:
        raise ValueError(generator)


def token_map(generator: str, token: str) -> str:
    require(token in {"X-", "X+", "Y-", "Y+"}, "wall token")
    if generator == "Jx" and token[0] == "X":
        return "X-" if token == "X+" else "X+"
    if generator == "Jy" and token[0] == "Y":
        return "Y-" if token == "Y+" else "Y+"
    return token


def pattern_map(
    generator: str, pattern: tuple[str, ...]
) -> tuple[str, ...]:
    return tuple(token_map(generator, token) for token in pattern)


def outgoing_map(generator: str, cell: str) -> str:
    require(cell in {"E", "W", "N", "S"}, "outgoing chart")
    if generator == "Jx":
        return {"E": "W", "W": "E", "N": "N", "S": "S"}[cell]
    if generator == "Jy":
        return {"E": "E", "W": "W", "N": "S", "S": "N"}[cell]
    raise ValueError(generator)


def compact_normal_numerator(chart: str) -> list[list[int]]:
    return {
        "E": [[1, 0, -1], [0, 2, 0]],
        "W": [[-1, 0, 1], [0, -2, 0]],
        "N": [[0, -2, 0], [1, 0, -1]],
        "S": [[0, 2, 0], [-1, 0, 1]],
    }[chart]


def substitute_minus_z(rows: list[list[int]]) -> list[list[int]]:
    return [
        [
            coefficient * (-1 if exponent % 2 else 1)
            for exponent, coefficient in enumerate(row)
        ]
        for row in rows
    ]


def reflect_vector_polynomial(
    generator: str,
    rows: list[list[int]],
) -> list[list[int]]:
    result = [list(row) for row in rows]
    component = 0 if generator == "Jx" else 1
    result[component] = [-coefficient for coefficient in result[component]]
    return result


def key_row(
    pair: tuple[str, str], pattern: tuple[str, ...]
) -> list[Any]:
    return [pair[0], pair[1], list(pattern), len(pattern) + 1]


def key_id(ordinal: int, row: list[Any]) -> str:
    return f"gate5-word:{ordinal:06d}:{digest(row)}"


def generator_contract(
    generator: str,
    tables: dict[str, Any],
) -> tuple[dict[str, Any], list[int]]:
    pairs = tables["source_g_pairs"]
    patterns = tables["patterns"]
    pair_lookup = tables["source_g_pair_index"]
    pattern_lookup = tables["pattern_index"]
    pair_permutation: list[int] = []
    for chart, target in pairs:
        mapped = (chart_map(generator, chart), target_map(generator, target))
        require(mapped in pair_lookup, f"mapped pair:{generator}")
        check_target_displacement_identity(generator, target, mapped[1])
        pair_permutation.append(pair_lookup[mapped])
    pattern_permutation = [
        pattern_lookup[pattern_map(generator, pattern)]
        for pattern in patterns
    ]
    require(
        sorted(pair_permutation) == list(range(SOURCE_G_PAIR_COUNT))
        and all(
            pair_permutation[pair_permutation[index]] == index
            for index in range(SOURCE_G_PAIR_COUNT)
        ),
        f"pair permutation:{generator}",
    )
    require(
        sorted(pattern_permutation) == list(range(PATTERN_COUNT))
        and all(
            pattern_permutation[pattern_permutation[index]] == index
            for index in range(PATTERN_COUNT)
        ),
        f"pattern permutation:{generator}",
    )
    ordinal_permutation = [
        pair_permutation[pair_index] * PATTERN_COUNT
        + pattern_permutation[pattern_index]
        for pair_index in range(SOURCE_G_PAIR_COUNT)
        for pattern_index in range(PATTERN_COUNT)
    ]
    require(
        sorted(ordinal_permutation) == list(range(SOURCE_G_KEY_COUNT))
        and all(
            ordinal_permutation[ordinal_permutation[index]] == index
            for index in range(SOURCE_G_KEY_COUNT)
        ),
        f"ordinal permutation:{generator}",
    )
    for source in range(SOURCE_G_KEY_COUNT):
        source_pair_index, source_pattern_index = divmod(
            source, PATTERN_COUNT
        )
        destination = ordinal_permutation[source]
        destination_pair_index, destination_pattern_index = divmod(
            destination, PATTERN_COUNT
        )
        require(
            destination_pair_index == pair_permutation[source_pair_index]
            and destination_pattern_index
            == pattern_permutation[source_pattern_index]
            and len(patterns[source_pattern_index])
            == len(patterns[destination_pattern_index]),
            f"ordinal conservation:{generator}",
        )
    pair_row_count, pair_row_sha256 = stream_digest(
        [index, value] for index, value in enumerate(pair_permutation)
    )
    pattern_row_count, pattern_row_sha256 = stream_digest(
        [index, value] for index, value in enumerate(pattern_permutation)
    )
    ordinal_row_count, ordinal_row_sha256 = stream_digest(
        [index, value] for index, value in enumerate(ordinal_permutation)
    )
    fixed_pairs = sum(
        index == value for index, value in enumerate(pair_permutation)
    )
    fixed_patterns = sum(
        index == value for index, value in enumerate(pattern_permutation)
    )
    fixed_ordinals = sum(
        index == value for index, value in enumerate(ordinal_permutation)
    )
    sample_ordinals = (
        0,
        56144,
        56145,
        112289,
        112290,
        168434,
        168435,
        224579,
    )
    sample_rows: list[dict[str, Any]] = []
    for source in sample_ordinals:
        destination = ordinal_permutation[source]
        source_pair_index, source_pattern_index = divmod(
            source, PATTERN_COUNT
        )
        destination_pair_index, destination_pattern_index = divmod(
            destination, PATTERN_COUNT
        )
        source_row = key_row(
            pairs[source_pair_index], patterns[source_pattern_index]
        )
        destination_row = key_row(
            pairs[destination_pair_index], patterns[destination_pattern_index]
        )
        require(
            destination_row == [
                chart_map(generator, source_row[0]),
                target_map(generator, source_row[1]),
                [
                    token_map(generator, token)
                    for token in source_row[2]
                ],
                source_row[3],
            ],
            f"sample row:{generator}",
        )
        sample_rows.append({
            "source_ordinal": source,
            "source_key_id": key_id(source, source_row),
            "source_row": source_row,
            "destination_ordinal": destination,
            "destination_key_id": key_id(destination, destination_row),
            "destination_row": destination_row,
        })
    t_map = {
        chart: (
            "t"
            if (
                (generator == "Jx" and chart in {"E", "W"})
                or (generator == "Jy" and chart in {"N", "S"})
            )
            else "-t"
        )
        for chart in ("E", "W", "N", "S")
    }
    source_chart_dictionary = {
        chart: chart_map(generator, chart)
        for chart in SOURCE_G_CHARTS
    }
    target_formulas = (
        {
            "G[ix,iy]": "G[-ix,iy]",
            "W[ix,iy]": "W[-ix-1,iy]",
        }
        if generator == "Jx"
        else {
            "G[ix,iy]": "G[ix,-iy]",
            "W[ix,iy]": "W[ix,-iy-1]",
        }
    )
    token_dictionary = {
        token: token_map(generator, token)
        for token in ("X-", "X+", "Y-", "Y+")
    }
    outgoing_dictionary = {
        cell: outgoing_map(generator, cell)
        for cell in ("E", "W", "N", "S")
    }
    wall_event_identity = (
        {
            "reflected_axis": "X",
            "source_segment": "x(alpha)=qx+alpha*(hx-qx)",
            "source_wall_equation":
                "alpha=(k-qx)/(hx-qx)",
            "rebased_reflection":
                "(qx,hx,k)->(-qx,-hx,-k)",
            "reflected_wall_equation":
                "(-k-(-qx))/((-hx)-(-qx))=(k-qx)/(hx-qx)",
            "perpendicular_axis": "(qy,hy,k)->(qy,hy,k)",
        }
        if generator == "Jx"
        else {
            "reflected_axis": "Y",
            "source_segment": "y(alpha)=qy+alpha*(hy-qy)",
            "source_wall_equation":
                "alpha=(k-qy)/(hy-qy)",
            "rebased_reflection":
                "(qy,hy,k)->(-qy,-hy,-k)",
            "reflected_wall_equation":
                "(-k-(-qy))/((-hy)-(-qy))=(k-qy)/(hy-qy)",
            "perpendicular_axis": "(qx,hx,k)->(qx,hx,k)",
        }
    )
    target_center_identity = (
        {
            "G[ix,iy] displacement": "(ix,iy)->(-ix,iy)",
            "W[ix,iy] displacement":
                "(ix+1/2+s,iy+1/2)->"
                "(-ix-1+1/2-s,iy+1/2)="
                "(-(ix+1/2+s),iy+1/2)",
            "source_lift_rebasing": "reflected source translated back to G[0,0]",
        }
        if generator == "Jx"
        else {
            "G[ix,iy] displacement": "(ix,iy)->(ix,-iy)",
            "W[ix,iy] displacement":
                "(ix+1/2+s,iy+1/2)->"
                "(ix+1/2+s,-iy-1+1/2)="
                "(ix+1/2+s,-(iy+1/2))",
            "source_lift_rebasing": "reflected source translated back to G[0,0]",
        }
    )
    compact_normal_rows: list[dict[str, Any]] = []
    for source_cell in ("E", "W", "N", "S"):
        destination_cell = outgoing_map(generator, source_cell)
        reflected = reflect_vector_polynomial(
            generator, compact_normal_numerator(source_cell)
        )
        destination_at_minus_z = substitute_minus_z(
            compact_normal_numerator(destination_cell)
        )
        require(
            reflected == destination_at_minus_z,
            f"compact normal reflection:{generator}:{source_cell}",
        )
        compact_normal_rows.append({
            "source_cell": source_cell,
            "destination_cell": destination_cell,
            "source_normal_after_spatial_reflection": reflected,
            "destination_normal_after_z_substitution":
                destination_at_minus_z,
            "z_map": "-z",
            "coefficientwise_identity": True,
        })
    return {
        "generator": generator,
        "physical_reflection": (
            "(x,y,s,p)->(-x,y,-s,-p)"
            if generator == "Jx"
            else "(x,y,s,p)->(x,-y,s,-p)"
        ),
        "ambient_torus_representative_before_source_lift_rebasing": (
            "(x,y,s,p)->(1-x,y,-s,-p)"
            if generator == "Jx"
            else "(x,y,s,p)->(x,1-y,s,-p)"
        ),
        "source_G_deck_rebasing":
            "subtract the reflected source deck vector so G[0,0] is fixed",
        "Gate3_parameter_map": {
            "t_by_source_cell": t_map,
            "p": "-p",
            "s": "-s" if generator == "Jx" else "s",
        },
        "compact_parameter_map": {
            "q": "-q",
            "s": "-s" if generator == "Jx" else "s",
            "z_by_source_cell": {
                chart: "-z" for chart in ("E", "W", "N", "S")
            },
        },
        "compact_normal_reflection_rows": compact_normal_rows,
        "compact_normal_reflection_rows_sha256":
            digest(compact_normal_rows),
        "all_four_compact_normal_identities_coefficientwise": True,
        "source_chart_dictionary": source_chart_dictionary,
        "target_lift_dictionary": target_formulas,
        "target_center_affine_displacement_identity":
            target_center_identity,
        "signed_wall_token_dictionary": token_dictionary,
        "integer_wall_index_dictionary": (
            {"X wall k": "X wall -k", "Y wall k": "Y wall k"}
            if generator == "Jx"
            else {"X wall k": "X wall k", "Y wall k": "Y wall -k"}
        ),
        "integer_wall_crossing_parameter_identity": wall_event_identity,
        "reflected_axis_velocity_multiplier": "-1",
        "perpendicular_axis_velocity_multiplier": "1",
        "token_sign_is_sign_of_axis_displacement": True,
        "token_dictionary_derived_from_velocity_multipliers": True,
        "target_wall_token_affine_consistency_checked": True,
        "event_parameter_and_strict_order_preserved": True,
        "simultaneous_corner_cemetery_preserved": True,
        "roof_formula": "r=number_of_wall_tokens+1",
        "roof_preserved": True,
        "strict_outgoing_chart_dictionary": outgoing_dictionary,
        "half_open_diagonal_owner_rule": "E or W owns; N or S excludes",
        "half_open_owner_set_image": sorted(
            outgoing_map(generator, cell) for cell in {"E", "W"}
        ),
        "half_open_owner_rule_equivariant": True,
        "pair_permutation": {
            "domain_count": pair_row_count,
            "image_count": len(set(pair_permutation)),
            "fixed_count": fixed_pairs,
            "two_cycle_count":
                (SOURCE_G_PAIR_COUNT - fixed_pairs) // 2,
            "image_index_list_sha256": digest(pair_permutation),
            "source_destination_rows_sha256": pair_row_sha256,
        },
        "pattern_permutation": {
            "domain_count": pattern_row_count,
            "image_count": len(set(pattern_permutation)),
            "fixed_count": fixed_patterns,
            "fixed_roof_histogram": {
                str(key): value
                for key, value in sorted(Counter(
                    len(patterns[index]) + 1
                    for index, value in enumerate(pattern_permutation)
                    if index == value
                ).items())
            },
            "two_cycle_count": (PATTERN_COUNT - fixed_patterns) // 2,
            "image_index_list_sha256": digest(pattern_permutation),
            "source_destination_rows_sha256": pattern_row_sha256,
        },
        "source_G_ordinal_permutation": {
            "ordinal_interval": [0, SOURCE_G_KEY_COUNT - 1],
            "domain_count": ordinal_row_count,
            "image_count": len(set(ordinal_permutation)),
            "fixed_count": fixed_ordinals,
            "two_cycle_count":
                (SOURCE_G_KEY_COUNT - fixed_ordinals) // 2,
            "image_ordinal_list_sha256": digest(ordinal_permutation),
            "source_destination_rows_sha256": ordinal_row_sha256,
            "bijective": True,
            "involutive": True,
            "roof_conserved_for_every_ordinal": True,
        },
        "sample_exact_key_transports": sample_rows,
        "sample_exact_key_transports_sha256": digest(sample_rows),
    }, ordinal_permutation


def klein_group(
    jx: list[int],
    jy: list[int],
) -> dict[str, Any]:
    require(len(jx) == len(jy) == SOURCE_G_KEY_COUNT, "Klein sizes")
    jxy = [jx[jy[index]] for index in range(SOURCE_G_KEY_COUNT)]
    require(
        all(
            jx[jx[index]] == index
            and jy[jy[index]] == index
            and jx[jy[index]] == jy[jx[index]]
            and jxy[jxy[index]] == index
            for index in range(SOURCE_G_KEY_COUNT)
        ),
        "Klein relations",
    )
    seen: set[int] = set()
    orbits: list[list[int]] = []
    for index in range(SOURCE_G_KEY_COUNT):
        if index in seen:
            continue
        orbit = sorted({index, jx[index], jy[index], jxy[index]})
        seen.update(orbit)
        orbits.append(orbit)
    histogram = Counter(len(orbit) for orbit in orbits)
    require(
        len(seen) == SOURCE_G_KEY_COUNT
        and histogram == {2: 54, 4: 56118}
        and len(orbits) == 56172
        and sum(map(len, orbits)) == SOURCE_G_KEY_COUNT,
        "Klein orbits",
    )
    count, row_sha256 = stream_digest(
        [index, value] for index, value in enumerate(jxy)
    )
    return {
        "generators": ["Jx", "Jy"],
        "relations": {
            "Jx_squared": "identity",
            "Jy_squared": "identity",
            "Jx_Jy_equals_Jy_Jx": True,
            "JxJy_squared": "identity",
        },
        "relations_checked_on_every_source_G_ordinal": True,
        "JxJy_permutation": {
            "domain_count": count,
            "fixed_count": sum(
                index == value for index, value in enumerate(jxy)
            ),
            "two_cycle_count": SOURCE_G_KEY_COUNT // 2,
            "image_ordinal_list_sha256": digest(jxy),
            "source_destination_rows_sha256": row_sha256,
        },
        "orbit_count": len(orbits),
        "orbit_size_histogram": {
            str(key): value for key, value in sorted(histogram.items())
        },
        "orbit_rows_sha256": digest(orbits),
        "ordinal_conservation": {
            "domain_interval": [0, SOURCE_G_KEY_COUNT - 1],
            "union_of_orbits_is_full_interval": True,
            "distinct_orbits_are_disjoint": True,
            "sum_of_orbit_sizes": sum(map(len, orbits)),
        },
    }


def source_g_census(atlas: dict[str, Any]) -> dict[str, int]:
    rows = [atlas["charts"][chart] for chart in SOURCE_G_CHARTS]
    result = {
        "leaf_count": sum(row["leaf_count"] for row in rows),
        "unique_first": sum(row["counts"]["unique_first"] for row in rows),
        "tangency_graph":
            sum(row["counts"]["tangency_graph"] for row in rows),
        "multi_candidate":
            sum(row["counts"]["multi_candidate"] for row in rows),
    }
    require(
        result == {
            "leaf_count": 66420,
            "unique_first": 21232,
            "tangency_graph": 160,
            "multi_candidate": 45028,
        },
        "source-G census",
    )
    return result


def build_result() -> dict[str, Any]:
    inputs = load_inputs()
    tables = rebuild_registry(inputs["gate5"])
    generator_rows: list[dict[str, Any]] = []
    permutations: dict[str, list[int]] = {}
    for generator in GENERATORS:
        row, permutation = generator_contract(generator, tables)
        generator_rows.append(row)
        permutations[generator] = permutation
    group = klein_group(permutations["Jx"], permutations["Jy"])
    census = source_g_census(inputs["atlas"])

    r169 = inputs["round169"]
    r171 = inputs["round171"]
    r169_keys = r169["source_G_exact_key_coverage_census"]
    require(
        r169["source_G_existing_inputs"]["candidate_exact_key_count"]
        == SOURCE_G_KEY_COUNT
        and r169_keys["global_geometric_exact_key_disposition_count"] == 0
        and r169_keys["keys_without_a_global_geometric_disposition_count"]
        == SOURCE_G_KEY_COUNT
        and r171["Round169_exact_key_guard"][
            "source_G_global_geometric_exact_key_disposition_count"
        ] == 0
        and r171["Round169_exact_key_guard"][
            "source_G_keys_without_global_geometric_disposition_count"
        ] == SOURCE_G_KEY_COUNT,
        "Round169/171 nonpromotion guard",
    )
    source_g_pairs = tables["source_g_pairs"]
    source_g_pair_count, source_g_pair_stream_sha256 = stream_digest(
        [index, list(pair)] for index, pair in enumerate(source_g_pairs)
    )
    require(source_g_pair_count == SOURCE_G_PAIR_COUNT, "pair stream")
    target_relabel_rows = [
        {
            "generator": generator,
            "source_chart": chart,
            "source_target": target,
            "destination_chart": chart_map(generator, chart),
            "destination_target": target_map(generator, target),
        }
        for generator in GENERATORS
        for chart, target in source_g_pairs
    ]

    return {
        "status": STATUS,
        "scope": {
            "source_obstacle": "G",
            "transport_generators": ["Jx", "Jy"],
            "Gate5_source_G_candidate_key_count": SOURCE_G_KEY_COUNT,
            "transport_dictionary_only": True,
            "signed_wall_word_transport_certified": True,
            "target_lift_transport_certified": True,
            "immutable_ordinal_transport_certified": True,
            "strict_outgoing_chart_transport_certified": True,
            "half_open_seam_outgoing_chart_transport_certified": True,
            "dynamic_source_G_leaf_rows_materialized": False,
            "exact_key_dispositions_added": 0,
            "exterior_sheets_excluded": 0,
        },
        "provenance": {
            "dependency_sha256": PINS,
            "Round169_result_sha256": ROUND169_RESULT_SHA256,
            "Round169_verification_result_sha256":
                ROUND169_VERIFICATION_RESULT_SHA256,
            "Round171_result_sha256": ROUND171_RESULT_SHA256,
            "Round171_verification_result_sha256":
                ROUND171_VERIFICATION_RESULT_SHA256,
            "Gate5_candidate_registry_rebuilt_without_importing_source": True,
            "Gate3_reflection_formulas_rederived_from_physical_maps": True,
            "old_artifacts_modified": False,
        },
        "rebuilt_Gate5_source_G_registry": {
            "full_chart_target_pair_count": len(tables["pairs"]),
            "full_chart_target_pair_rows_sha256": digest(tables["pairs"]),
            "crossing_pattern_count": len(tables["patterns"]),
            "crossing_pattern_rows_sha256": digest(tables["patterns"]),
            "source_G_chart_order": list(SOURCE_G_CHARTS),
            "source_G_candidate_count_per_chart": {
                chart: len(candidate_ids(chart))
                for chart in SOURCE_G_CHARTS
            },
            "source_G_chart_target_pair_count": len(source_g_pairs),
            "source_G_chart_target_pair_rows_sha256": digest(source_g_pairs),
            "source_G_indexed_pair_rows_sha256":
                source_g_pair_stream_sha256,
            "source_G_key_count": SOURCE_G_KEY_COUNT,
            "source_G_key_ordinal_interval": [0, SOURCE_G_KEY_COUNT - 1],
            "source_G_keys_are_exact_global_Gate5_ordinal_prefix": True,
            "source_G_key_rows_sha256":
                tables["source_g_key_rows_sha256"],
            "roof_formula": "len(crossing_pattern)+1",
            "target_relabel_rows_count": len(target_relabel_rows),
            "target_relabel_rows_sha256": digest(target_relabel_rows),
        },
        "exact_transport_generators": generator_rows,
        "exact_transport_generators_sha256": digest(generator_rows),
        "Klein_four_action": group,
        "direct_reflected_chart_contracts": [
            {
                "source_direct_chart": "G:E",
                "generator": "Jx",
                "destination_reflected_chart": "G:W",
                "Gate3_reflection_leaf_rows_sha256":
                    "46da8d49fbfc1493e1229bd4bd7c1a9dae9035a286bd97d58484ac312e4a4683",
                "exact_return_signature_transport_ready": True,
                "use_condition":
                    "a dynamic source row must first be materialized and "
                    "bound to its exact official Gate5 key",
            },
            {
                "source_direct_chart": "G:N",
                "generator": "Jy",
                "destination_reflected_chart": "G:S",
                "Gate3_reflection_leaf_rows_sha256":
                    "e91640f12bebd3a49b385aa190a6758f62aa10f1b87135eee5fd833e4a3aa5b9",
                "exact_return_signature_transport_ready": True,
                "use_condition":
                    "a dynamic source row must first be materialized and "
                    "bound to its exact official Gate5 key",
            },
        ],
        "outgoing_chart_contract": {
            "field_is_auxiliary_to_Gate5_word_ordinal": True,
            "strict_chart_transport_is_total_on_E_W_N_S": True,
            "diagonal_seam_rule":
                "E or W owns; N or S excludes",
            "owner_set": ["E", "W"],
            "owner_set_is_invariant_under_Jx_and_Jy": True,
            "duplicate_trace_is_identified_not_added": True,
            "grazing_and_simultaneous_corner_dynamic_typing_added": False,
        },
        "dynamic_row_credit_guard": {
            "source_G_Gate3_census": census,
            "unique_first_leaf_count_available_for_future_materialization":
                census["unique_first"],
            "dynamic_rows_materialized_by_Round173": 0,
            "transported_dynamic_rows_materialized_by_Round173": 0,
            "leaf_dispositions_added_by_Round173": 0,
            "global_geometric_exact_key_dispositions_before_Round173": 0,
            "global_geometric_exact_key_dispositions_after_Round173": 0,
            "keys_without_global_geometric_disposition_after_Round173":
                SOURCE_G_KEY_COUNT,
            "reason":
                "a total dictionary on the candidate-key envelope does not "
                "instantiate a physical owner/wall-word/outgoing-chart row",
        },
        "strict_nonpromotion": {
            "source_G_global_exact_key_dispositions_complete": False,
            "all_disconnected_exterior_sheets_excluded": False,
            "all_chart_seam_grazing_corner_strata_dynamically_typed": False,
            "all_return_signatures_excluded_or_connected": False,
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate":
            "materialize exact owner, wall-word, target lift and outgoing-"
            "chart rows on the 21232 source-G unique-first leaves, use this "
            "dictionary to transport the direct G:E/G:N rows to G:W/G:S, "
            "then refine 45028 multi-candidate leaves and type 160 tangency "
            "graphs plus grazing/seam/corner strata",
    }


def build() -> dict[str, Any]:
    result = build_result()
    return {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def safe_output(path: Path) -> None:
    parent = path.parent
    require(parent.exists() and parent.is_dir(), "output parent")
    require(not parent.is_symlink(), "output parent symlink")
    protected = [
        Path(__file__).resolve(),
        *[(HERE / name).resolve() for name in PINS],
    ]
    candidate = path.resolve(strict=False)
    require(candidate not in protected, "protected output")
    if path.exists() or path.is_symlink():
        require(not path.is_symlink(), "output symlink")
        information = path.stat()
        require(stat.S_ISREG(information.st_mode), "output regular")
        require(information.st_nlink == 1, "output hardlink")
        for item in protected:
            if item.exists():
                require(
                    not os.path.samefile(path, item),
                    "output aliases protected",
                )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    safe_output(arguments.output)
    document = build()
    arguments.output.write_text(
        json.dumps(
            document,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n",
        encoding="utf-8",
    )
    print(document["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
