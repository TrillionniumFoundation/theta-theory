#!/usr/bin/env python3
"""Independent full verifier for the Round174 source-G row materialization.

This program treats the Round174 producer as inert, pinned evidence: it never
imports, executes, parses, or evaluates that source file.  Starting from the
pinned Gate3/Gate5 inputs, it independently rebuilds the G:E and G:N atlases,
performs every bounded rational/Arb recut, applies the pinned Round173 Jx/Jy
dictionary, reconstructs every packed row and every certificate field, and
compares the 109 MiB attachment both as a strict JSON object and byte for byte.

The verification is deliberately fail-closed.  In particular, local 3D
occurrence rows, 2D/1D strata, and rational chart-guard rejections remain
separate ledgers and give no global Gate5 disposition or D02 credit.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import multiprocessing as mp
import os
import stat
import tempfile
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Callable

from flint import arb, ctx, __version__ as FLINT_VERSION

import cm2_gate3_candidate_first_hit_cert as first_hit
import cm2_gate3_eight_cell_symmetry_atlas_cert as atlas


BASE = Path(__file__).resolve().parent
PRODUCER = BASE / (
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization.py"
)
CERTIFICATE = BASE / (
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_"
    "certificate.json"
)
ATTACHMENT = BASE / (
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_"
    "rows.json"
)
OUTPUT = BASE / (
    "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_"
    "verification.json"
)

CERTIFICATE_SCHEMA = (
    "cm2.round174.source-g-unique-first-dynamic-occurrence-materialization.v1"
)
ATTACHMENT_SCHEMA = (
    "cm2.round174.source-g-unique-first-dynamic-occurrence-rows.v1"
)
VERIFICATION_SCHEMA = (
    "cm2.round174.source-g-unique-first-dynamic-occurrence-materialization."
    "verification.v1"
)
CERTIFIED_STATUS = (
    "CERTIFIED_BOUNDED_PARTIAL_SOURCE_G_UNIQUE_FIRST_DYNAMIC_OCCURRENCE_ROWS__"
    "NO_GLOBAL_DISPOSITION_OR_D02_PROMOTION"
)
EXPECTED_PRODUCER_SHA256 = (
    "3d329525dda6697a3a5d2a8227c94bd9c309ea7ebcc4cdd0c7fbe573c267a218"
)
EXPECTED_CERTIFICATE_SHA256 = (
    "10221141c58c044b42e43009beb34ae4705995925a88deaa70ff2eba2ea852c7"
)
EXPECTED_ATTACHMENT_SHA256 = (
    "9edeea2e1033b0dd70dee11a53b0f6aeb21fe74030aeefb60b081a7c420cff54"
)
EXPECTED_CERTIFICATE_RESULT = (
    "d45f05458c42189cf0ebc51e258356d13278ba40845cce80b6a072ffbc8cf09b"
)
EXPECTED_ATTACHMENT_RESULT = (
    "002ca6631edd39c2325c63a1e8f9717d111f4d10c6d2585077d665a0ff128d18"
)
ATLAS_BITS = 192
DYNAMIC_BITS = 256
MAX_RECUT_DEPTH = 6
PATTERN_COUNT = 985
SOURCE_G_KEY_COUNT = 224580
SOURCE_CHARTS = tuple(
    f"{source}:{cell}"
    for source in ("G", "W")
    for cell in ("E", "W", "N", "S")
)

R169P = "cm2_round169_source_g_return_signature_coverage_survey.py"
R169C = "cm2_round169_source_g_return_signature_coverage_survey_certificate.json"
R169V = "cm2_round169_source_g_return_signature_coverage_survey_verifier.py"
R169O = "cm2_round169_source_g_return_signature_coverage_survey_verification.json"
R171P = "cm2_round171_compact_gate3_source_g_coordinate_bridge.py"
R171C = "cm2_round171_compact_gate3_source_g_coordinate_bridge_certificate.json"
R171V = "cm2_round171_compact_gate3_source_g_coordinate_bridge_verifier.py"
R171O = "cm2_round171_compact_gate3_source_g_coordinate_bridge_verification.json"
R173P = "cm2_round173_source_g_exact_return_signature_transport.py"
R173C = "cm2_round173_source_g_exact_return_signature_transport_certificate.json"
R173V = "cm2_round173_source_g_exact_return_signature_transport_verifier.py"
R173O = "cm2_round173_source_g_exact_return_signature_transport_verification.json"
R173M = (
    "cm2-round173-source-g-exact-return-signature-transport-manifest-2026-07-26"
    ".sha256"
)
FHP = "cm2_gate3_candidate_first_hit_cert.py"
FHM = "cm2-gate3-first-hit-atlas-manifest-2026-07-15.json"
GEP = "cm2_gate3_ge_interval_atlas_cert.py"
GEM = "cm2-gate3-ge-interval-atlas-manifest-2026-07-15.json"
G3P = "cm2_gate3_eight_cell_symmetry_atlas_cert.py"
G3M = "cm2-gate3-eight-cell-symmetry-atlas-manifest-2026-07-15.json"
SP = "cm2_gate3_chart_seam_quotient_cert.py"
SV = "cm2_gate3_chart_seam_quotient_verifier.py"
SM = "cm2-gate3-chart-seam-quotient-manifest-2026-07-15.json"
G5P = "cm2_gate5_return_word_three_norm_frontier_cert.py"
G5V = "cm2_gate5_return_word_three_norm_frontier_verifier.py"
G5M = "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"

DEPENDENCIES = {
    R169P: "2be6580fb7d3d47a7ddab05f22d7987ba28d531bb1dd5af5c0082b458e089ee9",
    R169C: "87c5b5f5467aa19b3bafce9e20c10371877012af65937983ced43fcccb22c2fb",
    R169V: "ed5d26a532f184702551da526e5ffbc0feafbf1e8c89eb55d260b15428aaab67",
    R169O: "90c207dd952329d0547ec0440e35cffa57d7b11f98ed17869f3a07df6ce3161f",
    R171P: "bcaba20978ebb5386d64bcf248d254c54c8ac79d9c9c7eb023be278ab7e05c75",
    R171C: "1fb4827b42569d41602765445d0333c76b2ef97615873fc406563ac0e18af7a5",
    R171V: "aee7b3cc3f1468b6a46e7a90e1bb219bd609bddfe54075c6c73e124d98eda7e0",
    R171O: "effdfd4306dbf7bd70df1e9b5ed9166a58dc00a5d333b0f2f2a5f0cb930ccce9",
    R173P: "bdbf794a99dc9276b11b7680818994d63f52fe0e5a857948701f64e8d5d16a0f",
    R173C: "5ff82c5822f543109da0d50c0637d0d2f9148a738b1a21b16878c70e5505cf1a",
    R173V: "eb2b51929719563cd9fe72d180f3f1932a049e983ad1e7a8ec9ac89526bc30f1",
    R173O: "e205367506bc02aa982de074253e5806f07b4358dd3738fb4a0e14476e44ce99",
    R173M: "ba2a1b6eea612e538e3ca70e2916e07469fda38eaef24a751ff862262336f275",
    FHP: "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    FHM: "0c820a5e3481b2c18fabb14d8d0fab7ce454f9a9e68b856bb2a7bf139404f7f4",
    GEP: "ab120f85a263f3cb0697d8a40bc9ed2bf12b361aa7c54940c214b6fd85b17e2b",
    GEM: "d502d0b1c8ef6dba349fa5b7211da4c0a3fcff78bf92a46457cb4f4b64f760f5",
    G3P: "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    G3M: "f8fda665edbb7d8b39ce495188f90ecb2b5ec4384c1eb958949627df167c4987",
    SP: "fa00d4c14ee24b8f3fbc7f345deef13deb272080a886b68d2aa2f9c92a456fe1",
    SV: "3eb5b5525eab0d2e4935374e6d9fa453717de13634613afa579cd1ae30dbcea6",
    SM: "1fb40060336f04f28a7cac19a70abdd3692ced272825b2f1f6b6ae005f00518b",
    G5P: "ddcc250f8700c6a695f96019d9f7824fe98636e20a67685fdc6a3cce77f6d695",
    G5V: "0384acdd1f912b0d4b3bee84ff530358d9693893d1c5c64a1deabaede8e0867b",
    G5M: "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866",
}
R169_RESULT = "8cf83c0ef48aea3a6023546a2df52398241d7baf113e9b78a917c7de4e3d68d6"
R169_VERIFY_RESULT = (
    "4c89a30e89f4fd0b599264a52c8a81f535c4c9df6c60682e6f60594744decdb1"
)
R171_RESULT = "ffac0e2e16829c1a3ffc4783af2c224288265d02cf53c1d041aaf02013b52957"
R171_VERIFY_RESULT = (
    "60e9d4038c63bba14c0bd95478f63840735d8283f9cdfdefb1405ee2ed7defe3"
)
R173_RESULT = "948ab0a8539b08adc96c9493de415b44a5ffb75a1ee3ef47a4742902c211c11f"
R173_VERIFY_RESULT = (
    "047a580eb546cdb3880b93a9d0358e390d7ce418b371612f8e9fc4b0528f4644"
)


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


def qstr(value: Q) -> str:
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def input_guard(path: Path, maximum_bytes: int) -> bytes:
    require(path.parent == BASE, f"path parent:{path.name}")
    require(not path.parent.is_symlink(), f"path parent symlink:{path.name}")
    require(path.exists() and not path.is_symlink(), f"path exists:{path.name}")
    info = path.stat()
    require(stat.S_ISREG(info.st_mode), f"path regular:{path.name}")
    require(info.st_nlink == 1, f"path hardlink:{path.name}")
    require(0 < info.st_size <= maximum_bytes, f"path size:{path.name}")
    return path.read_bytes()


def strict_decode(raw: bytes) -> dict[str, Any]:
    require(
        raw and len(raw) <= 130_000_000,
        "strict JSON size",
    )
    require(
        not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        "strict JSON encoding",
    )

    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in output, f"duplicate key:{key}")
            output[key] = value
        return output

    def no_constant(token: str) -> None:
        raise ValueError(token)

    parsed = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=unique,
        parse_constant=no_constant,
        parse_float=no_constant,
    )

    def walk(value: Any) -> None:
        if type(value) is str:
            require(
                "\x00" not in value
                and not any(
                    0xD800 <= ord(character) <= 0xDFFF
                    for character in value
                ),
                "strict JSON string",
            )
        elif type(value) is list:
            for item in value:
                walk(item)
        elif type(value) is dict:
            for key, item in value.items():
                require(type(key) is str, "strict JSON key")
                walk(key)
                walk(item)
        else:
            require(
                value is None
                or type(value) in {bool, int},
                "strict JSON scalar",
            )

    walk(parsed)
    require(type(parsed) is dict, "strict JSON top-level object")
    return parsed


def strict_load(path: Path, maximum_bytes: int) -> dict[str, Any]:
    return strict_decode(input_guard(path, maximum_bytes))


def unwrap(
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
        document["result_sha256"]
        == result_sha256
        == digest(document["result"]),
        f"result digest:{schema}",
    )
    require(document["result"]["status"] == status, f"status:{schema}")
    return document["result"]


def load_frozen_inputs() -> dict[str, Any]:
    require(FLINT_VERSION == "0.9.0", "python-flint version")
    producer_raw = input_guard(PRODUCER, 200_000)
    require(
        hashlib.sha256(producer_raw).hexdigest() == EXPECTED_PRODUCER_SHA256,
        "inert producer pin",
    )
    # Crucially, producer_raw is never decoded as Python or executed.
    del producer_raw
    for name, expected in DEPENDENCIES.items():
        raw = input_guard(BASE / name, 5_000_000)
        require(hashlib.sha256(raw).hexdigest() == expected, f"pin:{name}")
    r169 = unwrap(
        strict_load(BASE / R169C, 5_000_000),
        "cm2.round169.source-g-return-signature-coverage-survey.v1",
        R169_RESULT,
        "CERTIFIED_SOURCE_G_EXACT_KEY_COVERAGE_DEFICIT_SURVEY__"
        "NO_EXTERIOR_OR_D02_PROMOTION",
    )
    r169v = unwrap(
        strict_load(BASE / R169O, 5_000_000),
        "cm2.round169.source-g-return-signature-coverage-survey.verification.v1",
        R169_VERIFY_RESULT,
        "PASS",
    )
    r171 = unwrap(
        strict_load(BASE / R171C, 5_000_000),
        "cm2.round171.compact-gate3-source-g-coordinate-bridge.v1",
        R171_RESULT,
        "CERTIFIED_COMPACT_TO_GATE3_SOURCE_G_COORDINATE_COVER__"
        "NO_RETURN_KEY_OR_D02_PROMOTION",
    )
    r171v = unwrap(
        strict_load(BASE / R171O, 5_000_000),
        "cm2.round171.compact-gate3-source-g-coordinate-bridge.verification.v1",
        R171_VERIFY_RESULT,
        "PASS",
    )
    r173 = unwrap(
        strict_load(BASE / R173C, 5_000_000),
        "cm2.round173.source-g-exact-return-signature-transport.v1",
        R173_RESULT,
        "CERTIFIED_SOURCE_G_JX_JY_EXACT_RETURN_SIGNATURE_TRANSPORT_DICTIONARY__"
        "NO_DYNAMIC_ROW_OR_D02_PROMOTION",
    )
    r173v = unwrap(
        strict_load(BASE / R173O, 5_000_000),
        "cm2.round173.source-g-exact-return-signature-transport.verification.v1",
        R173_VERIFY_RESULT,
        "PASS",
    )
    require(
        r169v["certificate_result_sha256"] == R169_RESULT
        and r171v["certificate_result_sha256"] == R171_RESULT
        and r173v["certificate_result_sha256"] == R173_RESULT
        and r169v["full_document_exactly_matched"] is True
        and r171v["full_document_exactly_matched"] is True
        and r173v["full_document_exactly_matched"] is True
        and r173v["producer_imported_or_executed"] is False,
        "upstream verifier binding",
    )
    require(
        r169["source_G_exact_key_coverage_census"][
            "global_geometric_exact_key_disposition_count"
        ] == 0
        and r169["source_G_exact_key_coverage_census"][
            "keys_without_a_global_geometric_disposition_count"
        ] == SOURCE_G_KEY_COUNT
        and r171["Round169_exact_key_guard"][
            "source_G_global_geometric_exact_key_disposition_count"
        ] == 0
        and r173["dynamic_row_credit_guard"][
            "dynamic_rows_materialized_by_Round173"
        ] == 0
        and r173["dynamic_row_credit_guard"][
            "global_geometric_exact_key_dispositions_after_Round173"
        ] == 0,
        "upstream no-credit binding",
    )
    gate5 = strict_load(BASE / G5M, 5_000_000)
    gate3 = strict_load(BASE / G3M, 5_000_000)
    first = strict_load(BASE / FHM, 5_000_000)
    seam = strict_load(BASE / SM, 5_000_000)
    registry = gate5["result"]["immutable_candidate_key_registry"]
    require(
        gate5["schema"]
        == "cm2.gate5.return-word-three-norm-frontier.manifest.v1"
        and registry["retained_chart_target_pair_count"] == 448
        and registry["crossing_pattern_count_per_pair"] == PATTERN_COUNT
        and registry["candidate_return_word_key_count"] == 441280
        and registry["complete_physical_operator_block_count"] == 0
        and gate5["verdict"]["gate5"] == "NOT_CERTIFIED",
        "Gate5 frozen frontier",
    )
    require(
        first["schema"] == "cm2.gate3.first-hit-atlas.v1"
        and first["candidate_reduction"]["retained_pair_count"] == 448,
        "Gate3 candidate frontier",
    )
    require(
        gate3["schema"] == "cm2.gate3.eight-cell-symmetry-atlas.v1"
        and gate3["coverage"]["global_leaf_count"] == 143248
        and gate3["charts"]["G:E"]["counts"]["unique_first"] == 5276
        and gate3["charts"]["G:N"]["counts"]["unique_first"] == 5340
        and gate3["charts"]["G:W"]["counts"]["unique_first"] == 5276
        and gate3["charts"]["G:S"]["counts"]["unique_first"] == 5340,
        "Gate3 source-G census",
    )
    require(
        seam["schema"] == "cm2.gate3.chart-seam-quotient.manifest.v1"
        and seam["result"]["unique_half_open_owner_rule"]["diagonal_tie"]
        == "E or W owns; N or S excludes"
        and seam["verdict"]["eight_chart_seam_ownership"] == "CERTIFIED",
        "half-open seam owner",
    )
    return {
        "r169": r169,
        "r171": r171,
        "r173": r173,
        "gate5": gate5,
        "gate3": gate3,
    }


def enumerate_patterns() -> tuple[tuple[str, ...], ...]:
    output: list[tuple[str, ...]] = []
    for x_count in range(5):
        for y_count in range(5):
            total = x_count + y_count
            x_directions = (0,) if x_count == 0 else (-1, 1)
            y_directions = (0,) if y_count == 0 else (-1, 1)
            for x_direction in x_directions:
                for y_direction in y_directions:
                    for x_positions_tuple in itertools.combinations(
                        range(total), x_count
                    ):
                        x_positions = set(x_positions_tuple)
                        x_token = "X+" if x_direction > 0 else "X-"
                        y_token = "Y+" if y_direction > 0 else "Y-"
                        output.append(tuple(
                            x_token if index in x_positions else y_token
                            for index in range(total)
                        ))
    return tuple(output)


def rebuild_registry(gate5: dict[str, Any]) -> dict[str, Any]:
    pairs = tuple(
        (chart, target)
        for chart in SOURCE_CHARTS
        for target in first_hit.candidate_ids(chart)
    )
    patterns = enumerate_patterns()
    require(
        len(pairs) == len(set(pairs)) == 448,
        "independent pair census",
    )
    require(
        len(patterns) == len(set(patterns)) == PATTERN_COUNT
        and Counter(map(len, patterns))
        == {0: 1, 1: 4, 2: 12, 3: 28, 4: 60,
            5: 120, 6: 200, 7: 280, 8: 280},
        "independent grammar census",
    )
    frozen = gate5["result"]
    registry = frozen["immutable_candidate_key_registry"]
    require(
        digest(pairs) == registry["chart_target_pair_rows_sha256"]
        and digest(patterns)
        == frozen["crossing_grammar"]["crossing_pattern_rows_sha256"],
        "independent registry digest",
    )
    stream = hashlib.sha256()
    count = 0
    for chart, target in pairs:
        for pattern in patterns:
            stream.update(canonical(
                [chart, target, list(pattern), len(pattern) + 1]
            ).encode("utf-8"))
            stream.update(b"\n")
            count += 1
    require(
        count == 441280
        and stream.hexdigest()
        == registry["candidate_word_key_rows_sha256"],
        "full registry stream",
    )
    return {
        "pairs": pairs,
        "patterns": patterns,
        "pair_index": {pair: index for index, pair in enumerate(pairs)},
        "pattern_index": {
            pattern: index for index, pattern in enumerate(patterns)
        },
    }


def exact_key(
    chart: str,
    target: str,
    pattern: tuple[str, ...],
    registry: dict[str, Any],
) -> dict[str, Any]:
    pair = (chart, target)
    require(pair in registry["pair_index"], "key pair")
    require(pattern in registry["pattern_index"], "key pattern")
    ordinal = (
        registry["pair_index"][pair] * PATTERN_COUNT
        + registry["pattern_index"][pattern]
    )
    row = [chart, target, list(pattern), len(pattern) + 1]
    return {
        "row": row,
        "ordinal": ordinal,
        "identifier": f"gate5-word:{ordinal:06d}:{digest(row)}",
    }


def build_direct_atlases() -> dict[str, list[Any]]:
    ctx.prec = ATLAS_BITS
    with mp.get_context("fork").Pool(processes=2) as pool:
        atlases = pool.map(atlas.build_atlas, ("G:E", "G:N"))
    return {"G:E": atlases[0], "G:N": atlases[1]}


def audit_atlases(
    direct: dict[str, list[Any]],
    gate3: dict[str, Any],
) -> dict[str, Any]:
    expected = {"G:E": (16580, 5276), "G:N": (16630, 5340)}
    chart_rows: dict[str, Any] = {}
    for chart, leaves in direct.items():
        leaf_rows = [atlas.leaf_row(chart, leaf) for leaf in leaves]
        unique = [leaf for leaf in leaves if leaf.classification == "unique_first"]
        require(
            (len(leaves), len(unique)) == expected[chart]
            and atlas.canonical_digest(leaf_rows)
            == gate3["charts"][chart]["leaf_rows_sha256"],
            f"direct atlas exact rebuild:{chart}",
        )
        chart_rows[chart] = {
            "leaf_count": len(leaves),
            "unique_first_parent_count": len(unique),
            "leaf_rows_sha256": atlas.canonical_digest(leaf_rows),
            "unique_first_leaf_rows_sha256": digest([
                atlas.leaf_row(chart, leaf) for leaf in unique
            ]),
        }
    for source, axis, destination, generator in (
        ("G:E", "vertical", "G:W", "Jx"),
        ("G:N", "horizontal", "G:S", "Jy"),
    ):
        reflected = [
            atlas.reflect_leaf(source, axis, leaf) for leaf in direct[source]
        ]
        reflected.sort(key=lambda leaf: leaf.box.path)
        rows = [atlas.leaf_row(destination, leaf) for leaf in reflected]
        require(
            len(reflected) == gate3["charts"][destination]["leaf_count"]
            and sum(
                leaf.classification == "unique_first" for leaf in reflected
            ) == gate3["charts"][destination]["counts"]["unique_first"]
            and atlas.canonical_digest(rows)
            == gate3["charts"][destination]["leaf_rows_sha256"],
            f"reflected atlas exact rebuild:{destination}",
        )
        chart_rows[destination] = {
            "leaf_count": len(reflected),
            "unique_first_parent_count": sum(
                leaf.classification == "unique_first" for leaf in reflected
            ),
            "leaf_rows_sha256": atlas.canonical_digest(rows),
            "transported_from": source,
            "transport_generator": generator,
        }
    require(
        sum(row["unique_first_parent_count"] for row in chart_rows.values())
        == 21232,
        "all source-G unique-first parent census",
    )
    return chart_rows


def box_values(box: Any) -> list[str]:
    return [
        qstr(box.t0), qstr(box.t1),
        qstr(box.p0), qstr(box.p1),
        qstr(box.s0), qstr(box.s1),
    ]


def volume(box: Any) -> Q:
    return (
        (box.t1 - box.t0)
        * (box.p1 - box.p0)
        * (box.s1 - box.s0)
    )


def rational_chart_class(box: Any) -> str:
    maximum_abs_t = max(abs(box.t0), abs(box.t1))
    minimum_abs_t = (
        Q(0)
        if box.t0 <= 0 <= box.t1
        else min(abs(box.t0), abs(box.t1))
    )
    if 2 * maximum_abs_t * maximum_abs_t < 1:
        return "inside"
    if 2 * minimum_abs_t * minimum_abs_t > 1:
        return "guard"
    return "seam"


def crossing_events(
    start: arb,
    finish: arb,
    axis: str,
) -> tuple[list[tuple[arb, str, int]] | None, list[str]]:
    if not (
        bool(start > -7)
        and bool(start < 7)
        and bool(finish > -7)
        and bool(finish < 7)
    ):
        return None, [f"wall_endpoint_audit_range:{axis}"]
    events: list[tuple[arb, str, int]] = []
    problems: list[str] = []
    for integer_wall in range(-6, 7):
        wall_ball = arb(integer_wall)
        increasing = bool(start < wall_ball) and bool(finish > wall_ball)
        decreasing = bool(start > wall_ball) and bool(finish < wall_ball)
        below = bool(start < wall_ball) and bool(finish < wall_ball)
        above = bool(start > wall_ball) and bool(finish > wall_ball)
        if increasing or decreasing:
            time = (wall_ball - start) / (finish - start)
            if bool(time > 0) and bool(time < 1):
                events.append((
                    time,
                    axis + ("+" if increasing else "-"),
                    integer_wall,
                ))
            else:
                problems.append(
                    f"wall_crossing_time_not_strict:{axis}:{integer_wall}"
                )
        elif not (below or above):
            problems.append(
                f"wall_endpoint_or_count_transition:{axis}:{integer_wall}"
            )
    if len(events) > 4:
        problems.append(f"more_than_four_crossings:{axis}")
    return (None, problems) if problems else (events, [])


def order_events(
    events: list[tuple[arb, str, int]],
) -> tuple[list[list[Any]] | None, list[str]]:
    pool = list(events)
    ordered: list[list[Any]] = []
    while pool:
        strict_minima = [
            index
            for index, (time, _token, _wall) in enumerate(pool)
            if all(
                index == other_index or bool(time < other_time)
                for other_index, (other_time, _other_token, _other_wall)
                in enumerate(pool)
            )
        ]
        if len(strict_minima) != 1:
            return None, ["simultaneous_corner_order"]
        _time, token, wall = pool.pop(strict_minima[0])
        ordered.append([token, wall])
    return ordered, []


def outgoing_cell(nx: arb, ny: arb) -> tuple[str | None, list[str]]:
    dominance = abs(nx) - abs(ny)
    if bool(dominance > 0):
        if bool(nx > 0):
            return "E", []
        if bool(nx < 0):
            return "W", []
        return None, ["outgoing_chart_component_sign"]
    if bool(dominance < 0):
        if bool(ny > 0):
            return "N", []
        if bool(ny < 0):
            return "S", []
        return None, ["outgoing_chart_component_sign"]
    return None, ["outgoing_chart_seam"]


def certify_signature(
    chart: str,
    box: Any,
    target: str,
    registry: dict[str, Any],
) -> tuple[dict[str, Any] | None, list[str]]:
    qx, qy, ux, uy, s, _source_cosine = atlas.geometry(chart, box)
    record = atlas.root_record(chart, box, target)
    if record.classification == "unresolved_discriminant":
        return None, ["target_grazing_or_discriminant"]
    if (
        record.classification != "strict_future_root"
        or record.near is None
        or not bool(record.discriminant > 0)
    ):
        return None, ["selected_root_sign_or_owner"]
    if not bool(record.near < first_hit.arbq(Q(3))):
        return None, ["return_time_not_below_three"]
    radical = record.discriminant.sqrt()
    radius = first_hit.arbq(first_hit.RADIUS[target[0]])
    nx = (-radical * ux + record.transverse * uy) / radius
    ny = (-radical * uy - record.transverse * ux) / radius
    target_object = first_hit.target_by_id(target)
    center_x, center_y = first_hit.target_center(target_object, s)
    hit_x = center_x + radius * nx
    hit_y = center_y + radius * ny
    x_events, x_reasons = crossing_events(qx, hit_x, "X")
    y_events, y_reasons = crossing_events(qy, hit_y, "Y")
    cell, cell_reasons = outgoing_cell(nx, ny)
    reasons = [*x_reasons, *y_reasons, *cell_reasons]
    ordered = None
    if x_events is not None and y_events is not None:
        ordered, order_reasons = order_events(x_events + y_events)
        reasons.extend(order_reasons)
    if reasons:
        return None, sorted(set(reasons))
    assert ordered is not None and cell is not None
    pattern = tuple(event[0] for event in ordered)
    require(
        len(pattern) <= 8
        and sum(token.startswith("X") for token in pattern) <= 4
        and sum(token.startswith("Y") for token in pattern) <= 4,
        "strict word grammar",
    )
    return {
        "target": target,
        "events": ordered,
        "pattern": pattern,
        "roof": len(pattern) + 1,
        "outgoing": cell,
        "target_chart": f"{target[0]}:{cell}",
        "key": exact_key(chart, target, pattern, registry),
    }, []


def bisect(box: Any, axis_index: int) -> tuple[Any, Any]:
    depth = box.depth + 1
    if axis_index == 0:
        middle = (box.t0 + box.t1) / 2
        return (
            atlas.AtlasBox(
                box.t0, middle, box.p0, box.p1, box.s0, box.s1,
                depth, box.path,
            ),
            atlas.AtlasBox(
                middle, box.t1, box.p0, box.p1, box.s0, box.s1,
                depth, box.path,
            ),
        )
    if axis_index == 1:
        middle = (box.p0 + box.p1) / 2
        return (
            atlas.AtlasBox(
                box.t0, box.t1, box.p0, middle, box.s0, box.s1,
                depth, box.path,
            ),
            atlas.AtlasBox(
                box.t0, box.t1, middle, box.p1, box.s0, box.s1,
                depth, box.path,
            ),
        )
    middle = (box.s0 + box.s1) / 2
    return (
        atlas.AtlasBox(
            box.t0, box.t1, box.p0, box.p1, box.s0, middle,
            depth, box.path,
        ),
        atlas.AtlasBox(
            box.t0, box.t1, box.p0, box.p1, middle, box.s1,
            depth, box.path,
        ),
    )


def classify_child(
    chart: str,
    box: Any,
    owner: str,
    registry: dict[str, Any],
) -> tuple[str, Any]:
    chart_class = rational_chart_class(box)
    if chart_class == "guard":
        return "guard", None
    if chart_class == "seam":
        return "source_seam", ["source_chart_seam"]
    signature, reasons = certify_signature(chart, box, owner, registry)
    return ("resolved", signature) if signature is not None else ("residual", reasons)


PARENT_COLUMNS = [
    "parent_id", "chart", "leaf_id", "owner_target", "box",
    "coordinate_volume", "resolved_child_count",
    "resolved_coordinate_volume", "residual_tube_count",
    "residual_coordinate_volume", "guard_rejection_count",
    "guard_rejection_coordinate_volume", "bulk_completion_status",
    "observed_exact_key_count", "observed_exact_key_ordinals_sha256",
    "provenance", "transport_source_parent_id", "transport_generator",
    "source_grazing_boundary_faces",
    "source_chart_seam_half_open_status", "gate3_leaf_row_sha256",
]
RESOLVED_COLUMNS = [
    "row_id", "chart", "parent_id", "refinement_path", "box",
    "coordinate_volume", "owner_target", "ordered_integer_wall_events",
    "wall_crossing_count", "signed_wall_word", "roof", "outgoing_cell",
    "target_chart", "official_key_row", "official_key_ordinal",
    "official_key_id", "ambient_dimension", "physical_open_subset_positive",
    "provenance", "transport_source_row_id", "transport_generator",
]
RESIDUAL_COLUMNS = [
    "row_id", "chart", "parent_id", "refinement_path", "box",
    "coordinate_volume", "reason_labels", "ambient_dimension",
    "whole_parent_credit", "provenance", "transport_source_row_id",
    "transport_generator",
]
GUARD_COLUMNS = [
    "row_id", "chart", "parent_id", "refinement_path", "box",
    "coordinate_volume", "exact_rejection_predicate", "classification",
    "is_CM2_exterior_sheet_exclusion", "is_Gate5_geometric_disposition",
    "provenance", "transport_source_row_id", "transport_generator",
]
STRATUM_COLUMNS = [
    "stratum_id", "chart", "parent_id", "containing_residual_row_id",
    "predicate_label", "equation", "dimension_account",
    "dimension_certification", "existence_certification",
    "half_open_owner_status", "three_dimensional_volume_credit",
    "whole_parent_credit", "provenance", "transport_source_stratum_id",
    "transport_generator",
]


def make_id(prefix: str, payload: Any) -> str:
    return f"round174-{prefix}:{digest(payload)}"


def source_faces(box: Any) -> list[str]:
    faces: list[str] = []
    if box.p0 == -1:
        faces.append("p=-1")
    if box.p1 == 1:
        faces.append("p=+1")
    return faces


def seam_owner(chart: str) -> str:
    return (
        "E_OR_W_HALF_OPEN_OWNER"
        if chart.split(":")[1] in {"E", "W"}
        else "N_OR_S_EXCLUDES_DIAGONAL_TIE"
    )


def resolved_row(
    chart: str,
    parent_id: str,
    path: list[str],
    box: Any,
    signature: dict[str, Any],
) -> dict[str, Any]:
    payload = [
        chart, parent_id, path, box_values(box),
        signature["key"]["identifier"], signature["outgoing"],
    ]
    return {
        "row_id": make_id("resolved-3d", payload),
        "chart": chart,
        "parent_id": parent_id,
        "refinement_path": path,
        "box": box_values(box),
        "coordinate_volume": qstr(volume(box)),
        "owner_target": signature["target"],
        "ordered_integer_wall_events": signature["events"],
        "wall_crossing_count": len(signature["events"]),
        "signed_wall_word": list(signature["pattern"]),
        "roof": signature["roof"],
        "outgoing_cell": signature["outgoing"],
        "target_chart": signature["target_chart"],
        "official_key_row": signature["key"]["row"],
        "official_key_ordinal": signature["key"]["ordinal"],
        "official_key_id": signature["key"]["identifier"],
        "ambient_dimension": 3,
        "physical_open_subset_positive": True,
        "provenance": "DIRECT_256_BIT_ARB_STRICT_CLOSED_ENCLOSURE",
        "transport_source_row_id": None,
        "transport_generator": None,
    }


def residual_row(
    chart: str,
    parent_id: str,
    path: list[str],
    box: Any,
    reasons: list[str],
) -> dict[str, Any]:
    reasons = sorted(set(reasons))
    payload = [chart, parent_id, path, box_values(box), reasons]
    return {
        "row_id": make_id("residual-3d-tube", payload),
        "chart": chart,
        "parent_id": parent_id,
        "refinement_path": path,
        "box": box_values(box),
        "coordinate_volume": qstr(volume(box)),
        "reason_labels": reasons,
        "ambient_dimension": 3,
        "whole_parent_credit": 0,
        "provenance": "DIRECT_BOUNDED_DEPTH_UNRESOLVED_TUBE",
        "transport_source_row_id": None,
        "transport_generator": None,
    }


def guard_row(
    chart: str,
    parent_id: str,
    path: list[str],
    box: Any,
) -> dict[str, Any]:
    payload = [chart, parent_id, path, box_values(box)]
    return {
        "row_id": make_id("chart-guard-rejection", payload),
        "chart": chart,
        "parent_id": parent_id,
        "refinement_path": path,
        "box": box_values(box),
        "coordinate_volume": qstr(volume(box)),
        "exact_rejection_predicate":
            "min_{t in box}|t| gives 2*t^2-1>0",
        "classification": "STRICT_OUTSIDE_THIS_TRUE_DOMINANT_SOURCE_CHART",
        "is_CM2_exterior_sheet_exclusion": False,
        "is_Gate5_geometric_disposition": False,
        "provenance": "DIRECT_EXACT_RATIONAL_CHART_DOMAIN_GUARD",
        "transport_source_row_id": None,
        "transport_generator": None,
    }


def independently_recut_parent(
    chart: str,
    leaf: Any,
    registry: dict[str, Any],
) -> dict[str, Any]:
    require(
        leaf.classification == "unique_first"
        and leaf.owner_target is not None,
        "unique-first input parent",
    )
    leaf_row = atlas.leaf_row(chart, leaf)
    parent_id = make_id("gate3-parent", leaf_row)
    base_width = (
        leaf.box.t1 - leaf.box.t0,
        leaf.box.p1 - leaf.box.p0,
        leaf.box.s1 - leaf.box.s0,
    )
    pending: list[tuple[Any, list[str], tuple[str, Any]]] = [(
        leaf.box,
        [],
        classify_child(chart, leaf.box, leaf.owner_target, registry),
    )]
    resolved: list[dict[str, Any]] = []
    residual: list[dict[str, Any]] = []
    guards: list[dict[str, Any]] = []
    while pending:
        box, path, classification = pending.pop()
        kind, data = classification
        if kind == "resolved":
            resolved.append(resolved_row(chart, parent_id, path, box, data))
            continue
        if kind == "guard":
            guards.append(guard_row(chart, parent_id, path, box))
            continue
        if len(path) >= MAX_RECUT_DEPTH:
            residual.append(residual_row(chart, parent_id, path, box, data))
            continue
        eligible_axes = (0,) if kind == "source_seam" else (0, 1, 2)
        widths = (
            box.t1 - box.t0,
            box.p1 - box.p0,
            box.s1 - box.s0,
        )
        options = []
        for axis_index in eligible_axes:
            children = bisect(box, axis_index)
            child_classes = [
                classify_child(chart, child, leaf.owner_target, registry)
                for child in children
            ]
            released = sum(
                (
                    volume(child)
                    for child, child_class
                    in zip(children, child_classes, strict=True)
                    if child_class[0] in {"resolved", "guard"}
                ),
                Q(0),
            )
            relative_width = widths[axis_index] / base_width[axis_index]
            options.append((
                released, relative_width, -axis_index,
                axis_index, children, child_classes,
            ))
        (
            _released, _relative_width, _negative_axis,
            chosen_axis, chosen_children, chosen_classes,
        ) = max(options, key=lambda option: option[:3])
        axis_name = ("t", "p", "s")[chosen_axis]
        for child_index, (child, child_class) in enumerate(
            zip(chosen_children, chosen_classes, strict=True)
        ):
            pending.append((
                child,
                [*path, f"{axis_name}{child_index}"],
                child_class,
            ))
    resolved.sort(key=lambda row: row["row_id"])
    residual.sort(key=lambda row: row["row_id"])
    guards.sort(key=lambda row: row["row_id"])
    resolved_volume = sum(
        (Q(row["coordinate_volume"]) for row in resolved), Q(0)
    )
    residual_volume = sum(
        (Q(row["coordinate_volume"]) for row in residual), Q(0)
    )
    guard_volume = sum(
        (Q(row["coordinate_volume"]) for row in guards), Q(0)
    )
    require(
        resolved_volume + residual_volume + guard_volume == volume(leaf.box),
        "per-parent exact volume conservation",
    )
    ordinals = sorted({
        row["official_key_ordinal"] for row in resolved
    })
    completion = (
        "COMPLETE_NONEMPTY_REGULAR_3D_BULK_RECUT__"
        "LOWER_DIMENSIONAL_BOUNDARY_FACES_SEPARATE"
        if residual_volume == 0
        else
        "BOUNDED_PARTIAL_NONEMPTY_3D_BULK_RECUT__"
        "POSITIVE_VOLUME_RESIDUAL_TUBES_RETAINED"
    )
    parent = {
        "parent_id": parent_id,
        "chart": chart,
        "leaf_id": leaf.box.path,
        "owner_target": leaf.owner_target,
        "box": box_values(leaf.box),
        "coordinate_volume": qstr(volume(leaf.box)),
        "resolved_child_count": len(resolved),
        "resolved_coordinate_volume": qstr(resolved_volume),
        "residual_tube_count": len(residual),
        "residual_coordinate_volume": qstr(residual_volume),
        "guard_rejection_count": len(guards),
        "guard_rejection_coordinate_volume": qstr(guard_volume),
        "bulk_completion_status": completion,
        "observed_exact_key_count": len(ordinals),
        "observed_exact_key_ordinals_sha256": digest(ordinals),
        "provenance": "DIRECT_GATE3_PARENT_AND_256_BIT_ARB_RECUT",
        "transport_source_parent_id": None,
        "transport_generator": None,
        "source_grazing_boundary_faces": source_faces(leaf.box),
        "source_chart_seam_half_open_status": seam_owner(chart),
        "gate3_leaf_row_sha256": digest(leaf_row),
    }
    return {
        "parent": parent,
        "resolved": resolved,
        "residual": residual,
        "guards": guards,
    }


def mirror_target(generator: str, target_id: str) -> str:
    target = first_hit.target_by_id(target_id)
    if generator == "Jx":
        ix = -target.ix if target.obstacle == "G" else -target.ix - 1
        iy = target.iy
    elif generator == "Jy":
        ix = target.ix
        iy = -target.iy if target.obstacle == "G" else -target.iy - 1
    else:
        raise ValueError(generator)
    return f"{target.obstacle}[{ix},{iy}]"


def mirror_token(generator: str, token: str) -> str:
    if generator == "Jx" and token.startswith("X"):
        return "X+" if token == "X-" else "X-"
    if generator == "Jy" and token.startswith("Y"):
        return "Y+" if token == "Y-" else "Y-"
    return token


def mirror_wall(generator: str, token: str, wall: int) -> int:
    if (
        (generator == "Jx" and token.startswith("X"))
        or (generator == "Jy" and token.startswith("Y"))
    ):
        return -wall
    return wall


def mirror_outgoing(generator: str, cell: str) -> str:
    if generator == "Jx":
        return {"E": "W", "W": "E", "N": "N", "S": "S"}[cell]
    if generator == "Jy":
        return {"E": "E", "W": "W", "N": "S", "S": "N"}[cell]
    raise ValueError(generator)


def mirror_box(generator: str, values: list[str]) -> list[str]:
    t0, t1, p0, p1, s0, s1 = map(Q, values)
    if generator == "Jx":
        reflected = (t0, t1, -p1, -p0, -s1, -s0)
    elif generator == "Jy":
        reflected = (t0, t1, -p1, -p0, s0, s1)
    else:
        raise ValueError(generator)
    return [qstr(value) for value in reflected]


def mirror_reason(generator: str, reason: str) -> str:
    parts = reason.split(":")
    if (
        len(parts) == 3
        and parts[1] in {"X", "Y"}
        and parts[2].lstrip("-").isdigit()
        and (
            (generator == "Jx" and parts[1] == "X")
            or (generator == "Jy" and parts[1] == "Y")
        )
    ):
        parts[2] = str(-int(parts[2]))
        return ":".join(parts)
    return reason


def opposite_grazing_face(face: str) -> str:
    return {"p=-1": "p=+1", "p=+1": "p=-1"}[face]


def independently_transport_parent(
    source_chart: str,
    destination_chart: str,
    generator: str,
    leaf: Any,
    direct: dict[str, Any],
    registry: dict[str, Any],
) -> dict[str, Any]:
    reflection_axis = "vertical" if generator == "Jx" else "horizontal"
    image_leaf = atlas.reflect_leaf(source_chart, reflection_axis, leaf)
    require(
        image_leaf.classification == "unique_first"
        and image_leaf.owner_target
        == mirror_target(generator, leaf.owner_target),
        "transported Gate3 owner",
    )
    image_leaf_row = atlas.leaf_row(destination_chart, image_leaf)
    parent_id = make_id("gate3-parent", image_leaf_row)
    source_parent = direct["parent"]
    resolved: list[dict[str, Any]] = []
    for source_row in direct["resolved"]:
        events = [
            [
                mirror_token(generator, token),
                mirror_wall(generator, token, wall),
            ]
            for token, wall in source_row["ordered_integer_wall_events"]
        ]
        pattern = tuple(event[0] for event in events)
        target = mirror_target(generator, source_row["owner_target"])
        key = exact_key(destination_chart, target, pattern, registry)
        outgoing = mirror_outgoing(generator, source_row["outgoing_cell"])
        require(
            key["row"][3] == source_row["roof"]
            and len(events) == source_row["wall_crossing_count"],
            "transported roof and count",
        )
        payload = [
            destination_chart,
            parent_id,
            source_row["refinement_path"],
            mirror_box(generator, source_row["box"]),
            key["identifier"],
            outgoing,
            source_row["row_id"],
        ]
        row = {
            "row_id": make_id("resolved-3d", payload),
            "chart": destination_chart,
            "parent_id": parent_id,
            "refinement_path": source_row["refinement_path"],
            "box": mirror_box(generator, source_row["box"]),
            "coordinate_volume": source_row["coordinate_volume"],
            "owner_target": target,
            "ordered_integer_wall_events": events,
            "wall_crossing_count": len(events),
            "signed_wall_word": list(pattern),
            "roof": len(pattern) + 1,
            "outgoing_cell": outgoing,
            "target_chart": f"{target[0]}:{outgoing}",
            "official_key_row": key["row"],
            "official_key_ordinal": key["ordinal"],
            "official_key_id": key["identifier"],
            "ambient_dimension": 3,
            "physical_open_subset_positive": True,
            "provenance": "ROUND173_EXACT_ISOMETRIC_TRANSPORT",
            "transport_source_row_id": source_row["row_id"],
            "transport_generator": generator,
        }
        twice_target = mirror_target(generator, target)
        twice_pattern = tuple(
            mirror_token(generator, token) for token in pattern
        )
        twice_key = exact_key(
            source_chart, twice_target, twice_pattern, registry
        )
        require(
            twice_key["identifier"] == source_row["official_key_id"],
            "transport key involution",
        )
        resolved.append(row)
    residual: list[dict[str, Any]] = []
    for source_row in direct["residual"]:
        reasons = sorted(
            mirror_reason(generator, reason)
            for reason in source_row["reason_labels"]
        )
        payload = [
            destination_chart,
            parent_id,
            source_row["refinement_path"],
            mirror_box(generator, source_row["box"]),
            reasons,
            source_row["row_id"],
        ]
        residual.append({
            "row_id": make_id("residual-3d-tube", payload),
            "chart": destination_chart,
            "parent_id": parent_id,
            "refinement_path": source_row["refinement_path"],
            "box": mirror_box(generator, source_row["box"]),
            "coordinate_volume": source_row["coordinate_volume"],
            "reason_labels": reasons,
            "ambient_dimension": 3,
            "whole_parent_credit": 0,
            "provenance": "ROUND173_EXACT_ISOMETRIC_TRANSPORT",
            "transport_source_row_id": source_row["row_id"],
            "transport_generator": generator,
        })
    guards: list[dict[str, Any]] = []
    for source_row in direct["guards"]:
        payload = [
            destination_chart,
            parent_id,
            source_row["refinement_path"],
            mirror_box(generator, source_row["box"]),
            source_row["row_id"],
        ]
        guards.append({
            "row_id": make_id("chart-guard-rejection", payload),
            "chart": destination_chart,
            "parent_id": parent_id,
            "refinement_path": source_row["refinement_path"],
            "box": mirror_box(generator, source_row["box"]),
            "coordinate_volume": source_row["coordinate_volume"],
            "exact_rejection_predicate":
                "min_{t in box}|t| gives 2*t^2-1>0",
            "classification": "STRICT_OUTSIDE_THIS_TRUE_DOMINANT_SOURCE_CHART",
            "is_CM2_exterior_sheet_exclusion": False,
            "is_Gate5_geometric_disposition": False,
            "provenance": "ROUND173_EXACT_ISOMETRIC_TRANSPORT",
            "transport_source_row_id": source_row["row_id"],
            "transport_generator": generator,
        })
    resolved.sort(key=lambda row: row["row_id"])
    residual.sort(key=lambda row: row["row_id"])
    guards.sort(key=lambda row: row["row_id"])
    ordinals = sorted({
        row["official_key_ordinal"] for row in resolved
    })
    parent = {
        "parent_id": parent_id,
        "chart": destination_chart,
        "leaf_id": image_leaf.box.path,
        "owner_target": image_leaf.owner_target,
        "box": box_values(image_leaf.box),
        "coordinate_volume": source_parent["coordinate_volume"],
        "resolved_child_count": len(resolved),
        "resolved_coordinate_volume":
            source_parent["resolved_coordinate_volume"],
        "residual_tube_count": len(residual),
        "residual_coordinate_volume":
            source_parent["residual_coordinate_volume"],
        "guard_rejection_count": len(guards),
        "guard_rejection_coordinate_volume":
            source_parent["guard_rejection_coordinate_volume"],
        "bulk_completion_status": source_parent["bulk_completion_status"],
        "observed_exact_key_count": len(ordinals),
        "observed_exact_key_ordinals_sha256": digest(ordinals),
        "provenance": "ROUND173_EXACT_ISOMETRIC_TRANSPORT",
        "transport_source_parent_id": source_parent["parent_id"],
        "transport_generator": generator,
        "source_grazing_boundary_faces": sorted(
            opposite_grazing_face(face)
            for face in source_parent["source_grazing_boundary_faces"]
        ),
        "source_chart_seam_half_open_status": seam_owner(destination_chart),
        "gate3_leaf_row_sha256": digest(image_leaf_row),
    }
    require(
        parent["owner_target"]
        == mirror_target(generator, source_parent["owner_target"])
        and parent["coordinate_volume"] == qstr(volume(image_leaf.box)),
        "transported parent exact binding",
    )
    return {
        "parent": parent,
        "resolved": resolved,
        "residual": residual,
        "guards": guards,
    }


def predicate_row(reason: str) -> tuple[str, str, str, str]:
    if reason == "source_chart_seam":
        return (
            "source_chart_seam",
            "2*t^2-1=0",
            "EXACT_DIMENSION_2_GRAPH",
            "CERTIFIED_PRESENT_IN_CROSS_SEAM_TUBE",
        )
    if reason == "outgoing_chart_seam":
        return (
            "outgoing_chart_seam",
            "target_normal_x^2-target_normal_y^2=0",
            "NOMINAL_DIMENSION_2_ANALYTIC_PREDICATE",
            "EXISTENCE_AND_REGULARITY_NOT_PROMOTED_FROM_INTERVAL_OVERWRAP",
        )
    if reason == "simultaneous_corner_order":
        return (
            "simultaneous_corner",
            "alpha_X_wall-alpha_Y_wall=0 after denominator clearing",
            "NOMINAL_DIMENSION_2_ANALYTIC_PREDICATE",
            "EXISTENCE_AND_REGULARITY_NOT_PROMOTED_FROM_INTERVAL_OVERWRAP",
        )
    if reason == "target_grazing_or_discriminant":
        return (
            "target_grazing",
            "target_discriminant=0",
            "NOMINAL_DIMENSION_2_ANALYTIC_PREDICATE",
            "EXISTENCE_AND_REGULARITY_NOT_PROMOTED_FROM_INTERVAL_OVERWRAP",
        )
    if reason.startswith("wall_endpoint_or_count_transition:"):
        _kind, axis, wall = reason.split(":")
        return (
            "integer_wall_endpoint",
            f"(source_{axis.lower()}-{wall})*"
            f"(target_{axis.lower()}-{wall})=0",
            "UNION_OF_NOMINAL_DIMENSION_2_ANALYTIC_PREDICATES",
            "EXISTENCE_AND_REGULARITY_NOT_PROMOTED_FROM_INTERVAL_OVERWRAP",
        )
    if reason.startswith("wall_crossing_time_not_strict:"):
        _kind, axis, wall = reason.split(":")
        return (
            "integer_wall_crossing_endpoint",
            f"alpha_{axis}_{wall}*(1-alpha_{axis}_{wall})=0",
            "UNION_OF_NOMINAL_DIMENSION_2_ANALYTIC_PREDICATES",
            "EXISTENCE_AND_REGULARITY_NOT_PROMOTED_FROM_INTERVAL_OVERWRAP",
        )
    if reason.startswith("wall_endpoint_audit_range:"):
        return (
            "wall_audit_range",
            "one flight endpoint reaches the finite wall audit boundary",
            "DIMENSION_NOT_CERTIFIED",
            "NOT_CERTIFIED",
        )
    return (
        "root_chart_or_grammar_boundary",
        reason,
        "NOMINAL_DIMENSION_2_BOUNDARY_PREDICATE",
        "EXISTENCE_AND_REGULARITY_NOT_PROMOTED_FROM_INTERVAL_OVERWRAP",
    )


def stratum_row(
    *,
    chart: str,
    parent_id: str,
    residual_id: str | None,
    identity_payload: Any,
    predicate_label: str,
    equation: str,
    dimension_account: str,
    dimension_certification: str,
    existence_certification: str,
    half_open_owner_status: str,
    provenance: str,
    source_id: str | None,
    generator: str | None,
) -> dict[str, Any]:
    return {
        "stratum_id": make_id("stratum", identity_payload),
        "chart": chart,
        "parent_id": parent_id,
        "containing_residual_row_id": residual_id,
        "predicate_label": predicate_label,
        "equation": equation,
        "dimension_account": dimension_account,
        "dimension_certification": dimension_certification,
        "existence_certification": existence_certification,
        "half_open_owner_status": half_open_owner_status,
        "three_dimensional_volume_credit": 0,
        "whole_parent_credit": 0,
        "provenance": provenance,
        "transport_source_stratum_id": source_id,
        "transport_generator": generator,
    }


def independently_build_strata(result: dict[str, Any]) -> list[dict[str, Any]]:
    parent = result["parent"]
    chart = parent["chart"]
    parent_id = parent["parent_id"]
    generator = parent["transport_generator"]
    source_parent = parent["transport_source_parent_id"]
    provenance = (
        "ROUND173_EXACT_ISOMETRIC_TRANSPORT"
        if generator is not None
        else "DIRECT_DIMENSION_SAFE_LEDGER"
    )
    rows: list[dict[str, Any]] = []
    faces = parent["source_grazing_boundary_faces"]
    for face in faces:
        source_face = (
            opposite_grazing_face(face) if generator is not None else None
        )
        source_id = (
            make_id("stratum", [
                source_parent, "source_grazing", source_face
            ])
            if source_parent is not None and source_face is not None
            else None
        )
        rows.append(stratum_row(
            chart=chart,
            parent_id=parent_id,
            residual_id=None,
            identity_payload=[parent_id, "source_grazing", face],
            predicate_label="source_grazing",
            equation=face,
            dimension_account="EXACT_DIMENSION_2_BOUNDARY_FACE",
            dimension_certification="CERTIFIED",
            existence_certification="CERTIFIED_PRESENT",
            half_open_owner_status="PHYSICAL_BOUNDARY_FACE",
            provenance=provenance,
            source_id=source_id,
            generator=generator,
        ))
    seam_residuals = [
        row for row in result["residual"]
        if "source_chart_seam" in row["reason_labels"]
    ]
    if seam_residuals:
        source_id = (
            make_id("stratum", [source_parent, "source_chart_seam"])
            if source_parent is not None
            else None
        )
        rows.append(stratum_row(
            chart=chart,
            parent_id=parent_id,
            residual_id=None,
            identity_payload=[parent_id, "source_chart_seam"],
            predicate_label="source_chart_seam",
            equation="2*t^2-1=0",
            dimension_account="EXACT_DIMENSION_2_GRAPH",
            dimension_certification="CERTIFIED",
            existence_certification="CERTIFIED_PRESENT",
            half_open_owner_status=seam_owner(chart),
            provenance=provenance,
            source_id=source_id,
            generator=generator,
        ))
        for face in faces:
            source_face = (
                opposite_grazing_face(face) if generator is not None else None
            )
            source_id = (
                make_id("stratum", [
                    source_parent,
                    "source_chart_seam_source_grazing_intersection",
                    source_face,
                ])
                if source_parent is not None and source_face is not None
                else None
            )
            rows.append(stratum_row(
                chart=chart,
                parent_id=parent_id,
                residual_id=None,
                identity_payload=[
                    parent_id,
                    "source_chart_seam_source_grazing_intersection",
                    face,
                ],
                predicate_label=
                    "source_chart_seam_source_grazing_intersection",
                equation=f"2*t^2-1=0 AND {face}",
                dimension_account="EXACT_DIMENSION_1_INTERSECTION",
                dimension_certification="CERTIFIED",
                existence_certification="CERTIFIED_PRESENT",
                half_open_owner_status=seam_owner(chart),
                provenance=provenance,
                source_id=source_id,
                generator=generator,
            ))
    for residual in result["residual"]:
        reasons = [
            reason for reason in residual["reason_labels"]
            if reason != "source_chart_seam"
        ]
        for reason in reasons:
            label, equation, dimension, existence = predicate_row(reason)
            if generator is None:
                source_id = None
            else:
                source_reason = mirror_reason(generator, reason)
                source_id = make_id("stratum", [
                    residual["transport_source_row_id"], source_reason
                ])
            rows.append(stratum_row(
                chart=chart,
                parent_id=parent_id,
                residual_id=residual["row_id"],
                identity_payload=[residual["row_id"], reason],
                predicate_label=label,
                equation=equation,
                dimension_account=dimension,
                dimension_certification=(
                    "DEFERRED"
                    if "NOMINAL" in dimension or "UNION" in dimension
                    else "NOT_CERTIFIED"
                ),
                existence_certification=existence,
                half_open_owner_status=(
                    "E_OR_W_OWNS_BY_SIGN_OF_TARGET_NORMAL_X"
                    if label == "outgoing_chart_seam"
                    else "NOT_APPLICABLE"
                ),
                provenance=provenance,
                source_id=source_id,
                generator=generator,
            ))
        for reason_a, reason_b in itertools.combinations(reasons, 2):
            ordered_reasons = sorted([reason_a, reason_b])
            if generator is None:
                source_id = None
            else:
                source_reasons = sorted([
                    mirror_reason(generator, reason_a),
                    mirror_reason(generator, reason_b),
                ])
                source_id = make_id("stratum", [
                    residual["transport_source_row_id"],
                    "candidate-intersection",
                    source_reasons,
                ])
            rows.append(stratum_row(
                chart=chart,
                parent_id=parent_id,
                residual_id=residual["row_id"],
                identity_payload=[
                    residual["row_id"],
                    "candidate-intersection",
                    ordered_reasons,
                ],
                predicate_label="candidate_pair_intersection",
                equation=" AND ".join(ordered_reasons),
                dimension_account=
                    "NOMINAL_DIMENSION_1_INTERSECTION_IF_TRANSVERSE",
                dimension_certification="DEFERRED",
                existence_certification="NOT_CERTIFIED",
                half_open_owner_status="NOT_APPLICABLE",
                provenance=provenance,
                source_id=source_id,
                generator=generator,
            ))
    rows.sort(key=lambda row: row["stratum_id"])
    return rows


def independently_build_all_rows(
    direct_atlases: dict[str, list[Any]],
    registry: dict[str, Any],
) -> dict[str, list[dict[str, Any]]]:
    output: dict[str, list[dict[str, Any]]] = {
        "parents": [],
        "resolved": [],
        "residual": [],
        "guards": [],
        "strata": [],
    }
    for source, destination, generator in (
        ("G:E", "G:W", "Jx"),
        ("G:N", "G:S", "Jy"),
    ):
        for leaf in direct_atlases[source]:
            if leaf.classification != "unique_first":
                continue
            direct = independently_recut_parent(source, leaf, registry)
            transported = independently_transport_parent(
                source, destination, generator, leaf, direct, registry
            )
            for result in (direct, transported):
                output["parents"].append(result["parent"])
                output["resolved"].extend(result["resolved"])
                output["residual"].extend(result["residual"])
                output["guards"].extend(result["guards"])
                output["strata"].extend(independently_build_strata(result))
    output["parents"].sort(key=lambda row: (row["chart"], row["leaf_id"]))
    output["resolved"].sort(key=lambda row: row["row_id"])
    output["residual"].sort(key=lambda row: row["row_id"])
    output["guards"].sort(key=lambda row: row["row_id"])
    output["strata"].sort(key=lambda row: row["stratum_id"])
    require(
        len(output["parents"]) == 21232
        and len({row["parent_id"] for row in output["parents"]}) == 21232
        and len({row["row_id"] for row in output["resolved"]})
        == len(output["resolved"])
        and len({row["row_id"] for row in output["residual"]})
        == len(output["residual"])
        and len({row["row_id"] for row in output["guards"]})
        == len(output["guards"])
        and len({row["stratum_id"] for row in output["strata"]})
        == len(output["strata"]),
        "independent unique row IDs",
    )
    require(
        2 * sum(
            row["transport_generator"] is None for row in output["resolved"]
        ) == len(output["resolved"])
        and 2 * sum(
            row["transport_generator"] is None for row in output["residual"]
        ) == len(output["residual"])
        and 2 * sum(
            row["transport_generator"] is None for row in output["guards"]
        ) == len(output["guards"]),
        "direct/reflected row count involution",
    )
    return output


def packed_row(columns: list[str], row: dict[str, Any]) -> list[Any]:
    require(set(row) == set(columns), "packed row exact keys")
    return [row[column] for column in columns]


def independently_pack_attachment(
    rows: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    packed = {
        "parent_rows": [
            packed_row(PARENT_COLUMNS, row) for row in rows["parents"]
        ],
        "resolved_3d_occurrence_rows": [
            packed_row(RESOLVED_COLUMNS, row) for row in rows["resolved"]
        ],
        "residual_3d_tube_rows": [
            packed_row(RESIDUAL_COLUMNS, row) for row in rows["residual"]
        ],
        "chart_guard_rejection_rows": [
            packed_row(GUARD_COLUMNS, row) for row in rows["guards"]
        ],
        "lower_dimensional_stratum_rows": [
            packed_row(STRATUM_COLUMNS, row) for row in rows["strata"]
        ],
    }
    result = {
        "row_column_schemas": {
            "parent_rows": PARENT_COLUMNS,
            "resolved_3d_occurrence_rows": RESOLVED_COLUMNS,
            "residual_3d_tube_rows": RESIDUAL_COLUMNS,
            "chart_guard_rejection_rows": GUARD_COLUMNS,
            "lower_dimensional_stratum_rows": STRATUM_COLUMNS,
        },
        **packed,
        "table_census_and_sha256": {
            name: {
                "row_count": len(table),
                "rows_sha256": digest(table),
            }
            for name, table in packed.items()
        },
    }
    return {
        "schema": ATTACHMENT_SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def sum_fraction(rows: list[dict[str, Any]], field: str) -> Q:
    return sum((Q(row[field]) for row in rows), Q(0))


def independently_compute_statistics(
    rows: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    parents = rows["parents"]
    resolved = rows["resolved"]
    residual = rows["residual"]
    guards = rows["guards"]
    strata = rows["strata"]
    parent_volume = sum_fraction(parents, "coordinate_volume")
    resolved_volume = sum_fraction(resolved, "coordinate_volume")
    residual_volume = sum_fraction(residual, "coordinate_volume")
    guard_volume = sum_fraction(guards, "coordinate_volume")
    require(
        resolved_volume + residual_volume + guard_volume == parent_volume,
        "independent global exact volume conservation",
    )
    completed = [
        row for row in parents if row["residual_coordinate_volume"] == "0"
    ]
    partial = [
        row for row in parents if Q(row["residual_coordinate_volume"]) > 0
    ]
    require(
        completed and partial and len(completed) + len(partial) == 21232,
        "complete/partial split",
    )
    observed_ids = sorted({
        row["official_key_id"] for row in resolved
    })
    observed_ordinals = sorted({
        row["official_key_ordinal"] for row in resolved
    })
    direct_resolved = [
        row for row in resolved if row["transport_generator"] is None
    ]
    direct_ids = sorted({
        row["official_key_id"] for row in direct_resolved
    })
    direct_ordinals = sorted({
        row["official_key_ordinal"] for row in direct_resolved
    })
    require(
        len(observed_ids) == len(observed_ordinals)
        and len(direct_ids) == len(direct_ordinals),
        "key identifier/ordinal bijection",
    )
    fully_closed_regular = [
        row for row in completed if not row["source_grazing_boundary_faces"]
    ]
    return {
        "parent_count": len(parents),
        "completed_nonempty_3d_bulk_parent_count": len(completed),
        "bounded_partial_nonempty_parent_count": len(partial),
        "fully_closed_regular_parent_count": len(fully_closed_regular),
        "parent_chart_histogram": dict(sorted(
            Counter(row["chart"] for row in parents).items()
        )),
        "completed_parent_chart_histogram": dict(sorted(
            Counter(row["chart"] for row in completed).items()
        )),
        "partial_parent_chart_histogram": dict(sorted(
            Counter(row["chart"] for row in partial).items()
        )),
        "parent_coordinate_volume": qstr(parent_volume),
        "resolved_3d_coordinate_volume": qstr(resolved_volume),
        "positive_volume_residual_tube_coordinate_volume":
            qstr(residual_volume),
        "chart_guard_rejection_coordinate_volume": qstr(guard_volume),
        "volume_conservation_exact": True,
        "resolved_3d_occurrence_row_count": len(resolved),
        "residual_3d_tube_row_count": len(residual),
        "chart_guard_rejection_row_count": len(guards),
        "lower_dimensional_stratum_row_count": len(strata),
        "direct_resolved_3d_occurrence_row_count": len(direct_resolved),
        "transported_resolved_3d_occurrence_row_count":
            len(resolved) - len(direct_resolved),
        "observed_exact_key_count": len(observed_ids),
        "observed_exact_key_ids_sha256": digest(observed_ids),
        "observed_exact_key_ordinals_sha256": digest(observed_ordinals),
        "direct_observed_exact_key_count": len(direct_ids),
        "direct_observed_exact_key_ids_sha256": digest(direct_ids),
        "direct_observed_exact_key_ordinals_sha256": digest(direct_ordinals),
        "occurrence_row_chart_histogram": dict(sorted(
            Counter(row["chart"] for row in resolved).items()
        )),
        "wall_crossing_count_histogram": {
            str(key): value
            for key, value in sorted(
                Counter(
                    row["wall_crossing_count"] for row in resolved
                ).items()
            )
        },
        "roof_histogram": {
            str(key): value
            for key, value in sorted(
                Counter(row["roof"] for row in resolved).items()
            )
        },
        "target_outgoing_chart_histogram": dict(sorted(
            Counter(row["target_chart"] for row in resolved).items()
        )),
        "residual_reason_histogram": dict(sorted(
            Counter(
                reason
                for row in residual
                for reason in row["reason_labels"]
            ).items()
        )),
        "stratum_predicate_histogram": dict(sorted(
            Counter(row["predicate_label"] for row in strata).items()
        )),
        "stratum_dimension_account_histogram": dict(sorted(
            Counter(row["dimension_account"] for row in strata).items()
        )),
    }


def expected_certificate_result(
    inputs: dict[str, Any],
    chart_rows: dict[str, Any],
    statistics: dict[str, Any],
    attachment: dict[str, Any],
    attachment_file_sha256: str,
) -> dict[str, Any]:
    require(
        statistics["parent_count"] == 21232
        and statistics["completed_nonempty_3d_bulk_parent_count"] == 17392
        and statistics["bounded_partial_nonempty_parent_count"] == 3840
        and statistics["resolved_3d_occurrence_row_count"] == 72500
        and statistics["residual_3d_tube_row_count"] == 62012
        and statistics["lower_dimensional_stratum_row_count"] == 62696
        and statistics["observed_exact_key_count"] == 116,
        "required independently rebuilt census",
    )
    generators = inputs["r173"]["exact_transport_generators"]
    require(
        [row["generator"] for row in generators] == ["Jx", "Jy"]
        and all(
            row["source_G_ordinal_permutation"]["bijective"] is True
            and row["source_G_ordinal_permutation"]["involutive"] is True
            for row in generators
        ),
        "Round173 exact transport contract",
    )
    return {
        "status": CERTIFIED_STATUS,
        "scope": {
            "source_obstacle": "G",
            "Gate3_unique_first_parent_count": 21232,
            "direct_parent_charts": ["G:E", "G:N"],
            "transported_parent_charts": ["G:W", "G:S"],
            "dynamic_materialization_kind":
                "bounded adaptive positive-3D occurrence rows",
            "maximum_additional_dyadic_refine_depth": MAX_RECUT_DEPTH,
            "all_unique_first_parents_audited": True,
            "all_unique_first_parents_fully_materialized": False,
            "global_geometric_exact_key_dispositions_added": 0,
            "CM2_exterior_sheet_exclusions_added": 0,
        },
        "provenance": {
            "dependency_sha256": DEPENDENCIES,
            "python_flint_version": FLINT_VERSION,
            "Gate3_atlas_precision_bits": ATLAS_BITS,
            "dynamic_recut_precision_bits": DYNAMIC_BITS,
            "Round169_result_sha256": R169_RESULT,
            "Round169_verification_result_sha256": R169_VERIFY_RESULT,
            "Round171_result_sha256": R171_RESULT,
            "Round171_verification_result_sha256": R171_VERIFY_RESULT,
            "Round173_result_sha256": R173_RESULT,
            "Round173_verification_result_sha256": R173_VERIFY_RESULT,
            "old_artifacts_modified": False,
        },
        "independent_direct_Gate3_rebuild": {
            "chart_rows": chart_rows,
            "direct_G_E_unique_first_parent_count": 5276,
            "direct_G_N_unique_first_parent_count": 5340,
            "transported_G_W_unique_first_parent_count": 5276,
            "transported_G_S_unique_first_parent_count": 5340,
            "direct_parent_count": 10616,
            "transported_parent_count": 10616,
            "all_source_G_parent_count": 21232,
            "direct_atlases_rebuilt_from_pinned_source_at_192_bits": True,
            "reflected_atlas_leaf_rows_rebound_to_pinned_digests": True,
        },
        "adaptive_recut_contract": {
            "parent_owner_inheritance":
                "pinned unique-first owner remains strict on every child",
            "strict_cell_requirements": [
                "selected non-grazing near root positive and below 3",
                "source and target flight endpoints off every integer wall",
                "at most four strict crossings per coordinate axis",
                "all X/Y wall-event times in one strict total order",
                "signed wall word in the frozen 985-pattern grammar",
                "strict target-normal outgoing chart",
                "exact target lift, roof, Gate5 ordinal and key ID",
            ],
            "source_chart_domain_test": "exact rational sign of 2*t^2-1",
            "source_chart_diagonal_half_open_rule":
                "E or W owns; N or S excludes",
            "adaptive_axis_choice":
                "try every eligible dyadic t/p/s bisection; maximize exact "
                "child volume immediately released as strict occurrence or "
                "guard rejection; tie-break by largest parent-relative "
                "width then t,p,s",
            "cross_source_chart_seam_forces_t_bisection": True,
            "bounded_depth_fail_closed": True,
            "positive_volume_residual_tubes_retained": True,
        },
        "materialization_census": statistics,
        "dimension_safe_ledger": {
            "resolved_and_residual_bulk_rows_ambient_dimension": 3,
            "source_grazing_faces_exact_dimension": 2,
            "source_chart_seam_graphs_exact_dimension": 2,
            "source_chart_seam_source_grazing_intersections_exact_dimension":
                1,
            "wall_endpoint_outgoing_seam_corner_target_grazing_predicates":
                "separate nominal 2D rows; existence/regularity deferred "
                "when interval overwrap alone does not prove a graph",
            "candidate_pair_intersections":
                "separate nominal 1D rows; existence/transversality deferred",
            "lower_dimensional_row_three_dimensional_volume_credit": 0,
            "lower_dimensional_row_whole_parent_credit": 0,
            "residual_tube_whole_parent_credit": 0,
            "graph_to_whole_parent_promotion_forbidden": True,
            "chart_guard_rejection_is_not_CM2_exterior_sheet_exclusion": True,
            "chart_guard_rejection_is_not_Gate5_geometric_disposition": True,
        },
        "Round173_transport_application": {
            "G_E_to_G_W_generator": "Jx",
            "G_N_to_G_S_generator": "Jy",
            "source_chart_target_lift_signed_wall_wall_index_roof_ordinal_and_outgoing_chart_transported":
                True,
            "every_transported_key_checked_by_official_registry_reconstruction":
                True,
            "every_transported_key_checked_involutively": True,
            "direct_and_transported_resolved_row_counts_equal": True,
            "direct_and_transported_residual_row_counts_equal": True,
            "direct_and_transported_guard_row_counts_equal": True,
        },
        "observed_occurrence_vs_global_disposition": {
            "observed_dynamic_occurrence_rows_are_positive_local_3D_witnesses":
                True,
            "observed_exact_key_count": statistics["observed_exact_key_count"],
            "global_geometric_exact_key_disposition_count_before_Round174": 0,
            "global_geometric_exact_key_disposition_count_after_Round174": 0,
            "keys_without_global_geometric_disposition_after_Round174":
                SOURCE_G_KEY_COUNT,
            "reason":
                "local nonempty occurrence rows neither connect every fibre "
                "of a key nor globally exclude its complement",
        },
        "row_attachment": {
            "path": ATTACHMENT.name,
            "schema": ATTACHMENT_SCHEMA,
            "file_sha256": attachment_file_sha256,
            "result_sha256": attachment["result_sha256"],
            "table_census_and_sha256":
                attachment["result"]["table_census_and_sha256"],
            "full_attachment_rows_materialized": True,
        },
        "strict_nonpromotion": {
            "all_21232_unique_first_parents_fully_materialized": False,
            "all_lower_dimensional_strata_typed": False,
            "source_G_global_exact_key_dispositions_complete": False,
            "all_disconnected_exterior_sheets_excluded": False,
            "all_return_signatures_excluded_or_connected": False,
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "next_core_gate":
            "resolve the positive-volume Round174 residual tubes with exact "
            "normal forms for outgoing seams, integer-wall endpoint/order "
            "changes and simultaneous corners; materialize their 2D graphs "
            "and 1D intersections without bulk promotion, then address the "
            "45028 source-G multi-candidate parents and 160 tangency graphs",
    }


def physical_ledger_audit(
    rows: dict[str, list[dict[str, Any]]],
    statistics: dict[str, Any],
) -> dict[str, Any]:
    parents = rows["parents"]
    resolved = rows["resolved"]
    residual = rows["residual"]
    guards = rows["guards"]
    strata = rows["strata"]
    for row in guards:
        t0, t1 = map(Q, row["box"][:2])
        minimum_abs = (
            Q(0) if t0 <= 0 <= t1 else min(abs(t0), abs(t1))
        )
        require(
            2 * minimum_abs * minimum_abs > 1,
            "every rational guard is strictly outside 2t^2=1",
        )
        require(
            row["is_CM2_exterior_sheet_exclusion"] is False
            and row["is_Gate5_geometric_disposition"] is False,
            "guard no-credit flags",
        )
    require(
        all(row["ambient_dimension"] == 3 for row in resolved)
        and all(
            row["ambient_dimension"] == 3
            and row["whole_parent_credit"] == 0
            for row in residual
        ),
        "3D occurrence/residual dimensional account",
    )
    require(
        all(
            row["three_dimensional_volume_credit"] == 0
            and row["whole_parent_credit"] == 0
            for row in strata
        ),
        "all lower-dimensional rows have zero bulk credit",
    )
    exact_dimensions = Counter(
        row["dimension_account"] for row in strata
    )
    require(
        exact_dimensions
        == {
            "EXACT_DIMENSION_2_BOUNDARY_FACE": 12,
            "EXACT_DIMENSION_2_GRAPH": 472,
            "NOMINAL_DIMENSION_1_INTERSECTION_IF_TRANSVERSE": 336,
            "NOMINAL_DIMENSION_2_ANALYTIC_PREDICATE": 34188,
            "UNION_OF_NOMINAL_DIMENSION_2_ANALYTIC_PREDICATES": 27688,
        },
        "2D/1D stratum dimensional split",
    )
    # A source seam is a graph 2*t^2=1, never a 3D leaf.  The rational
    # conservative atlas extends slightly beyond it; those strict outer boxes
    # are chart-coordinate guard rejections only.
    seam_rows = [
        row for row in strata if row["predicate_label"] == "source_chart_seam"
    ]
    require(
        len(seam_rows) == 472
        and all(
            row["equation"] == "2*t^2-1=0"
            and row["dimension_account"] == "EXACT_DIMENSION_2_GRAPH"
            for row in seam_rows
        ),
        "physical source-chart seam graph",
    )
    require(
        len(parents) == 21232
        and statistics["completed_nonempty_3d_bulk_parent_count"] == 17392
        and statistics["bounded_partial_nonempty_parent_count"] == 3840
        and statistics["observed_exact_key_count"] == 116,
        "headline census",
    )
    return {
        "exact_rational_guard_rows_checked": len(guards),
        "source_chart_equation": "2*t^2=1",
        "source_chart_seam_2d_rows_checked": len(seam_rows),
        "source_grazing_2d_rows_checked": sum(
            row["predicate_label"] == "source_grazing" for row in strata
        ),
        "bulk_3d_rows_checked": len(resolved) + len(residual),
        "lower_dimensional_zero_credit_rows_checked": len(strata),
        "observed_local_exact_keys": 116,
        "global_geometric_exact_key_dispositions": 0,
    }


def wrapper(document_schema: str, result: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": document_schema,
        "result": result,
        "result_sha256": digest(result),
    }


def resign(document: dict[str, Any]) -> dict[str, Any]:
    document["result_sha256"] = digest(document["result"])
    return document


def exact_documents(
    certificate: dict[str, Any],
    attachment: dict[str, Any],
    expected_certificate: dict[str, Any],
    expected_attachment: dict[str, Any],
) -> None:
    require(
        certificate == expected_certificate,
        "full certificate canonical exact equality",
    )
    require(
        attachment == expected_attachment,
        "full attachment canonical exact equality",
    )


def mutation_tests(
    certificate: dict[str, Any],
    attachment: dict[str, Any],
    expected_certificate: dict[str, Any],
    expected_attachment: dict[str, Any],
) -> dict[str, Any]:
    certificate_mutations: list[
        tuple[str, Callable[[dict[str, Any]], None]]
    ] = [
        ("status", lambda d: d["result"].__setitem__("status", "PASS")),
        ("scope_count", lambda d: d["result"]["scope"].__setitem__(
            "Gate3_unique_first_parent_count", 21231
        )),
        ("scope_global_credit", lambda d: d["result"]["scope"].__setitem__(
            "global_geometric_exact_key_dispositions_added", 1
        )),
        ("precision", lambda d: d["result"]["provenance"].__setitem__(
            "dynamic_recut_precision_bits", 128
        )),
        ("atlas_direct", lambda d: d["result"][
            "independent_direct_Gate3_rebuild"
        ].__setitem__("direct_parent_count", 10615)),
        ("domain_equation", lambda d: d["result"][
            "adaptive_recut_contract"
        ].__setitem__("source_chart_domain_test", "2*t^2-1<=0")),
        ("half_open_owner", lambda d: d["result"][
            "adaptive_recut_contract"
        ].__setitem__("source_chart_diagonal_half_open_rule", "all own")),
        ("resolved_count", lambda d: d["result"][
            "materialization_census"
        ].__setitem__("resolved_3d_occurrence_row_count", 72499)),
        ("residual_count", lambda d: d["result"][
            "materialization_census"
        ].__setitem__("residual_3d_tube_row_count", 62011)),
        ("strata_count", lambda d: d["result"][
            "materialization_census"
        ].__setitem__("lower_dimensional_stratum_row_count", 62695)),
        ("complete_count", lambda d: d["result"][
            "materialization_census"
        ].__setitem__("completed_nonempty_3d_bulk_parent_count", 17393)),
        ("partial_count", lambda d: d["result"][
            "materialization_census"
        ].__setitem__("bounded_partial_nonempty_parent_count", 3839)),
        ("observed_keys", lambda d: d["result"][
            "materialization_census"
        ].__setitem__("observed_exact_key_count", 117)),
        ("global_disposition_after", lambda d: d["result"][
            "observed_occurrence_vs_global_disposition"
        ].__setitem__(
            "global_geometric_exact_key_disposition_count_after_Round174", 1
        )),
        ("keys_remaining", lambda d: d["result"][
            "observed_occurrence_vs_global_disposition"
        ].__setitem__("keys_without_global_geometric_disposition_after_Round174", 224579)),
        ("D02", lambda d: d["result"]["strict_nonpromotion"].__setitem__(
            "D02", "READY"
        )),
        ("Gate5", lambda d: d["result"]["strict_nonpromotion"].__setitem__(
            "global_Gate5_fields", "18/18"
        )),
        ("CM2", lambda d: d["result"]["strict_nonpromotion"].__setitem__(
            "CM2", "GO"
        )),
        ("attachment_path", lambda d: d["result"]["row_attachment"].__setitem__(
            "path", "../rows.json"
        )),
        ("attachment_hash", lambda d: d["result"]["row_attachment"].__setitem__(
            "file_sha256", "0" * 64
        )),
        ("table_digest", lambda d: d["result"]["row_attachment"][
            "table_census_and_sha256"
        ]["resolved_3d_occurrence_rows"].__setitem__(
            "rows_sha256", "0" * 64
        )),
        ("dimension_credit", lambda d: d["result"][
            "dimension_safe_ledger"
        ].__setitem__("lower_dimensional_row_whole_parent_credit", 1)),
        ("guard_credit", lambda d: d["result"][
            "dimension_safe_ledger"
        ].__setitem__(
            "chart_guard_rejection_is_not_Gate5_geometric_disposition", False
        )),
        ("transport", lambda d: d["result"][
            "Round173_transport_application"
        ].__setitem__("G_E_to_G_W_generator", "Jy")),
    ]
    attachment_mutations: list[tuple[str, tuple[Any, ...], Any]] = [
        ("parent_cell", ("result", "parent_rows", 0, 1), "G:W"),
        (
            "resolved_key",
            ("result", "resolved_3d_occurrence_rows", 0, 14),
            0,
        ),
        (
            "resolved_dimension",
            ("result", "resolved_3d_occurrence_rows", 0, 16),
            2,
        ),
        (
            "residual_credit",
            ("result", "residual_3d_tube_rows", 0, 8),
            1,
        ),
        (
            "guard_cm2_credit",
            ("result", "chart_guard_rejection_rows", 0, 8),
            True,
        ),
        (
            "guard_gate5_credit",
            ("result", "chart_guard_rejection_rows", 0, 9),
            True,
        ),
        (
            "stratum_3d_credit",
            ("result", "lower_dimensional_stratum_rows", 0, 10),
            1,
        ),
        (
            "stratum_whole_credit",
            ("result", "lower_dimensional_stratum_rows", 0, 11),
            1,
        ),
        (
            "alias_column",
            ("result", "row_column_schemas", "parent_rows", 0),
            "id",
        ),
        (
            "census_count",
            (
                "result", "table_census_and_sha256",
                "parent_rows", "row_count",
            ),
            21231,
        ),
    ]
    rejected: list[str] = []
    for name, mutate in certificate_mutations:
        candidate = copy.deepcopy(certificate)
        mutate(candidate)
        resign(candidate)
        try:
            exact_documents(
                candidate, attachment,
                expected_certificate, expected_attachment,
            )
        except Exception:
            rejected.append(f"certificate:{name}")
        else:
            raise RuntimeError(f"accepted resigned certificate attack:{name}")
    for name, path, replacement in attachment_mutations:
        container: Any = attachment
        for component in path[:-1]:
            container = container[component]
        final_component = path[-1]
        original = container[final_component]
        original_result_sha256 = attachment["result_sha256"]
        container[final_component] = replacement
        resign(attachment)
        try:
            exact_documents(
                certificate, attachment,
                expected_certificate, expected_attachment,
            )
        except Exception:
            rejected.append(f"attachment:{name}")
        else:
            raise RuntimeError(f"accepted resigned attachment attack:{name}")
        finally:
            container[final_component] = original
            attachment["result_sha256"] = original_result_sha256
    require(
        len(rejected)
        == len(certificate_mutations) + len(attachment_mutations),
        "resigned attack census",
    )
    return {
        "attempted": len(rejected),
        "rejected": len(rejected),
        "labels": rejected,
        "all_rejected": True,
    }


def strict_json_tests() -> dict[str, Any]:
    attacks = {
        "duplicate_key": b'{"x":1,"x":2}',
        "bom": b'\xef\xbb\xbf{"x":1}',
        "nul": b'{"x":"\\u0000"}',
        "nan": b'{"x":NaN}',
        "infinity": b'{"x":Infinity}',
        "float": b'{"x":1.25}',
        "top_array": b'[]',
        "trailing": b'{"x":1} trailing',
        "invalid_utf8": b'{"x":"\xff"}',
    }
    rejected = []
    for name, raw in attacks.items():
        try:
            strict_decode(raw)
        except Exception:
            rejected.append(name)
        else:
            raise RuntimeError(f"accepted strict JSON attack:{name}")
    try:
        strict_decode(b"x" * 130_000_001)
    except Exception:
        rejected.append("oversize")
    else:
        raise RuntimeError("accepted strict JSON oversize attack")
    return {
        "attempted": len(attacks) + 1,
        "rejected": len(rejected),
        "labels": rejected,
        "all_rejected": len(rejected) == len(attacks) + 1,
    }


def path_tests() -> dict[str, Any]:
    rejected: list[str] = []
    with tempfile.TemporaryDirectory(dir=BASE) as temporary:
        root = Path(temporary)
        stem = root.name
        ordinary = BASE / f"{stem}-ordinary.json"
        symlink = BASE / f"{stem}-symlink.json"
        hardlink = BASE / f"{stem}-hardlink.json"
        directory = BASE / f"{stem}-directory.json"
        fifo = BASE / f"{stem}-fifo.json"
        ordinary.write_text('{"x":1}', encoding="utf-8")
        symlink.symlink_to(ordinary)
        os.link(ordinary, hardlink)
        directory.mkdir()
        os.mkfifo(fifo)
        attacks = [
            ("parent_escape", root / "outside.json"),
            ("symlink", symlink),
            ("hardlink", hardlink),
            ("directory", directory),
            ("fifo", fifo),
            ("missing", BASE / f"{stem}-missing.json"),
        ]
        try:
            for name, path in attacks:
                try:
                    input_guard(path, 1_000_000)
                except Exception:
                    rejected.append(name)
                else:
                    raise RuntimeError(f"accepted path attack:{name}")
            output_attacks = [
                ("output_producer_alias", PRODUCER),
                ("output_certificate_alias", CERTIFICATE),
                ("output_attachment_alias", ATTACHMENT),
                ("output_symlink", symlink),
                ("output_hardlink", hardlink),
            ]
            for name, path in output_attacks:
                try:
                    output_guard(path)
                except Exception:
                    rejected.append(name)
                else:
                    raise RuntimeError(f"accepted output alias attack:{name}")
        finally:
            for path in (symlink, hardlink, ordinary, fifo):
                if path.exists() or path.is_symlink():
                    path.unlink()
            if directory.exists():
                directory.rmdir()
    return {
        "attempted": 11,
        "rejected": len(rejected),
        "labels": rejected,
        "all_rejected": len(rejected) == 11,
    }


def output_guard(path: Path) -> None:
    protected = {
        PRODUCER.resolve(),
        CERTIFICATE.resolve(),
        ATTACHMENT.resolve(),
        Path(__file__).resolve(),
        *[(BASE / name).resolve() for name in DEPENDENCIES],
    }
    require(path.parent.exists() and path.parent.is_dir(), "output parent")
    require(not path.parent.is_symlink(), "output parent symlink")
    candidate = path.resolve(strict=False)
    require(candidate not in protected, "output aliases protected input")
    if path.exists() or path.is_symlink():
        require(not path.is_symlink(), "output symlink")
        info = path.stat()
        require(stat.S_ISREG(info.st_mode), "output regular")
        require(info.st_nlink == 1, "output hardlink")
        require(
            all(not os.path.samefile(path, protected_path)
                for protected_path in protected),
            "output samefile protected input",
        )


def build_verification() -> dict[str, Any]:
    inputs = load_frozen_inputs()
    certificate_raw = input_guard(CERTIFICATE, 1_000_000)
    attachment_raw = input_guard(ATTACHMENT, 130_000_000)
    require(
        hashlib.sha256(certificate_raw).hexdigest()
        == EXPECTED_CERTIFICATE_SHA256,
        "certificate file pin",
    )
    require(
        hashlib.sha256(attachment_raw).hexdigest()
        == EXPECTED_ATTACHMENT_SHA256,
        "attachment file pin",
    )
    certificate = strict_decode(certificate_raw)
    attachment = strict_decode(attachment_raw)
    require(
        set(certificate) == {"schema", "result", "result_sha256"}
        and certificate["schema"] == CERTIFICATE_SCHEMA
        and certificate["result_sha256"]
        == EXPECTED_CERTIFICATE_RESULT
        == digest(certificate["result"])
        and certificate["result"]["status"] == CERTIFIED_STATUS,
        "certificate wrapper",
    )
    require(
        set(attachment) == {"schema", "result", "result_sha256"}
        and attachment["schema"] == ATTACHMENT_SCHEMA
        and attachment["result_sha256"]
        == EXPECTED_ATTACHMENT_RESULT
        == digest(attachment["result"]),
        "attachment wrapper",
    )

    registry = rebuild_registry(inputs["gate5"])
    direct_atlases = build_direct_atlases()
    chart_rows = audit_atlases(direct_atlases, inputs["gate3"])
    ctx.prec = DYNAMIC_BITS
    rows = independently_build_all_rows(direct_atlases, registry)
    expected_attachment = independently_pack_attachment(rows)
    expected_attachment_raw = (
        canonical(expected_attachment) + "\n"
    ).encode("utf-8")
    require(
        hashlib.sha256(expected_attachment_raw).hexdigest()
        == EXPECTED_ATTACHMENT_SHA256,
        "independently reconstructed attachment byte digest",
    )
    require(
        expected_attachment_raw == attachment_raw,
        "full 109 MiB attachment byte equality",
    )
    statistics = independently_compute_statistics(rows)
    physical = physical_ledger_audit(rows, statistics)
    result = expected_certificate_result(
        inputs,
        chart_rows,
        statistics,
        expected_attachment,
        EXPECTED_ATTACHMENT_SHA256,
    )
    expected_certificate = wrapper(CERTIFICATE_SCHEMA, result)
    require(
        expected_certificate["result_sha256"]
        == EXPECTED_CERTIFICATE_RESULT,
        "independently reconstructed certificate result digest",
    )
    exact_documents(
        certificate,
        attachment,
        expected_certificate,
        expected_attachment,
    )
    mutations = mutation_tests(
        certificate,
        attachment,
        expected_certificate,
        expected_attachment,
    )
    strict_json = strict_json_tests()
    paths = path_tests()
    verifier_sha256 = hashlib.sha256(
        Path(__file__).read_bytes()
    ).hexdigest()
    verification_result = {
        "status": "PASS",
        "certificate_schema": CERTIFICATE_SCHEMA,
        "certificate_file_sha256": EXPECTED_CERTIFICATE_SHA256,
        "certificate_result_sha256": EXPECTED_CERTIFICATE_RESULT,
        "attachment_schema": ATTACHMENT_SCHEMA,
        "attachment_file_sha256": EXPECTED_ATTACHMENT_SHA256,
        "attachment_result_sha256": EXPECTED_ATTACHMENT_RESULT,
        "producer_file_sha256": EXPECTED_PRODUCER_SHA256,
        "verifier_file_sha256": verifier_sha256,
        "producer_imported_or_executed": False,
        "producer_treated_as_inert_pinned_evidence": True,
        "full_certificate_exactly_matched": True,
        "full_attachment_exactly_matched": True,
        "full_attachment_byte_for_byte_matched": True,
        "full_attachment_bytes_compared": len(attachment_raw),
        "independent_reconstruction": {
            "Gate3_atlas_precision_bits": ATLAS_BITS,
            "dynamic_recut_precision_bits": DYNAMIC_BITS,
            "direct_atlas_leaf_counts": {
                "G:E": 16580,
                "G:N": 16630,
            },
            "direct_unique_first_parent_counts": {
                "G:E": 5276,
                "G:N": 5340,
            },
            "direct_and_reflected_parent_count": 21232,
            "resolved_3d_occurrence_row_count": 72500,
            "residual_3d_tube_row_count": 62012,
            "chart_guard_rejection_row_count": 728,
            "lower_dimensional_stratum_row_count": 62696,
            "completed_nonempty_3d_bulk_parent_count": 17392,
            "bounded_partial_nonempty_parent_count": 3840,
            "observed_local_exact_key_count": 116,
            "global_geometric_exact_key_disposition_count": 0,
            "Round173_reflected_rows_checked_exactly": True,
        },
        "physical_chart_and_dimension_audit": physical,
        "resigned_semantic_attacks": mutations,
        "strict_json_attacks": strict_json,
        "path_alias_and_type_attacks": paths,
        "strict_nonpromotion_reconfirmed": {
            "source_G_global_exact_key_dispositions": "0/224580",
            "global_Gate5_fields": "10/18",
            "global_complete_18_field_blocks": 0,
            "D02": "BLOCKED",
            "D03_negative_oracle": "UNAUTHORIZED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
        "hash_seed_sensitive_output_fields": [],
    }
    return wrapper(VERIFICATION_SCHEMA, verification_result)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    output_guard(arguments.output)
    verification = build_verification()
    arguments.output.write_text(
        json.dumps(
            verification,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        ) + "\n",
        encoding="utf-8",
    )
    result = verification["result"]
    print(result["status"])
    print(
        "full rows",
        result["independent_reconstruction"][
            "resolved_3d_occurrence_row_count"
        ],
        result["independent_reconstruction"]["residual_3d_tube_row_count"],
        result["independent_reconstruction"][
            "lower_dimensional_stratum_row_count"
        ],
    )
    print(
        "attacks",
        result["resigned_semantic_attacks"]["rejected"],
        result["strict_json_attacks"]["rejected"],
        result["path_alias_and_type_attacks"]["rejected"],
    )
    print(verification["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
