#!/usr/bin/env python3
"""Round174: bounded source-G unique-first dynamic occurrence materialization.

The two direct Gate3 atlases G:E and G:N are rebuilt at the frozen 192-bit
precision.  Every unique-first parent is then recut at 256 bits.  A positive
three-dimensional child is accepted only when all of the following are
strict on its closed enclosure:

* the inherited first owner has a positive non-grazing near root below 3;
* every integer-wall endpoint is off every wall;
* crossing counts and the complete X/Y event order are fixed;
* the signed wall word belongs to the frozen 985-pattern grammar;
* the target normal lies in one strict outgoing chart; and
* the exact Gate5 pair, roof, ordinal and key identifier agree.

Jx transports G:E rows to G:W and Jy transports G:N rows to G:S using the
frozen Round173 dictionary.  Source-chart guard rejection, unresolved
positive-volume tubes, two-dimensional analytic predicates and
one-dimensional candidate intersections are kept in separate tables.  No
graph or intersection is promoted to a whole-parent or three-dimensional
credit, and occurrence witnesses are not global geometric dispositions.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import multiprocessing as mp
import os
import stat
import sys
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Iterable

from flint import arb, ctx, __version__ as FLINT_VERSION

import cm2_gate3_candidate_first_hit_cert as first_hit
import cm2_gate3_eight_cell_symmetry_atlas_cert as atlas


HERE = Path(__file__).resolve().parent
OUTPUT = (
    HERE
    / "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_certificate.json"
)
ATTACHMENT = (
    HERE
    / "cm2_round174_source_g_unique_first_dynamic_occurrence_materialization_rows.json"
)
SCHEMA = (
    "cm2.round174.source-g-unique-first-dynamic-occurrence-materialization.v1"
)
ATTACHMENT_SCHEMA = (
    "cm2.round174.source-g-unique-first-dynamic-occurrence-rows.v1"
)
STATUS = (
    "CERTIFIED_BOUNDED_PARTIAL_SOURCE_G_UNIQUE_FIRST_DYNAMIC_OCCURRENCE_ROWS__"
    "NO_GLOBAL_DISPOSITION_OR_D02_PROMOTION"
)
ATLAS_PRECISION_BITS = 192
DYNAMIC_PRECISION_BITS = 256
MAX_DYNAMIC_REFINE_DEPTH = 6
PATTERN_COUNT = 985
SOURCE_G_KEY_COUNT = 224580
DIRECT_CHARTS = ("G:E", "G:N")
ALL_G_CHARTS = ("G:E", "G:W", "G:N", "G:S")

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
    "cm2-round173-source-g-exact-return-signature-transport-manifest-2026-07-26.sha256"
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

PINS = {
    R169P:
        "2be6580fb7d3d47a7ddab05f22d7987ba28d531bb1dd5af5c0082b458e089ee9",
    R169C:
        "87c5b5f5467aa19b3bafce9e20c10371877012af65937983ced43fcccb22c2fb",
    R169V:
        "ed5d26a532f184702551da526e5ffbc0feafbf1e8c89eb55d260b15428aaab67",
    R169O:
        "90c207dd952329d0547ec0440e35cffa57d7b11f98ed17869f3a07df6ce3161f",
    R171P:
        "bcaba20978ebb5386d64bcf248d254c54c8ac79d9c9c7eb023be278ab7e05c75",
    R171C:
        "1fb4827b42569d41602765445d0333c76b2ef97615873fc406563ac0e18af7a5",
    R171V:
        "aee7b3cc3f1468b6a46e7a90e1bb219bd609bddfe54075c6c73e124d98eda7e0",
    R171O:
        "effdfd4306dbf7bd70df1e9b5ed9166a58dc00a5d333b0f2f2a5f0cb930ccce9",
    R173P:
        "bdbf794a99dc9276b11b7680818994d63f52fe0e5a857948701f64e8d5d16a0f",
    R173C:
        "5ff82c5822f543109da0d50c0637d0d2f9148a738b1a21b16878c70e5505cf1a",
    R173V:
        "eb2b51929719563cd9fe72d180f3f1932a049e983ad1e7a8ec9ac89526bc30f1",
    R173O:
        "e205367506bc02aa982de074253e5806f07b4358dd3738fb4a0e14476e44ce99",
    R173M:
        "ba2a1b6eea612e538e3ca70e2916e07469fda38eaef24a751ff862262336f275",
    FHP:
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    FHM:
        "0c820a5e3481b2c18fabb14d8d0fab7ce454f9a9e68b856bb2a7bf139404f7f4",
    GEP:
        "ab120f85a263f3cb0697d8a40bc9ed2bf12b361aa7c54940c214b6fd85b17e2b",
    GEM:
        "d502d0b1c8ef6dba349fa5b7211da4c0a3fcff78bf92a46457cb4f4b64f760f5",
    G3P:
        "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    G3M:
        "f8fda665edbb7d8b39ce495188f90ecb2b5ec4384c1eb958949627df167c4987",
    SP:
        "fa00d4c14ee24b8f3fbc7f345deef13deb272080a886b68d2aa2f9c92a456fe1",
    SV:
        "3eb5b5525eab0d2e4935374e6d9fa453717de13634613afa579cd1ae30dbcea6",
    SM:
        "1fb40060336f04f28a7cac19a70abdd3692ced272825b2f1f6b6ae005f00518b",
    G5P:
        "ddcc250f8700c6a695f96019d9f7824fe98636e20a67685fdc6a3cce77f6d695",
    G5V:
        "0384acdd1f912b0d4b3bee84ff530358d9693893d1c5c64a1deabaede8e0867b",
    G5M:
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866",
}
R169_RESULT = (
    "8cf83c0ef48aea3a6023546a2df52398241d7baf113e9b78a917c7de4e3d68d6"
)
R169_VERIFY_RESULT = (
    "4c89a30e89f4fd0b599264a52c8a81f535c4c9df6c60682e6f60594744decdb1"
)
R171_RESULT = (
    "ffac0e2e16829c1a3ffc4783af2c224288265d02cf53c1d041aaf02013b52957"
)
R171_VERIFY_RESULT = (
    "60e9d4038c63bba14c0bd95478f63840735d8283f9cdfdefb1405ee2ed7defe3"
)
R173_RESULT = (
    "948ab0a8539b08adc96c9493de415b44a5ffb75a1ee3ef47a4742902c211c11f"
)
R173_VERIFY_RESULT = (
    "047a580eb546cdb3880b93a9d0358e390d7ce418b371612f8e9fc4b0528f4644"
)

SOURCE_CHARTS = tuple(
    f"{source}:{cell}"
    for source in ("G", "W")
    for cell in ("E", "W", "N", "S")
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
        document["result_sha256"] == result_sha256
        == digest(document["result"]),
        f"digest:{schema}",
    )
    require(document["result"]["status"] == status, f"status:{schema}")
    return document["result"]


def load_inputs() -> dict[str, Any]:
    require(FLINT_VERSION == "0.9.0", "python-flint version")
    for name, expected in PINS.items():
        path = HERE / name
        safe_input(path)
        require(
            hashlib.sha256(path.read_bytes()).hexdigest() == expected,
            f"pin:{name}",
        )
    r169 = unwrap(
        strict_load(HERE / R169C),
        "cm2.round169.source-g-return-signature-coverage-survey.v1",
        R169_RESULT,
        "CERTIFIED_SOURCE_G_EXACT_KEY_COVERAGE_DEFICIT_SURVEY__"
        "NO_EXTERIOR_OR_D02_PROMOTION",
    )
    r169v = unwrap(
        strict_load(HERE / R169O),
        "cm2.round169.source-g-return-signature-coverage-survey.verification.v1",
        R169_VERIFY_RESULT,
        "PASS",
    )
    r171 = unwrap(
        strict_load(HERE / R171C),
        "cm2.round171.compact-gate3-source-g-coordinate-bridge.v1",
        R171_RESULT,
        "CERTIFIED_COMPACT_TO_GATE3_SOURCE_G_COORDINATE_COVER__"
        "NO_RETURN_KEY_OR_D02_PROMOTION",
    )
    r171v = unwrap(
        strict_load(HERE / R171O),
        "cm2.round171.compact-gate3-source-g-coordinate-bridge.verification.v1",
        R171_VERIFY_RESULT,
        "PASS",
    )
    r173 = unwrap(
        strict_load(HERE / R173C),
        "cm2.round173.source-g-exact-return-signature-transport.v1",
        R173_RESULT,
        "CERTIFIED_SOURCE_G_JX_JY_EXACT_RETURN_SIGNATURE_TRANSPORT_DICTIONARY__"
        "NO_DYNAMIC_ROW_OR_D02_PROMOTION",
    )
    r173v = unwrap(
        strict_load(HERE / R173O),
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
        "prior verification bindings",
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
        "prior zero-credit guard",
    )
    gate5 = strict_load(HERE / G5M)
    gate3 = strict_load(HERE / G3M)
    first = strict_load(HERE / FHM)
    seam = strict_load(HERE / SM)
    registry = gate5["result"]["immutable_candidate_key_registry"]
    require(
        gate5["schema"]
        == "cm2.gate5.return-word-three-norm-frontier.manifest.v1"
        and registry["retained_chart_target_pair_count"] == 448
        and registry["crossing_pattern_count_per_pair"] == PATTERN_COUNT
        and registry["candidate_return_word_key_count"] == 441280
        and registry["complete_physical_operator_block_count"] == 0
        and gate5["verdict"]["gate5"] == "NOT_CERTIFIED",
        "Gate5 frontier",
    )
    require(
        first["schema"] == "cm2.gate3.first-hit-atlas.v1"
        and first["candidate_reduction"]["retained_pair_count"] == 448,
        "first-hit frontier",
    )
    require(
        gate3["schema"] == "cm2.gate3.eight-cell-symmetry-atlas.v1"
        and gate3["coverage"]["global_leaf_count"] == 143248
        and gate3["charts"]["G:E"]["counts"]["unique_first"] == 5276
        and gate3["charts"]["G:N"]["counts"]["unique_first"] == 5340
        and gate3["charts"]["G:W"]["counts"]["unique_first"] == 5276
        and gate3["charts"]["G:S"]["counts"]["unique_first"] == 5340,
        "Gate3 source-G atlas",
    )
    require(
        seam["schema"] == "cm2.gate3.chart-seam-quotient.manifest.v1"
        and seam["result"]["unique_half_open_owner_rule"]["diagonal_tie"]
        == "E or W owns; N or S excludes"
        and seam["verdict"]["eight_chart_seam_ownership"] == "CERTIFIED",
        "source/outgoing half-open chart rule",
    )
    return {
        "r169": r169,
        "r171": r171,
        "r173": r173,
        "gate5": gate5,
        "gate3": gate3,
        "seam": seam,
    }


def crossing_patterns() -> tuple[tuple[str, ...], ...]:
    rows: list[tuple[str, ...]] = []
    for nx in range(5):
        for ny in range(5):
            length = nx + ny
            x_signs = (0,) if nx == 0 else (-1, 1)
            y_signs = (0,) if ny == 0 else (-1, 1)
            for sx in x_signs:
                for sy in y_signs:
                    for positions in itertools.combinations(range(length), nx):
                        x_positions = set(positions)
                        x_token = "X+" if sx > 0 else "X-"
                        y_token = "Y+" if sy > 0 else "Y-"
                        rows.append(tuple(
                            x_token if index in x_positions else y_token
                            for index in range(length)
                        ))
    return tuple(rows)


def registry_tables(gate5: dict[str, Any]) -> dict[str, Any]:
    pairs = tuple(
        (chart, target)
        for chart in SOURCE_CHARTS
        for target in first_hit.candidate_ids(chart)
    )
    patterns = crossing_patterns()
    require(
        len(pairs) == len(set(pairs)) == 448,
        "Gate5 pair reconstruction",
    )
    require(
        len(patterns) == len(set(patterns)) == PATTERN_COUNT
        and Counter(map(len, patterns))
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
        "Gate5 pattern reconstruction",
    )
    frozen = gate5["result"]
    registry = frozen["immutable_candidate_key_registry"]
    require(
        digest(pairs) == registry["chart_target_pair_rows_sha256"]
        and digest(patterns)
        == frozen["crossing_grammar"]["crossing_pattern_rows_sha256"],
        "Gate5 pair/pattern digests",
    )
    stream = hashlib.sha256()
    count = 0
    for chart, target in pairs:
        for pattern in patterns:
            row = [chart, target, list(pattern), len(pattern) + 1]
            stream.update(canonical(row).encode("utf-8"))
            stream.update(b"\n")
            count += 1
    require(
        count == 441280
        and stream.hexdigest()
        == registry["candidate_word_key_rows_sha256"],
        "Gate5 full row stream",
    )
    return {
        "pairs": pairs,
        "patterns": patterns,
        "pair_index": {
            pair: index for index, pair in enumerate(pairs)
        },
        "pattern_index": {
            pattern: index for index, pattern in enumerate(patterns)
        },
    }


def official_key(
    chart: str,
    target: str,
    pattern: tuple[str, ...],
    tables: dict[str, Any],
) -> dict[str, Any]:
    pair = (chart, target)
    require(pair in tables["pair_index"], "official pair")
    require(pattern in tables["pattern_index"], "official pattern")
    ordinal = (
        tables["pair_index"][pair] * PATTERN_COUNT
        + tables["pattern_index"][pattern]
    )
    row = [chart, target, list(pattern), len(pattern) + 1]
    return {
        "row": row,
        "ordinal": ordinal,
        "identifier": f"gate5-word:{ordinal:06d}:{digest(row)}",
    }


def rebuild_direct_atlases() -> dict[str, list[Any]]:
    ctx.prec = ATLAS_PRECISION_BITS
    # Each chart is independent.  Forked workers inherit only pinned module
    # state; returned leaves contain exact Fractions and finite labels, no Arb.
    with mp.get_context("fork").Pool(processes=2) as pool:
        rebuilt = pool.map(atlas.build_atlas, DIRECT_CHARTS)
    result = dict(zip(DIRECT_CHARTS, rebuilt, strict=True))
    return result


def audit_atlases(
    direct: dict[str, list[Any]],
    gate3: dict[str, Any],
) -> dict[str, Any]:
    expected = {
        "G:E": (16580, 5276),
        "G:N": (16630, 5340),
    }
    rows: dict[str, Any] = {}
    reflected: dict[str, list[Any]] = {}
    for chart in DIRECT_CHARTS:
        leaves = direct[chart]
        leaf_rows = [atlas.leaf_row(chart, leaf) for leaf in leaves]
        unique = [
            leaf for leaf in leaves
            if leaf.classification == "unique_first"
        ]
        require(
            (len(leaves), len(unique)) == expected[chart]
            and atlas.canonical_digest(leaf_rows)
            == gate3["charts"][chart]["leaf_rows_sha256"],
            f"direct atlas:{chart}",
        )
        rows[chart] = {
            "leaf_count": len(leaves),
            "unique_first_parent_count": len(unique),
            "leaf_rows_sha256": atlas.canonical_digest(leaf_rows),
            "unique_first_leaf_rows_sha256": digest([
                atlas.leaf_row(chart, leaf) for leaf in unique
            ]),
        }
    for source_chart, axis, destination_chart in (
        ("G:E", "vertical", "G:W"),
        ("G:N", "horizontal", "G:S"),
    ):
        leaves = [
            atlas.reflect_leaf(source_chart, axis, leaf)
            for leaf in direct[source_chart]
        ]
        leaves.sort(key=lambda leaf: leaf.box.path)
        leaf_rows = [
            atlas.leaf_row(destination_chart, leaf) for leaf in leaves
        ]
        require(
            len(leaves) == gate3["charts"][destination_chart]["leaf_count"]
            and sum(
                leaf.classification == "unique_first" for leaf in leaves
            )
            == gate3["charts"][destination_chart]["counts"]["unique_first"]
            and atlas.canonical_digest(leaf_rows)
            == gate3["charts"][destination_chart]["leaf_rows_sha256"],
            f"reflected atlas:{destination_chart}",
        )
        reflected[destination_chart] = leaves
        rows[destination_chart] = {
            "leaf_count": len(leaves),
            "unique_first_parent_count": sum(
                leaf.classification == "unique_first" for leaf in leaves
            ),
            "leaf_rows_sha256": atlas.canonical_digest(leaf_rows),
            "transported_from": source_chart,
            "transport_generator": "Jx" if axis == "vertical" else "Jy",
        }
    require(
        sum(
            row["unique_first_parent_count"] for row in rows.values()
        ) == 21232,
        "source-G unique parent census",
    )
    return {"rows": rows, "reflected": reflected}


def box_payload(box: Any) -> list[str]:
    return [
        qstr(box.t0),
        qstr(box.t1),
        qstr(box.p0),
        qstr(box.p1),
        qstr(box.s0),
        qstr(box.s1),
    ]


def box_volume(box: Any) -> Q:
    return (
        (box.t1 - box.t0)
        * (box.p1 - box.p0)
        * (box.s1 - box.s0)
    )


def chart_domain_status(box: Any) -> str:
    maximum_abs = max(abs(box.t0), abs(box.t1))
    minimum_abs = (
        Q(0)
        if box.t0 <= 0 <= box.t1
        else min(abs(box.t0), abs(box.t1))
    )
    if 2 * maximum_abs * maximum_abs - 1 < 0:
        return "STRICT_INSIDE_TRUE_SOURCE_CHART"
    if 2 * minimum_abs * minimum_abs - 1 > 0:
        return "STRICT_OUTSIDE_TRUE_SOURCE_CHART_GUARD"
    return "CROSSES_TRUE_SOURCE_CHART_SEAM"


def axis_events(
    q: arb,
    h: arb,
    axis: str,
) -> tuple[list[tuple[arb, str, int]] | None, list[str]]:
    if not (
        bool(q > -7)
        and bool(q < 7)
        and bool(h > -7)
        and bool(h < 7)
    ):
        return None, [f"wall_endpoint_audit_range:{axis}"]
    events: list[tuple[arb, str, int]] = []
    reasons: list[str] = []
    for wall in range(-6, 7):
        wall_ball = arb(wall)
        plus = bool(q < wall_ball) and bool(h > wall_ball)
        minus = bool(q > wall_ball) and bool(h < wall_ball)
        same_lower = bool(q < wall_ball) and bool(h < wall_ball)
        same_upper = bool(q > wall_ball) and bool(h > wall_ball)
        if plus or minus:
            alpha = (wall_ball - q) / (h - q)
            if bool(alpha > 0) and bool(alpha < 1):
                events.append((
                    alpha,
                    axis + ("+" if plus else "-"),
                    wall,
                ))
            else:
                reasons.append(
                    f"wall_crossing_time_not_strict:{axis}:{wall}"
                )
        elif not (same_lower or same_upper):
            reasons.append(
                f"wall_endpoint_or_count_transition:{axis}:{wall}"
            )
    if len(events) > 4:
        reasons.append(f"more_than_four_crossings:{axis}")
    if reasons:
        return None, reasons
    return events, []


def strict_event_order(
    events: list[tuple[arb, str, int]],
) -> tuple[list[list[Any]] | None, list[str]]:
    remaining = list(events)
    ordered: list[list[Any]] = []
    while remaining:
        minima = [
            index
            for index, (alpha, _token, _wall) in enumerate(remaining)
            if all(
                index == other
                or bool(alpha < other_alpha)
                for other, (other_alpha, _other_token, _other_wall)
                in enumerate(remaining)
            )
        ]
        if len(minima) != 1:
            return None, ["simultaneous_corner_order"]
        _alpha, token, wall = remaining.pop(minima[0])
        ordered.append([token, wall])
    return ordered, []


def strict_outgoing_chart(
    normal_x: arb,
    normal_y: arb,
) -> tuple[str | None, list[str]]:
    difference = abs(normal_x) - abs(normal_y)
    if bool(difference > 0):
        if bool(normal_x > 0):
            return "E", []
        if bool(normal_x < 0):
            return "W", []
        return None, ["outgoing_chart_component_sign"]
    if bool(difference < 0):
        if bool(normal_y > 0):
            return "N", []
        if bool(normal_y < 0):
            return "S", []
        return None, ["outgoing_chart_component_sign"]
    return None, ["outgoing_chart_seam"]


def dynamic_signature(
    chart: str,
    box: Any,
    target: str,
    tables: dict[str, Any],
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
    normal_x = (
        -radical * ux + record.transverse * uy
    ) / radius
    normal_y = (
        -radical * uy - record.transverse * ux
    ) / radius
    target_object = first_hit.target_by_id(target)
    center_x, center_y = first_hit.target_center(target_object, s)
    hit_x = center_x + radius * normal_x
    hit_y = center_y + radius * normal_y
    x_events, x_reasons = axis_events(qx, hit_x, "X")
    y_events, y_reasons = axis_events(qy, hit_y, "Y")
    outgoing, outgoing_reasons = strict_outgoing_chart(
        normal_x, normal_y
    )
    reasons = [*x_reasons, *y_reasons, *outgoing_reasons]
    ordered: list[list[Any]] | None = None
    if x_events is not None and y_events is not None:
        ordered, order_reasons = strict_event_order(
            x_events + y_events
        )
        reasons.extend(order_reasons)
    if reasons:
        return None, sorted(set(reasons))
    assert ordered is not None and outgoing is not None
    pattern = tuple(row[0] for row in ordered)
    key = official_key(chart, target, pattern, tables)
    require(
        len(pattern) <= 8
        and sum(token.startswith("X") for token in pattern) <= 4
        and sum(token.startswith("Y") for token in pattern) <= 4,
        "wall grammar bounds",
    )
    return {
        "target": target,
        "events": ordered,
        "pattern": pattern,
        "roof": len(pattern) + 1,
        "outgoing_cell": outgoing,
        "target_chart": f"{target[0]}:{outgoing}",
        "key": key,
        "target_grazing_strictly_absent": True,
        "event_order_strict_on_closed_enclosure": True,
    }, []


def split_box(box: Any, axis: int) -> tuple[Any, Any]:
    depth = box.depth + 1
    if axis == 0:
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
    if axis == 1:
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


def evaluate_cell(
    chart: str,
    box: Any,
    target: str,
    tables: dict[str, Any],
) -> tuple[str, Any]:
    domain = chart_domain_status(box)
    if domain == "STRICT_OUTSIDE_TRUE_SOURCE_CHART_GUARD":
        return "guard", None
    if domain == "CROSSES_TRUE_SOURCE_CHART_SEAM":
        return "source_seam", ["source_chart_seam"]
    signature, reasons = dynamic_signature(chart, box, target, tables)
    if signature is not None:
        return "resolved", signature
    return "residual", reasons


PARENT_COLUMNS = [
    "parent_id",
    "chart",
    "leaf_id",
    "owner_target",
    "box",
    "coordinate_volume",
    "resolved_child_count",
    "resolved_coordinate_volume",
    "residual_tube_count",
    "residual_coordinate_volume",
    "guard_rejection_count",
    "guard_rejection_coordinate_volume",
    "bulk_completion_status",
    "observed_exact_key_count",
    "observed_exact_key_ordinals_sha256",
    "provenance",
    "transport_source_parent_id",
    "transport_generator",
    "source_grazing_boundary_faces",
    "source_chart_seam_half_open_status",
    "gate3_leaf_row_sha256",
]
RESOLVED_COLUMNS = [
    "row_id",
    "chart",
    "parent_id",
    "refinement_path",
    "box",
    "coordinate_volume",
    "owner_target",
    "ordered_integer_wall_events",
    "wall_crossing_count",
    "signed_wall_word",
    "roof",
    "outgoing_cell",
    "target_chart",
    "official_key_row",
    "official_key_ordinal",
    "official_key_id",
    "ambient_dimension",
    "physical_open_subset_positive",
    "provenance",
    "transport_source_row_id",
    "transport_generator",
]
RESIDUAL_COLUMNS = [
    "row_id",
    "chart",
    "parent_id",
    "refinement_path",
    "box",
    "coordinate_volume",
    "reason_labels",
    "ambient_dimension",
    "whole_parent_credit",
    "provenance",
    "transport_source_row_id",
    "transport_generator",
]
GUARD_COLUMNS = [
    "row_id",
    "chart",
    "parent_id",
    "refinement_path",
    "box",
    "coordinate_volume",
    "exact_rejection_predicate",
    "classification",
    "is_CM2_exterior_sheet_exclusion",
    "is_Gate5_geometric_disposition",
    "provenance",
    "transport_source_row_id",
    "transport_generator",
]
STRATUM_COLUMNS = [
    "stratum_id",
    "chart",
    "parent_id",
    "containing_residual_row_id",
    "predicate_label",
    "equation",
    "dimension_account",
    "dimension_certification",
    "existence_certification",
    "half_open_owner_status",
    "three_dimensional_volume_credit",
    "whole_parent_credit",
    "provenance",
    "transport_source_stratum_id",
    "transport_generator",
]


def as_row(columns: list[str], values: dict[str, Any]) -> list[Any]:
    require(set(values) == set(columns), "row columns")
    return [values[column] for column in columns]


def source_grazing_faces(box: Any) -> list[str]:
    result: list[str] = []
    if box.p0 == -1:
        result.append("p=-1")
    if box.p1 == 1:
        result.append("p=+1")
    return result


def source_seam_status(chart: str) -> str:
    cell = chart.split(":")[1]
    return (
        "E_OR_W_HALF_OPEN_OWNER"
        if cell in {"E", "W"}
        else "N_OR_S_EXCLUDES_DIAGONAL_TIE"
    )


def row_id(prefix: str, payload: Any) -> str:
    return f"round174-{prefix}:{digest(payload)}"


def build_resolved_row(
    chart: str,
    parent_id: str,
    refinement_path: list[str],
    box: Any,
    signature: dict[str, Any],
) -> dict[str, Any]:
    payload = [
        chart,
        parent_id,
        refinement_path,
        box_payload(box),
        signature["key"]["identifier"],
        signature["outgoing_cell"],
    ]
    return {
        "row_id": row_id("resolved-3d", payload),
        "chart": chart,
        "parent_id": parent_id,
        "refinement_path": refinement_path,
        "box": box_payload(box),
        "coordinate_volume": qstr(box_volume(box)),
        "owner_target": signature["target"],
        "ordered_integer_wall_events": signature["events"],
        "wall_crossing_count": len(signature["events"]),
        "signed_wall_word": list(signature["pattern"]),
        "roof": signature["roof"],
        "outgoing_cell": signature["outgoing_cell"],
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


def build_residual_row(
    chart: str,
    parent_id: str,
    refinement_path: list[str],
    box: Any,
    reasons: list[str],
) -> dict[str, Any]:
    reasons = sorted(set(reasons))
    payload = [
        chart, parent_id, refinement_path, box_payload(box), reasons
    ]
    return {
        "row_id": row_id("residual-3d-tube", payload),
        "chart": chart,
        "parent_id": parent_id,
        "refinement_path": refinement_path,
        "box": box_payload(box),
        "coordinate_volume": qstr(box_volume(box)),
        "reason_labels": reasons,
        "ambient_dimension": 3,
        "whole_parent_credit": 0,
        "provenance": "DIRECT_BOUNDED_DEPTH_UNRESOLVED_TUBE",
        "transport_source_row_id": None,
        "transport_generator": None,
    }


def build_guard_row(
    chart: str,
    parent_id: str,
    refinement_path: list[str],
    box: Any,
) -> dict[str, Any]:
    payload = [chart, parent_id, refinement_path, box_payload(box)]
    return {
        "row_id": row_id("chart-guard-rejection", payload),
        "chart": chart,
        "parent_id": parent_id,
        "refinement_path": refinement_path,
        "box": box_payload(box),
        "coordinate_volume": qstr(box_volume(box)),
        "exact_rejection_predicate":
            "min_{t in box}|t| gives 2*t^2-1>0",
        "classification":
            "STRICT_OUTSIDE_THIS_TRUE_DOMINANT_SOURCE_CHART",
        "is_CM2_exterior_sheet_exclusion": False,
        "is_Gate5_geometric_disposition": False,
        "provenance": "DIRECT_EXACT_RATIONAL_CHART_DOMAIN_GUARD",
        "transport_source_row_id": None,
        "transport_generator": None,
    }


def recut_parent(
    chart: str,
    leaf: Any,
    tables: dict[str, Any],
) -> dict[str, Any]:
    require(
        leaf.classification == "unique_first"
        and leaf.owner_target is not None,
        "unique parent",
    )
    gate3_row = atlas.leaf_row(chart, leaf)
    parent_id = row_id("gate3-parent", gate3_row)
    base_widths = (
        leaf.box.t1 - leaf.box.t0,
        leaf.box.p1 - leaf.box.p0,
        leaf.box.s1 - leaf.box.s0,
    )
    initial_evaluation = evaluate_cell(
        chart, leaf.box, leaf.owner_target, tables
    )
    pending: list[tuple[Any, list[str], tuple[str, Any]]] = [
        (leaf.box, [], initial_evaluation)
    ]
    resolved: list[dict[str, Any]] = []
    residual: list[dict[str, Any]] = []
    guards: list[dict[str, Any]] = []
    while pending:
        box, path, evaluation = pending.pop()
        kind, data = evaluation
        if kind == "resolved":
            resolved.append(build_resolved_row(
                chart, parent_id, path, box, data
            ))
            continue
        if kind == "guard":
            guards.append(build_guard_row(
                chart, parent_id, path, box
            ))
            continue
        if len(path) >= MAX_DYNAMIC_REFINE_DEPTH:
            residual.append(build_residual_row(
                chart, parent_id, path, box, data
            ))
            continue
        if kind == "source_seam":
            candidate_axes = (0,)
        else:
            candidate_axes = (0, 1, 2)
        options: list[
            tuple[Q, Q, int, int, tuple[Any, Any], list[tuple[str, Any]]]
        ] = []
        widths = (
            box.t1 - box.t0,
            box.p1 - box.p0,
            box.s1 - box.s0,
        )
        for axis_index in candidate_axes:
            children = split_box(box, axis_index)
            evaluations = [
                evaluate_cell(
                    chart, child, leaf.owner_target, tables
                )
                for child in children
            ]
            immediately_released = sum(
                (
                    box_volume(child)
                    for child, child_evaluation
                    in zip(children, evaluations, strict=True)
                    if child_evaluation[0] in {"resolved", "guard"}
                ),
                Q(0),
            )
            relative_width = (
                widths[axis_index] / base_widths[axis_index]
            )
            options.append((
                immediately_released,
                relative_width,
                -axis_index,
                axis_index,
                children,
                evaluations,
            ))
        (
            _released,
            _relative,
            _negative_axis,
            chosen_axis,
            chosen_children,
            chosen_evaluations,
        ) = max(options, key=lambda option: option[:3])
        axis_name = ("t", "p", "s")[chosen_axis]
        for child_index, (child, child_evaluation) in enumerate(
            zip(
                chosen_children,
                chosen_evaluations,
                strict=True,
            )
        ):
            pending.append((
                child,
                [*path, f"{axis_name}{child_index}"],
                child_evaluation,
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
    parent_volume = box_volume(leaf.box)
    require(
        resolved_volume + residual_volume + guard_volume
        == parent_volume,
        "parent volume conservation",
    )
    ordinals = sorted({
        row["official_key_ordinal"] for row in resolved
    })
    if residual_volume == 0:
        completion = (
            "COMPLETE_NONEMPTY_REGULAR_3D_BULK_RECUT__"
            "LOWER_DIMENSIONAL_BOUNDARY_FACES_SEPARATE"
        )
    else:
        completion = (
            "BOUNDED_PARTIAL_NONEMPTY_3D_BULK_RECUT__"
            "POSITIVE_VOLUME_RESIDUAL_TUBES_RETAINED"
        )
    parent = {
        "parent_id": parent_id,
        "chart": chart,
        "leaf_id": leaf.box.path,
        "owner_target": leaf.owner_target,
        "box": box_payload(leaf.box),
        "coordinate_volume": qstr(parent_volume),
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
        "source_grazing_boundary_faces":
            source_grazing_faces(leaf.box),
        "source_chart_seam_half_open_status":
            source_seam_status(chart),
        "gate3_leaf_row_sha256": digest(gate3_row),
    }
    return {
        "parent": parent,
        "resolved": resolved,
        "residual": residual,
        "guards": guards,
    }


def reflected_chart(generator: str, chart: str) -> str:
    require(chart in ALL_G_CHARTS, "source-G chart")
    source, cell = chart.split(":")
    if generator == "Jx":
        cell = {"E": "W", "W": "E", "N": "N", "S": "S"}[cell]
    elif generator == "Jy":
        cell = {"E": "E", "W": "W", "N": "S", "S": "N"}[cell]
    else:
        raise ValueError(generator)
    return f"{source}:{cell}"


def reflected_target(generator: str, value: str) -> str:
    target = first_hit.target_by_id(value)
    if generator == "Jx":
        ix = -target.ix if target.obstacle == "G" else -target.ix - 1
        iy = target.iy
    elif generator == "Jy":
        ix = target.ix
        iy = -target.iy if target.obstacle == "G" else -target.iy - 1
    else:
        raise ValueError(generator)
    return f"{target.obstacle}[{ix},{iy}]"


def reflected_token(generator: str, token: str) -> str:
    if generator == "Jx" and token.startswith("X"):
        return "X+" if token == "X-" else "X-"
    if generator == "Jy" and token.startswith("Y"):
        return "Y+" if token == "Y-" else "Y-"
    return token


def reflected_wall(generator: str, token: str, wall: int) -> int:
    if (
        (generator == "Jx" and token.startswith("X"))
        or (generator == "Jy" and token.startswith("Y"))
    ):
        return -wall
    return wall


def reflected_outgoing(generator: str, cell: str) -> str:
    if generator == "Jx":
        return {"E": "W", "W": "E", "N": "N", "S": "S"}[cell]
    if generator == "Jy":
        return {"E": "E", "W": "W", "N": "S", "S": "N"}[cell]
    raise ValueError(generator)


def reflected_box(
    generator: str,
    values: list[str],
) -> list[str]:
    t0, t1, p0, p1, s0, s1 = map(Q, values)
    if generator == "Jx":
        return [
            qstr(t0), qstr(t1),
            qstr(-p1), qstr(-p0),
            qstr(-s1), qstr(-s0),
        ]
    if generator == "Jy":
        return [
            qstr(t0), qstr(t1),
            qstr(-p1), qstr(-p0),
            qstr(s0), qstr(s1),
        ]
    raise ValueError(generator)


def reflected_reason(generator: str, reason: str) -> str:
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


def reflected_grazing_face(face: str) -> str:
    return {"p=-1": "p=+1", "p=+1": "p=-1"}[face]


def transport_parent(
    source_chart: str,
    destination_chart: str,
    generator: str,
    direct_leaf: Any,
    direct_result: dict[str, Any],
    tables: dict[str, Any],
) -> dict[str, Any]:
    axis = "vertical" if generator == "Jx" else "horizontal"
    reflected_leaf = atlas.reflect_leaf(source_chart, axis, direct_leaf)
    require(
        reflected_leaf.classification == "unique_first"
        and reflected_leaf.owner_target
        == reflected_target(generator, direct_leaf.owner_target),
        "reflected parent owner",
    )
    gate3_row = atlas.leaf_row(destination_chart, reflected_leaf)
    parent_id = row_id("gate3-parent", gate3_row)
    source_parent = direct_result["parent"]
    resolved: list[dict[str, Any]] = []
    for source_row in direct_result["resolved"]:
        events = [
            [
                reflected_token(generator, token),
                reflected_wall(generator, token, wall),
            ]
            for token, wall in source_row["ordered_integer_wall_events"]
        ]
        pattern = tuple(event[0] for event in events)
        target = reflected_target(
            generator, source_row["owner_target"]
        )
        key = official_key(
            destination_chart, target, pattern, tables
        )
        outgoing = reflected_outgoing(
            generator, source_row["outgoing_cell"]
        )
        require(
            key["row"][3] == source_row["roof"]
            and len(events) == source_row["wall_crossing_count"],
            "transport roof/count",
        )
        payload = [
            destination_chart,
            parent_id,
            source_row["refinement_path"],
            reflected_box(generator, source_row["box"]),
            key["identifier"],
            outgoing,
            source_row["row_id"],
        ]
        resolved.append({
            "row_id": row_id("resolved-3d", payload),
            "chart": destination_chart,
            "parent_id": parent_id,
            "refinement_path": source_row["refinement_path"],
            "box": reflected_box(generator, source_row["box"]),
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
        })
        # Applying the same involution again recovers the direct exact key.
        twice_target = reflected_target(generator, target)
        twice_pattern = tuple(
            reflected_token(generator, token) for token in pattern
        )
        twice = official_key(
            source_chart, twice_target, twice_pattern, tables
        )
        require(
            twice["identifier"] == source_row["official_key_id"],
            "transport key involution",
        )
    residual: list[dict[str, Any]] = []
    for source_row in direct_result["residual"]:
        reasons = sorted(
            reflected_reason(generator, reason)
            for reason in source_row["reason_labels"]
        )
        payload = [
            destination_chart,
            parent_id,
            source_row["refinement_path"],
            reflected_box(generator, source_row["box"]),
            reasons,
            source_row["row_id"],
        ]
        residual.append({
            "row_id": row_id("residual-3d-tube", payload),
            "chart": destination_chart,
            "parent_id": parent_id,
            "refinement_path": source_row["refinement_path"],
            "box": reflected_box(generator, source_row["box"]),
            "coordinate_volume": source_row["coordinate_volume"],
            "reason_labels": reasons,
            "ambient_dimension": 3,
            "whole_parent_credit": 0,
            "provenance": "ROUND173_EXACT_ISOMETRIC_TRANSPORT",
            "transport_source_row_id": source_row["row_id"],
            "transport_generator": generator,
        })
    guards: list[dict[str, Any]] = []
    for source_row in direct_result["guards"]:
        payload = [
            destination_chart,
            parent_id,
            source_row["refinement_path"],
            reflected_box(generator, source_row["box"]),
            source_row["row_id"],
        ]
        guards.append({
            "row_id": row_id("chart-guard-rejection", payload),
            "chart": destination_chart,
            "parent_id": parent_id,
            "refinement_path": source_row["refinement_path"],
            "box": reflected_box(generator, source_row["box"]),
            "coordinate_volume": source_row["coordinate_volume"],
            "exact_rejection_predicate":
                "min_{t in box}|t| gives 2*t^2-1>0",
            "classification":
                "STRICT_OUTSIDE_THIS_TRUE_DOMINANT_SOURCE_CHART",
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
        "leaf_id": reflected_leaf.box.path,
        "owner_target": reflected_leaf.owner_target,
        "box": box_payload(reflected_leaf.box),
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
        "bulk_completion_status":
            source_parent["bulk_completion_status"],
        "observed_exact_key_count": len(ordinals),
        "observed_exact_key_ordinals_sha256": digest(ordinals),
        "provenance": "ROUND173_EXACT_ISOMETRIC_TRANSPORT",
        "transport_source_parent_id": source_parent["parent_id"],
        "transport_generator": generator,
        "source_grazing_boundary_faces": sorted(
            reflected_grazing_face(face)
            for face in source_parent["source_grazing_boundary_faces"]
        ),
        "source_chart_seam_half_open_status":
            source_seam_status(destination_chart),
        "gate3_leaf_row_sha256": digest(gate3_row),
    }
    require(
        parent["owner_target"]
        == reflected_target(generator, source_parent["owner_target"])
        and parent["coordinate_volume"]
        == qstr(box_volume(reflected_leaf.box)),
        "transport parent binding",
    )
    return {
        "parent": parent,
        "resolved": resolved,
        "residual": residual,
        "guards": guards,
    }


def predicate_details(reason: str) -> tuple[str, str, str, str]:
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


def make_stratum(
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
        "stratum_id": row_id("stratum", identity_payload),
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


def strata_for_parent(result: dict[str, Any]) -> list[dict[str, Any]]:
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
            reflected_grazing_face(face)
            if generator is not None
            else None
        )
        source_id = (
            row_id("stratum", [
                source_parent, "source_grazing", source_face
            ])
            if source_parent is not None and source_face is not None
            else None
        )
        rows.append(make_stratum(
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
            row_id("stratum", [source_parent, "source_chart_seam"])
            if source_parent is not None
            else None
        )
        rows.append(make_stratum(
            chart=chart,
            parent_id=parent_id,
            residual_id=None,
            identity_payload=[parent_id, "source_chart_seam"],
            predicate_label="source_chart_seam",
            equation="2*t^2-1=0",
            dimension_account="EXACT_DIMENSION_2_GRAPH",
            dimension_certification="CERTIFIED",
            existence_certification="CERTIFIED_PRESENT",
            half_open_owner_status=source_seam_status(chart),
            provenance=provenance,
            source_id=source_id,
            generator=generator,
        ))
        for face in faces:
            source_face = (
                reflected_grazing_face(face)
                if generator is not None
                else None
            )
            source_id = (
                row_id("stratum", [
                    source_parent,
                    "source_chart_seam_source_grazing_intersection",
                    source_face,
                ])
                if source_parent is not None and source_face is not None
                else None
            )
            rows.append(make_stratum(
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
                half_open_owner_status=source_seam_status(chart),
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
            (
                label,
                equation,
                dimension,
                existence,
            ) = predicate_details(reason)
            if generator is not None:
                source_reason = reflected_reason(generator, reason)
                source_id = row_id("stratum", [
                    residual["transport_source_row_id"], source_reason
                ])
            else:
                source_id = None
            rows.append(make_stratum(
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
        for first_reason, second_reason in itertools.combinations(
            reasons, 2
        ):
            ordered_reasons = sorted([first_reason, second_reason])
            if generator is not None:
                source_reasons = sorted([
                    reflected_reason(generator, first_reason),
                    reflected_reason(generator, second_reason),
                ])
                source_id = row_id("stratum", [
                    residual["transport_source_row_id"],
                    "candidate-intersection",
                    source_reasons,
                ])
            else:
                source_id = None
            rows.append(make_stratum(
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


def build_materialized_rows(
    direct_atlases: dict[str, list[Any]],
    tables: dict[str, Any],
) -> dict[str, list[dict[str, Any]]]:
    parents: list[dict[str, Any]] = []
    resolved: list[dict[str, Any]] = []
    residual: list[dict[str, Any]] = []
    guards: list[dict[str, Any]] = []
    strata: list[dict[str, Any]] = []
    for source_chart, destination_chart, generator in (
        ("G:E", "G:W", "Jx"),
        ("G:N", "G:S", "Jy"),
    ):
        unique = [
            leaf for leaf in direct_atlases[source_chart]
            if leaf.classification == "unique_first"
        ]
        for leaf in unique:
            direct_result = recut_parent(source_chart, leaf, tables)
            transported = transport_parent(
                source_chart,
                destination_chart,
                generator,
                leaf,
                direct_result,
                tables,
            )
            for result in (direct_result, transported):
                parents.append(result["parent"])
                resolved.extend(result["resolved"])
                residual.extend(result["residual"])
                guards.extend(result["guards"])
                strata.extend(strata_for_parent(result))
    parents.sort(key=lambda row: (row["chart"], row["leaf_id"]))
    resolved.sort(key=lambda row: row["row_id"])
    residual.sort(key=lambda row: row["row_id"])
    guards.sort(key=lambda row: row["row_id"])
    strata.sort(key=lambda row: row["stratum_id"])
    require(
        len(parents) == 21232
        and len({row["parent_id"] for row in parents}) == len(parents)
        and len({row["row_id"] for row in resolved}) == len(resolved)
        and len({row["row_id"] for row in residual}) == len(residual)
        and len({row["row_id"] for row in guards}) == len(guards)
        and len({row["stratum_id"] for row in strata}) == len(strata),
        "materialized row ID census",
    )
    require(
        sum(row["transport_generator"] is None for row in resolved) * 2
        == len(resolved)
        and sum(row["transport_generator"] is None for row in residual) * 2
        == len(residual)
        and sum(row["transport_generator"] is None for row in guards) * 2
        == len(guards),
        "direct/transport row conservation",
    )
    return {
        "parents": parents,
        "resolved": resolved,
        "residual": residual,
        "guards": guards,
        "strata": strata,
    }


def pack_attachment(
    rows: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    packed = {
        "parent_rows": [
            as_row(PARENT_COLUMNS, row) for row in rows["parents"]
        ],
        "resolved_3d_occurrence_rows": [
            as_row(RESOLVED_COLUMNS, row) for row in rows["resolved"]
        ],
        "residual_3d_tube_rows": [
            as_row(RESIDUAL_COLUMNS, row) for row in rows["residual"]
        ],
        "chart_guard_rejection_rows": [
            as_row(GUARD_COLUMNS, row) for row in rows["guards"]
        ],
        "lower_dimensional_stratum_rows": [
            as_row(STRATUM_COLUMNS, row) for row in rows["strata"]
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


def attachment_bytes(document: dict[str, Any]) -> bytes:
    return (canonical(document) + "\n").encode("utf-8")


def fraction_sum(rows: list[dict[str, Any]], field: str) -> Q:
    return sum((Q(row[field]) for row in rows), Q(0))


def table_statistics(
    rows: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    parents = rows["parents"]
    resolved = rows["resolved"]
    residual = rows["residual"]
    guards = rows["guards"]
    strata = rows["strata"]
    parent_volume = fraction_sum(parents, "coordinate_volume")
    resolved_volume = fraction_sum(resolved, "coordinate_volume")
    residual_volume = fraction_sum(residual, "coordinate_volume")
    guard_volume = fraction_sum(guards, "coordinate_volume")
    require(
        resolved_volume + residual_volume + guard_volume
        == parent_volume,
        "global volume conservation",
    )
    completed = [
        row for row in parents
        if row["residual_coordinate_volume"] == "0"
    ]
    partial = [
        row for row in parents
        if Q(row["residual_coordinate_volume"]) > 0
    ]
    require(
        completed
        and partial
        and len(completed) + len(partial) == len(parents),
        "bounded partial parent split",
    )
    observed_ids = sorted({
        row["official_key_id"] for row in resolved
    })
    observed_ordinals = sorted({
        row["official_key_ordinal"] for row in resolved
    })
    require(len(observed_ids) == len(observed_ordinals), "key ID bijection")
    direct_resolved = [
        row for row in resolved
        if row["transport_generator"] is None
    ]
    direct_ids = sorted({
        row["official_key_id"] for row in direct_resolved
    })
    direct_ordinals = sorted({
        row["official_key_ordinal"] for row in direct_resolved
    })
    require(len(direct_ids) == len(direct_ordinals), "direct key IDs")
    reason_histogram = Counter(
        reason
        for row in residual
        for reason in row["reason_labels"]
    )
    chart_parent_histogram = Counter(row["chart"] for row in parents)
    chart_completed_histogram = Counter(
        row["chart"] for row in completed
    )
    chart_partial_histogram = Counter(row["chart"] for row in partial)
    chart_occurrence_histogram = Counter(
        row["chart"] for row in resolved
    )
    wall_histogram = Counter(
        row["wall_crossing_count"] for row in resolved
    )
    roof_histogram = Counter(row["roof"] for row in resolved)
    outgoing_histogram = Counter(
        row["target_chart"] for row in resolved
    )
    predicate_histogram = Counter(
        row["predicate_label"] for row in strata
    )
    dimension_histogram = Counter(
        row["dimension_account"] for row in strata
    )
    fully_closed_regular = [
        row for row in completed
        if not row["source_grazing_boundary_faces"]
    ]
    return {
        "parent_count": len(parents),
        "completed_nonempty_3d_bulk_parent_count": len(completed),
        "bounded_partial_nonempty_parent_count": len(partial),
        "fully_closed_regular_parent_count":
            len(fully_closed_regular),
        "parent_chart_histogram": dict(sorted(
            chart_parent_histogram.items()
        )),
        "completed_parent_chart_histogram": dict(sorted(
            chart_completed_histogram.items()
        )),
        "partial_parent_chart_histogram": dict(sorted(
            chart_partial_histogram.items()
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
        "direct_resolved_3d_occurrence_row_count":
            len(direct_resolved),
        "transported_resolved_3d_occurrence_row_count":
            len(resolved) - len(direct_resolved),
        "observed_exact_key_count": len(observed_ids),
        "observed_exact_key_ids_sha256": digest(observed_ids),
        "observed_exact_key_ordinals_sha256":
            digest(observed_ordinals),
        "direct_observed_exact_key_count": len(direct_ids),
        "direct_observed_exact_key_ids_sha256": digest(direct_ids),
        "direct_observed_exact_key_ordinals_sha256":
            digest(direct_ordinals),
        "occurrence_row_chart_histogram": dict(sorted(
            chart_occurrence_histogram.items()
        )),
        "wall_crossing_count_histogram": {
            str(key): value
            for key, value in sorted(wall_histogram.items())
        },
        "roof_histogram": {
            str(key): value
            for key, value in sorted(roof_histogram.items())
        },
        "target_outgoing_chart_histogram": dict(sorted(
            outgoing_histogram.items()
        )),
        "residual_reason_histogram": dict(sorted(
            reason_histogram.items()
        )),
        "stratum_predicate_histogram": dict(sorted(
            predicate_histogram.items()
        )),
        "stratum_dimension_account_histogram": dict(sorted(
            dimension_histogram.items()
        )),
    }


def build_certificate_result(
    inputs: dict[str, Any],
    atlas_audit: dict[str, Any],
    rows: dict[str, list[dict[str, Any]]],
    attachment: dict[str, Any],
    attachment_sha256: str,
) -> dict[str, Any]:
    statistics = table_statistics(rows)
    table_census = attachment["result"]["table_census_and_sha256"]
    require(
        statistics["parent_count"] == 21232
        and statistics["positive_volume_residual_tube_coordinate_volume"]
        != "0"
        and statistics["observed_exact_key_count"] > 0,
        "Round174 bounded partial state",
    )
    r173_generators = inputs["r173"]["exact_transport_generators"]
    require(
        [row["generator"] for row in r173_generators] == ["Jx", "Jy"]
        and all(
            row["source_G_ordinal_permutation"]["bijective"] is True
            and row["source_G_ordinal_permutation"]["involutive"] is True
            for row in r173_generators
        ),
        "Round173 transport binding",
    )
    return {
        "status": STATUS,
        "scope": {
            "source_obstacle": "G",
            "Gate3_unique_first_parent_count": 21232,
            "direct_parent_charts": ["G:E", "G:N"],
            "transported_parent_charts": ["G:W", "G:S"],
            "dynamic_materialization_kind":
                "bounded adaptive positive-3D occurrence rows",
            "maximum_additional_dyadic_refine_depth":
                MAX_DYNAMIC_REFINE_DEPTH,
            "all_unique_first_parents_audited": True,
            "all_unique_first_parents_fully_materialized": False,
            "global_geometric_exact_key_dispositions_added": 0,
            "CM2_exterior_sheet_exclusions_added": 0,
        },
        "provenance": {
            "dependency_sha256": PINS,
            "python_flint_version": FLINT_VERSION,
            "Gate3_atlas_precision_bits": ATLAS_PRECISION_BITS,
            "dynamic_recut_precision_bits": DYNAMIC_PRECISION_BITS,
            "Round169_result_sha256": R169_RESULT,
            "Round169_verification_result_sha256":
                R169_VERIFY_RESULT,
            "Round171_result_sha256": R171_RESULT,
            "Round171_verification_result_sha256":
                R171_VERIFY_RESULT,
            "Round173_result_sha256": R173_RESULT,
            "Round173_verification_result_sha256":
                R173_VERIFY_RESULT,
            "old_artifacts_modified": False,
        },
        "independent_direct_Gate3_rebuild": {
            "chart_rows": atlas_audit["rows"],
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
            "source_chart_domain_test":
                "exact rational sign of 2*t^2-1",
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
            "observed_exact_key_count":
                statistics["observed_exact_key_count"],
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
            "file_sha256": attachment_sha256,
            "result_sha256": attachment["result_sha256"],
            "table_census_and_sha256": table_census,
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


def build_all() -> tuple[dict[str, Any], dict[str, Any], bytes]:
    inputs = load_inputs()
    tables = registry_tables(inputs["gate5"])
    direct_atlases = rebuild_direct_atlases()
    atlas_audit = audit_atlases(direct_atlases, inputs["gate3"])
    ctx.prec = DYNAMIC_PRECISION_BITS
    rows = build_materialized_rows(direct_atlases, tables)
    attachment = pack_attachment(rows)
    encoded_attachment = attachment_bytes(attachment)
    attachment_sha256 = hashlib.sha256(encoded_attachment).hexdigest()
    result = build_certificate_result(
        inputs,
        atlas_audit,
        rows,
        attachment,
        attachment_sha256,
    )
    certificate = {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    return certificate, attachment, encoded_attachment


def safe_output(path: Path, protected: list[Path]) -> None:
    parent = path.parent
    require(parent.exists() and parent.is_dir(), "output parent")
    require(not parent.is_symlink(), "output parent symlink")
    candidate = path.resolve(strict=False)
    protected_resolved = [
        protected_path.resolve(strict=False)
        for protected_path in protected
    ]
    require(candidate not in protected_resolved, "protected output")
    if path.exists() or path.is_symlink():
        require(not path.is_symlink(), "output symlink")
        information = path.stat()
        require(stat.S_ISREG(information.st_mode), "output regular")
        require(information.st_nlink == 1, "output hardlink")
        for protected_path in protected:
            if protected_path.exists():
                require(
                    not os.path.samefile(path, protected_path),
                    "output aliases protected",
                )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument(
        "--attachment-output", type=Path, default=ATTACHMENT
    )
    arguments = parser.parse_args()
    protected = [
        Path(__file__).resolve(),
        *[(HERE / name).resolve() for name in PINS],
    ]
    safe_output(arguments.output, [
        *protected, arguments.attachment_output.resolve(strict=False)
    ])
    safe_output(arguments.attachment_output, [
        *protected, arguments.output.resolve(strict=False)
    ])
    require(
        arguments.output.resolve(strict=False)
        != arguments.attachment_output.resolve(strict=False),
        "certificate/attachment distinct",
    )
    certificate, _attachment, encoded_attachment = build_all()
    arguments.attachment_output.write_bytes(encoded_attachment)
    arguments.output.write_text(
        json.dumps(
            certificate,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n",
        encoding="utf-8",
    )
    census = certificate["result"]["materialization_census"]
    print(
        "parents",
        census["completed_nonempty_3d_bulk_parent_count"],
        "complete +",
        census["bounded_partial_nonempty_parent_count"],
        "partial",
    )
    print(
        "occurrence rows",
        census["resolved_3d_occurrence_row_count"],
        "distinct exact keys",
        census["observed_exact_key_count"],
    )
    print(certificate["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
