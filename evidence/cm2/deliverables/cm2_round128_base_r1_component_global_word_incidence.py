#!/usr/bin/env python3
"""Round-128 base-R1 physical-component/global-word incidence certificate.

This producer closes one deliberately narrow crosswalk:

    Round-72 nonempty base-R1 face component
      -> Round-71 base-R1 source/destination path cell
      -> frozen Gate-5 official candidate return-word key.

It does not identify the Round-67 occurrence/owner root with those components.
That second crosswalk remains empty because no recordwise twelve-coordinate
Round-67 owner/path key is materialized.  It also records that the sole
official-word overlap with the Round-121 exact-seed path is physically
disjoint in the common local W:N collision coordinates.

The global candidate registry, the 24 Gate-25 cores, all component IDs, all
path-cell IDs, and the exact-seed coordinate separation are replayed here.
The resulting rows certify incidence and symbolic word membership only; they
are not global domain coverage and are not complete Gate-5 operator blocks.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Iterator

import flint
from flint import ctx

import cm2_gate25_physical_return_core_registry_cert as gate25
import cm2_round121_rank3_exact_seed_three_leg_recut_f5f6 as round121


HERE = Path(__file__).resolve().parent
OUTPUT = HERE / "cm2-round128-base-r1-component-global-word-incidence-2026-07-24.json"
SCHEMA = "cm2.round128.base-r1-component-global-word-incidence.v1"
PRECISION_BITS = 1024

GLOBAL_MANIFEST = "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
GLOBAL_PRODUCER = "cm2_gate5_return_word_three_norm_frontier_cert.py"
FIRST_HIT_PRODUCER = "cm2_gate3_candidate_first_hit_cert.py"
GATE25_MANIFEST = "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json"
GATE25_PRODUCER = "cm2_gate25_physical_return_core_registry_cert.py"
ROUND67_MANIFEST = "cm2-round67-fixed-j-occurrence-owner-root-time-potential-frontier-manifest-2026-07-21.json"
ROUND67_PRODUCER = "cm2_round67_fixed_j_occurrence_owner_root_time_potential_frontier_cert.py"
ROUND68_MANIFEST = "cm2-round68-common-root-all-gate-frontier-manifest-2026-07-21.json"
ROUND68_PRODUCER = "cm2_round68_common_root_all_gate_frontier_cert.py"
ROUND69_MANIFEST = "cm2-round69-base-s-return-incidence-all-gate-manifest-2026-07-21.json"
ROUND69_PRODUCER = "cm2_round69_base_s_return_incidence_all_gate_cert.py"
ROUND71_MANIFEST = "cm2-round71-r1-nonempty-face-germs-manifest-2026-07-21.json"
ROUND71_WITNESSES = "cm2-round71-r1-nonempty-face-witnesses-2026-07-21.json"
ROUND71_PRODUCER = "cm2_round71_r1_nonempty_face_germs_cert.py"
ROUND72_MANIFEST = "cm2-round72-r1-full-atlas-f10-f13-f16-manifest-2026-07-21.json"
ROUND72_FIELDS = "cm2-round72-r1-component-f10-f13-f16-proof-2026-07-21.json"
ROUND72_PRODUCER = "cm2_round72_r1_full_atlas_f10_f13_f16_cert.py"
ROUND72_FIELD_PRODUCER = "cm2_round72_r1_component_f10_f13_f16_generator.py"
ROUND121_CERTIFICATE = "cm2-round121-rank3-exact-seed-three-leg-recut-f5f6-2026-07-23.json"
ROUND121_PRODUCER = "cm2_round121_rank3_exact_seed_three_leg_recut_f5f6.py"
ROUND121_VERIFICATION = "cm2-round121-rank3-exact-seed-three-leg-recut-f5f6-verification-2026-07-23.json"
ROUND127_CERTIFICATE = "cm2-round127-global-return-word-exact-seed-crosswalk-2026-07-24.json"
ROUND127_PRODUCER = "cm2_round127_global_return_word_exact_seed_crosswalk.py"
ROUND127_VERIFIER = "cm2_round127_global_return_word_exact_seed_crosswalk_verifier.py"
ROUND127_VERIFICATION = "cm2-round127-global-return-word-exact-seed-crosswalk-verification-2026-07-24.json"

PINS = {
    GLOBAL_MANIFEST: "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866",
    GLOBAL_PRODUCER: "ddcc250f8700c6a695f96019d9f7824fe98636e20a67685fdc6a3cce77f6d695",
    FIRST_HIT_PRODUCER: "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    GATE25_MANIFEST: "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42",
    GATE25_PRODUCER: "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
    ROUND67_MANIFEST: "97cb410b9e960d8331a37ef9203b040c9b1d86c3ed3d1ba6ba66a28c4e4ff400",
    ROUND67_PRODUCER: "cfb501aff4f321742e3fead9895c596e9105b2a89d064d917646b70c6f91ee8f",
    ROUND68_MANIFEST: "a9dd3e825f384f0a36db2745a8677505fb852a76fef2dd2fb9682bdc4573214f",
    ROUND68_PRODUCER: "b10da56552faf6e7006943cc8229afc6478fe211526c621511922addca63a27d",
    ROUND69_MANIFEST: "08d996d52d6aa8ea3b716a46b51d6ae8f0a6b4b9e24c9fab402afe88059bc838",
    ROUND69_PRODUCER: "17a07346c61920a42eb04e074bc736eb1f78809a4867c130ac7ed86613d67e8f",
    ROUND71_MANIFEST: "fb7fd4233d14834ca6a3efc488c2e8f1fcdf97bdeb410a1b93eda8d9b59d50f9",
    ROUND71_WITNESSES: "3226044b8d0718a0d565c7ff9dd6c4736d2b1d28fa784c46443da92e85b61cc6",
    ROUND71_PRODUCER: "ec5b229a7a624ca37f93884d938e26a5e946ff4254edf24cd9a7e7d98d8c6c72",
    ROUND72_MANIFEST: "4bb012ae54db337cbdaa8cdc02aee55025dd522ccc566a7fb343b57010d4f6f9",
    ROUND72_FIELDS: "12c1f1db87030cf63552621a24ac0ebb1adb39933dc420497b425fb3c1f8e8a9",
    ROUND72_PRODUCER: "bf0a9ced0b66174b100dfe195666312215ce9a873558c48787669e0f77da04f9",
    ROUND72_FIELD_PRODUCER: "20eb60b52acce9173e2685979aa44bd532c02ec10fd2c2d3862a5e10c92d0381",
    ROUND121_CERTIFICATE: "ba56b41a41fbf0d77c6467fcb5fc521ef4d6928f65a9f79d5bba8b83c9b4fc6e",
    ROUND121_PRODUCER: "30c69e1849867841398483749f547a7840d401bc3cc24b9e4ef0a4892ad990ed",
    ROUND121_VERIFICATION: "ec527c19a8c50025514db0769808ce21aeb53c7d1cc64edb75f1a9c5a6aa3e80",
    ROUND127_CERTIFICATE: "4aa7cde5e22883dfcb8e59f16e7bd6ab16c4436229c9964384ef72dda0c16408",
    ROUND127_PRODUCER: "ea461b3ed1301149bca350f32190348aca955f0a04ce42663fab23451144b0dd",
    ROUND127_VERIFIER: "24de0b53c872d43f0a0d7422164e5a2a776a1d35879c923bcf5a07afef94e157",
    ROUND127_VERIFICATION: "5958b4905b8e005886302a6bffc32d15fd1091cf8dbe20b743488e3f91eeb383",
}

EXPECTED_GLOBAL_ROW_STREAM_SHA256 = "841cb96798c9bd41e1440c8b2cdd93af5d80f2f64d693f2aa00175a440045ab9"
EXPECTED_PAIR_ROWS_SHA256 = "ccf4e9e42c7b17f6ebb7f33ec707616bb49ec1d755a817ce141dc92d47056f75"
EXPECTED_PATTERN_ROWS_SHA256 = "2d655b1b83918b0cc42845e465d05f7309657b776f0acbd3d3003e8ae17bb39d"
EXPECTED_MINIMAL_MAPPING_ROWS_SHA256 = "6a19bb49fcde593afc64e14cfb4c25b40151facd92f5cc77e2c11d1239b953b0"
EXPECTED_SUMMARY_ROWS_SHA256 = "69a1b5460325507d1ac7b5949edc636fef6cdb7051b0f8d7c29653a7b7ee7bad"
EXPECTED_OFFICIAL_WORD_IDS_SHA256 = "b1599b17b48895de82be81855ee840382cf2e5c4f65c3b9df7df9c7bae7f7144"
EXPECTED_COMPONENT_WORD_PAIRS_SHA256 = "0cb469f08f007d395cd88a438fd48c44e3835b369be49606689557a84c347d95"


class Round128Error(RuntimeError):
    """Fail-closed producer error."""


def require(condition: Any, label: str) -> None:
    if not bool(condition):
        raise Round128Error(label)


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reject_constant(value: str) -> Any:
    raise Round128Error(f"non-finite JSON constant: {value}")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise Round128Error(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def strict_json(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        parse_constant=reject_constant,
        object_pairs_hook=unique_object,
    )
    require(type(value) is dict, f"JSON object: {path.name}")
    return value


def closed_result(path: Path, schema: str) -> dict[str, Any]:
    document = strict_json(path)
    require(set(document) == {"schema", "result", "result_sha256"}, f"closed envelope: {path.name}")
    require(document["schema"] == schema, f"schema: {path.name}")
    require(document["result_sha256"] == digest(document["result"]), f"result digest: {path.name}")
    require(type(document["result"]) is dict, f"result object: {path.name}")
    return document["result"]


def validate_pins() -> None:
    for name, expected in PINS.items():
        path = HERE / name
        require(path.is_file(), f"missing pin: {name}")
        require(sha256_path(path) == expected, f"byte pin: {name}")


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


# ---------------------------------------------------------------------------
# Independent exact-rational global candidate-word enumeration.

SOURCE_CHARTS = tuple(
    f"{source}:{cell}"
    for source in ("G", "W")
    for cell in ("E", "W", "N", "S")
)
RADIUS = {"G": Q(9, 25), "W": Q(4, 25)}
EPS = Q(1, 400)
TAU_MAX = Q(3)
INV_SQRT2_LOWER = Q(707, 1000)
INV_SQRT2_UPPER = Q(708, 1000)


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


def dominant_support_upper(
    cell: str, x0: Q, x1: Q, y0: Q, y1: Q
) -> Q:
    if cell == "E":
        axis_upper, transverse_abs = x1, max(abs(y0), abs(y1))
    elif cell == "W":
        axis_upper, transverse_abs = -x0, max(abs(y0), abs(y1))
    elif cell == "N":
        axis_upper, transverse_abs = y1, max(abs(x0), abs(x1))
    elif cell == "S":
        axis_upper, transverse_abs = -y0, max(abs(x0), abs(x1))
    else:
        raise Round128Error(f"cell: {cell}")
    if axis_upper >= 0:
        return axis_upper + transverse_abs * INV_SQRT2_UPPER
    return axis_upper * INV_SQRT2_LOWER + transverse_abs * INV_SQRT2_UPPER


def retained(source: str, cell: str, target: Target) -> bool:
    if target.obstacle == source and target.ix == 0 and target.iy == 0:
        return False
    x0, x1, y0, y1 = vector_interval(source, target)
    distance_squared = square_min_abs(x0, x1) + square_min_abs(y0, y1)
    horizon = TAU_MAX + RADIUS[source] + RADIUS[target.obstacle]
    if distance_squared >= horizon * horizon:
        return False
    support_upper = dominant_support_upper(cell, x0, x1, y0, y1)
    return not (support_upper < RADIUS[source] - RADIUS[target.obstacle])


def retained_chart_target_pairs() -> tuple[tuple[str, str], ...]:
    rows: list[tuple[str, str]] = []
    for chart in SOURCE_CHARTS:
        source, cell = chart.split(":")
        for target in TARGETS:
            if retained(source, cell, target):
                rows.append((chart, target.target_id))
    result = tuple(rows)
    require(len(result) == 448 and len(set(result)) == 448, "448 retained pairs")
    return result


def orientation_choices(count: int) -> tuple[int, ...]:
    return (0,) if count == 0 else (-1, 1)


def crossing_patterns() -> Iterator[tuple[str, ...]]:
    for nx in range(5):
        for ny in range(5):
            length = nx + ny
            for sx in orientation_choices(nx):
                for sy in orientation_choices(ny):
                    for x_positions in itertools.combinations(range(length), nx):
                        x_set = set(x_positions)
                        x_token = "X+" if sx > 0 else "X-"
                        y_token = "Y+" if sy > 0 else "Y-"
                        yield tuple(
                            x_token if index in x_set else y_token
                            for index in range(length)
                        )


def registry_row(
    chart_id: str, target_id: str, crossings: tuple[str, ...]
) -> list[Any]:
    return [chart_id, target_id, list(crossings), len(crossings) + 1]


def replay_global_registry(
    manifest: dict[str, Any],
) -> tuple[
    tuple[tuple[str, str], ...],
    tuple[tuple[str, ...], ...],
    dict[tuple[str, str], int],
    dict[tuple[str, ...], int],
    dict[str, Any],
]:
    result = manifest["result"]
    require(result["schema"] == "cm2.gate5.return-word-three-norm-frontier.v1", "global result schema")
    registry = result["immutable_candidate_key_registry"]
    grammar = result["crossing_grammar"]
    pairs = retained_chart_target_pairs()
    patterns = tuple(crossing_patterns())
    require(len(patterns) == 985 and len(set(patterns)) == 985, "985 crossing patterns")
    histogram = dict(sorted(Counter(len(row) for row in patterns).items()))
    require(
        histogram == {0: 1, 1: 4, 2: 12, 3: 28, 4: 60, 5: 120, 6: 200, 7: 280, 8: 280},
        "crossing histogram",
    )
    require(digest(pairs) == EXPECTED_PAIR_ROWS_SHA256, "pair rows digest")
    require(digest(patterns) == EXPECTED_PATTERN_ROWS_SHA256, "pattern rows digest")
    require(grammar["crossing_pattern_rows_sha256"] == EXPECTED_PATTERN_ROWS_SHA256, "manifest pattern digest")
    require(registry["chart_target_pair_rows_sha256"] == EXPECTED_PAIR_ROWS_SHA256, "manifest pair digest")

    stream = hashlib.sha256()
    word_count = 0
    roof_level_count = 0
    for chart_id, target_id in pairs:
        for crossings in patterns:
            row = registry_row(chart_id, target_id, crossings)
            stream.update(canonical(row).encode("utf-8"))
            stream.update(b"\n")
            word_count += 1
            roof_level_count += len(crossings) + 1
    stream_digest = stream.hexdigest()
    require(word_count == registry["candidate_return_word_key_count"] == 441280, "global word count")
    require(
        roof_level_count
        == registry["prefix_suffix_factor_contract"]["roof_level_prefix_suffix_factor_pair_count"]
        == 3286976,
        "global roof-level count",
    )
    require(stream_digest == registry["candidate_word_key_rows_sha256"], "manifest row-stream digest")
    require(stream_digest == EXPECTED_GLOBAL_ROW_STREAM_SHA256, "frozen row-stream digest")

    pair_index = {row: index for index, row in enumerate(pairs)}
    pattern_index = {row: index for index, row in enumerate(patterns)}
    require(len(pair_index) == 448 and len(pattern_index) == 985, "registry index uniqueness")
    replay = {
        "source_chart_count": 8,
        "target_lift_count": 162,
        "retained_chart_target_pair_count": 448,
        "crossing_pattern_count_per_pair": 985,
        "candidate_return_word_key_count": 441280,
        "roof_level_prefix_suffix_pair_count": 3286976,
        "chart_target_pair_rows_sha256": EXPECTED_PAIR_ROWS_SHA256,
        "crossing_pattern_rows_sha256": EXPECTED_PATTERN_ROWS_SHA256,
        "candidate_word_row_stream_sha256": stream_digest,
        "enumeration_independently_reimplemented_with_exact_rationals": True,
    }
    return pairs, patterns, pair_index, pattern_index, replay


def official_word(
    core: "Core",
    pair_index: dict[tuple[str, str], int],
    pattern_index: dict[tuple[str, ...], int],
) -> tuple[list[Any], int, int, int, str]:
    pair = (core.chart_id, core.target_id)
    require(pair in pair_index, f"retained pair: {pair}")
    require(core.crossings in pattern_index, f"crossing record: {core.crossings}")
    pair_ordinal = pair_index[pair]
    pattern_ordinal = pattern_index[core.crossings]
    ordinal = pair_ordinal * 985 + pattern_ordinal
    row = registry_row(core.chart_id, core.target_id, core.crossings)
    identifier = f"gate5-word:{ordinal:06d}:{digest(row)}"
    return row, pair_ordinal, pattern_ordinal, ordinal, identifier


# ---------------------------------------------------------------------------
# Independent frozen Gate-25 core reconstruction.


@dataclass(frozen=True)
class Core:
    chart_id: str
    t0: Q
    t1: Q
    p0: Q
    p1: Q
    target_id: str
    crossings: tuple[str, ...]
    family: str

    @property
    def source(self) -> str:
        return self.chart_id.split(":")[0]


def physical_cores() -> tuple[Core, ...]:
    rows: list[Core] = []
    axis_targets = {
        "E": (1, 0, "X+"),
        "W": (-1, 0, "X-"),
        "N": (0, 1, "Y+"),
        "S": (0, -1, "Y-"),
    }
    for source in ("G", "W"):
        for cell in ("E", "W", "N", "S"):
            ix, iy, token = axis_targets[cell]
            rows.append(
                Core(
                    f"{source}:{cell}",
                    Q(1, 100),
                    Q(1, 50),
                    -Q(1, 500),
                    Q(1, 500),
                    f"{source}[{ix},{iy}]",
                    () if source == "G" else (token,),
                    "axis_translate",
                )
            )
    diagonal_data = {
        "G": {
            "NE": (("E", 1), ("N", 1), "W[0,0]"),
            "NW": (("W", 1), ("N", -1), "W[-1,0]"),
            "SE": (("E", -1), ("S", 1), "W[0,-1]"),
            "SW": (("W", -1), ("S", -1), "W[-1,-1]"),
        },
        "W": {
            "NE": (("E", 1), ("N", 1), "G[1,1]"),
            "NW": (("W", 1), ("N", -1), "G[0,1]"),
            "SE": (("E", -1), ("S", 1), "G[1,0]"),
            "SW": (("W", -1), ("S", -1), "G[0,0]"),
        },
    }
    for source in ("G", "W"):
        for direction in ("NE", "NW", "SE", "SW"):
            first, second, target_id = diagonal_data[source][direction]
            for cell, sign in (first, second):
                t0, t1 = (
                    (Q(69, 100), Q(7, 10))
                    if sign > 0
                    else (-Q(7, 10), -Q(69, 100))
                )
                rows.append(
                    Core(
                        f"{source}:{cell}",
                        t0,
                        t1,
                        -Q(1, 50),
                        Q(1, 50),
                        target_id,
                        (),
                        f"diagonal_{direction}",
                    )
                )
    rows.sort(
        key=lambda row: (
            row.chart_id,
            row.target_id,
            row.crossings,
            row.t0,
            row.t1,
            row.p0,
            row.p1,
        )
    )
    require(len(rows) == 24, "24 reconstructed cores")
    return tuple(rows)


def core_payload(core: Core) -> dict[str, Any]:
    return {
        "chart_id": core.chart_id,
        "t": [qstr(core.t0), qstr(core.t1)],
        "p": [qstr(core.p0), qstr(core.p1)],
        "target_id": core.target_id,
        "crossings": list(core.crossings),
    }


def core_id(core: Core) -> str:
    return "core:" + digest(core_payload(core))


def face_id(core: Core, side: str) -> str:
    require(side in {"t_lower", "t_upper", "p_lower", "p_upper"}, "core face side")
    coordinate = side[0]
    value = (
        core.t0
        if side == "t_lower"
        else core.t1
        if side == "t_upper"
        else core.p0
        if side == "p_lower"
        else core.p1
    )
    return "physical-core-face:" + digest(
        {
            "core_id": core_id(core),
            "core_chart_id": core.chart_id,
            "core_source_obstacle": core.source,
            "side": side,
            "coordinate": coordinate,
            "coordinate_value": qstr(value),
            "outward_normal_sign": -1 if side.endswith("lower") else 1,
        }
    )


def replay_gate25_cores(
    manifest: dict[str, Any],
    pair_index: dict[tuple[str, str], int],
    pattern_index: dict[tuple[str, ...], int],
) -> tuple[tuple[Core, ...], dict[str, Any]]:
    cores = physical_cores()
    upstream = gate25.physical_cores()
    require(len(upstream) == len(cores) == 24, "upstream core count")
    for index, (ours, theirs) in enumerate(zip(cores, upstream)):
        require(
            (
                ours.chart_id,
                ours.t0,
                ours.t1,
                ours.p0,
                ours.p1,
                ours.target_id,
                ours.crossings,
                ours.family,
            )
            == (
                theirs.chart_id,
                theirs.t0,
                theirs.t1,
                theirs.p0,
                theirs.p1,
                theirs.target_id,
                theirs.crossings,
                theirs.family,
            ),
            f"independent core equality: {index}",
        )

    physical = gate25.physical_registry()
    frozen = manifest["result"]["physical_return_core_registry"]
    require(physical["rows_sha256"] == frozen["rows_sha256"], "Gate25 physical rows digest")
    require(
        physical["distinct_key_rows_sha256"] == frozen["distinct_key_rows_sha256"],
        "Gate25 key rows digest",
    )
    require(frozen["physical_compact_homogeneous_core_count"] == 24, "Gate25 core count")
    require(frozen["all_24_keys_members_of_frozen_441280_envelope"] is True, "Gate25 memberships")
    require(
        frozen["all_cores_strict_first_hit_against_complete_retained_candidate_list"] is True,
        "Gate25 strict first hit",
    )
    require(frozen["all_wall_records_physically_replayed"] is True, "Gate25 wall replay")

    key_rows = []
    official_ids = []
    for core in cores:
        row, _pair, _pattern, _ordinal, identifier = official_word(
            core, pair_index, pattern_index
        )
        key_rows.append(canonical(row))
        official_ids.append(identifier)
    require(len(set(key_rows)) == len(key_rows) == 24, "24 distinct core word keys")
    require(
        digest(sorted(key_rows)) == frozen["distinct_key_rows_sha256"],
        "independent Gate25 key digest",
    )
    replay = {
        "physical_core_count": 24,
        "distinct_official_word_key_count": 24,
        "core_payload_rows_sha256": digest([core_payload(core) for core in cores]),
        "core_ids_sha256": digest([core_id(core) for core in cores]),
        "distinct_key_rows_sha256": frozen["distinct_key_rows_sha256"],
        "upstream_full_Arb_physical_rows_sha256": frozen["rows_sha256"],
        "all_cores_strict_first_hit": True,
        "all_cores_members_of_global_candidate_registry": True,
        "core_definitions_independently_reconstructed": True,
    }
    return cores, replay


# ---------------------------------------------------------------------------
# Round-71/Round-72 component incidence.


def witness_component_id(witness: dict[str, Any]) -> str:
    return "physical-r1-face-component:" + digest(
        {
            "candidate_family_id": witness["candidate_family_id"],
            "base_parameter": "s=0",
            "witness_minus": witness["witness_minus"],
            "witness_plus": witness["witness_plus"],
        }
    )


def path_cell_id(source_core_id: str, destination_core_id: str) -> str:
    return "base-r1-edge-cell:" + digest(
        {
            "source_core_id": source_core_id,
            "destination_core_id": destination_core_id,
            "s": "0",
        }
    )


def closed_row(row: dict[str, Any]) -> dict[str, Any]:
    require("row_sha256" not in row, "row already closed")
    result = dict(row)
    result["row_sha256"] = digest(result)
    return result


def component_incidence(
    round71_manifest: dict[str, Any],
    round71_witnesses: dict[str, Any],
    round72_manifest: dict[str, Any],
    round72_fields: dict[str, Any],
    cores: tuple[Core, ...],
    pair_index: dict[tuple[str, str], int],
    pattern_index: dict[tuple[str, ...], int],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    r71 = round71_manifest["result"]
    r72 = round72_manifest["result"]
    require(r71["schema"] == "cm2.round71.r1-nonempty-face-germs.v1", "Round71 schema")
    require(r72["schema"] == "cm2.round72.r1-full-atlas-f10-f13-f16.v1", "Round72 schema")
    require(round71_witnesses["schema"] == "cm2.round71.r1-nonempty-face-witnesses.v1", "witness schema")
    require(round72_fields["schema"] == "cm2.round72.r1-component-f10-f13-f16.v1", "field schema")

    component_rows = r71["base_fibre_nonempty_face_witness_registry"]["component_rows"]
    field_rows = r72["numeric_local_field_registry"]["component_field_rows"]
    proof_rows = round72_fields["result"]["rows"]
    witnesses = round71_witnesses["rows"]
    require(len(component_rows) == len(field_rows) == len(proof_rows) == len(witnesses) == 32, "32 row inputs")

    component_map = {row["component_id"]: row for row in component_rows}
    field_map = {row["component_id"]: row for row in field_rows}
    proof_map = {row["component_id"]: row for row in proof_rows}
    witness_map = {witness_component_id(row): row for row in witnesses}
    identifiers = set(component_map)
    require(
        identifiers == set(field_map) == set(proof_map) == set(witness_map)
        and len(identifiers) == 32,
        "same 32 component IDs",
    )
    require(
        r72["numeric_local_field_registry"]["component_field_rows_sha256"]
        == round72_fields["result"]["rows_sha256"]
        == digest(proof_rows),
        "Round72 field rows digest",
    )
    require(field_rows == proof_rows, "manifest/proof field row byte-value equality")

    incidence_rows: list[dict[str, Any]] = []
    minimal_rows: list[dict[str, Any]] = []
    source_projection_minimal_rows: list[dict[str, Any]] = []
    grouped: dict[
        tuple[str, str, int, int, int, str, str, int, int, int, str, str, str, str, str],
        list[tuple[str, str]],
    ] = defaultdict(list)
    core_use = Counter()

    for component_identifier in sorted(identifiers):
        component = component_map[component_identifier]
        field = field_map[component_identifier]
        witness = witness_map[component_identifier]
        require(component["candidate_family_id"] == field["candidate_family_id"], "candidate family R71/R72")
        require(component["candidate_family_id"] == witness["candidate_family_id"], "candidate family witness")
        require(field["source_core_index"] == witness["source_core_index"], "source core index")
        source_index = field["source_core_index"]
        destination_index = witness["destination_core_index"]
        require(type(source_index) is int and 0 <= source_index < 24, "source core index range")
        require(type(destination_index) is int and 0 <= destination_index < 24, "destination core index range")
        source = cores[source_index]
        destination = cores[destination_index]
        source_identifier = core_id(source)
        destination_identifier = core_id(destination)
        require(component["source_core_id"] == witness["source_core_id"] == source_identifier, "source core ID")
        require(
            component["destination_core_id"] == witness["destination_core_id"] == destination_identifier,
            "destination core ID",
        )
        require(
            component["destination_face_id"] == witness["destination_face_id"]
            == face_id(destination, witness["side"]),
            "destination face ID",
        )
        expected_path = path_cell_id(source_identifier, destination_identifier)
        require(component["path_cell_id"] == expected_path, "path cell ID")
        require(component["time_j"] == 1 and component["connected_rank"] == 0, "time/rank")
        require(
            component["incidence_relation"]
            == "TERMINAL_CORE_PREIMAGE_FACE_GERM_INCIDENT_TO_BASE_R1_EDGE_CELL",
            "typed incidence relation",
        )
        traces = component["trace_rows"]
        require(
            [row["side_label"] for row in traces] == ["inside", "outside"],
            "trace side labels",
        )
        for trace in traces:
            require(
                trace["trace_id"]
                == "physical-r1-trace:"
                + digest(
                    {
                        "component_id": component_identifier,
                        "side": trace["side_label"],
                    }
                ),
                "trace ID",
            )

        (
            source_word_row,
            source_word_pair_index,
            source_word_pattern_index,
            source_word_ordinal,
            source_word_identifier,
        ) = official_word(
            source, pair_index, pattern_index
        )
        (
            destination_word_row,
            destination_word_pair_index,
            destination_word_pattern_index,
            destination_word_ordinal,
            destination_word_identifier,
        ) = official_word(destination, pair_index, pattern_index)
        require(
            source.crossings == destination.crossings == ()
            and source_word_row[3] == destination_word_row[3] == 1,
            "Round72 source and destination word roofs one",
        )
        core_use[source_index] += 1
        stable_key = [
            "round128-base-r1-component-directed-word-incidence-v2",
            component_identifier,
            expected_path,
            source_word_identifier,
            destination_word_identifier,
        ]
        row = {
            "incidence_row_id": "round128-component-word-incidence:" + digest(stable_key),
            "component_id": component_identifier,
            "candidate_family_id": component["candidate_family_id"],
            "source_core_index": source_index,
            "source_core_index_is_not_the_immutable_key": True,
            "source_core_id": source_identifier,
            "source_core_payload": core_payload(source),
            "destination_core_index": destination_index,
            "destination_core_id": destination_identifier,
            "destination_face_id": component["destination_face_id"],
            "path_cell_id": expected_path,
            "base_parameter": "s=0",
            "time_j": 1,
            "connected_rank": 0,
            "trace_rows": traces,
            "component_face_side": field["side"],
            "component_coordinate_germ": {
                "t_center": field["t_center"],
                "t_radius": field["t_radius"],
                "p_center": field["p_center"],
                "p_bracket_radius": field["p_bracket_radius"],
                "s_radius": field["s_radius"],
            },
            "numeric_local_fields": {
                "F10_integer_upper": field["F10_integer_upper"],
                "F13_current_variation_strict_upper": field[
                    "F13_current_variation_strict_upper"
                ],
                "F16_Piola_flux_cost_strict_upper": field[
                    "F16_Piola_flux_cost_strict_upper"
                ],
            },
            "source_official_word_row": source_word_row,
            "source_official_word_pair_index": source_word_pair_index,
            "source_crossing_pattern_index": source_word_pattern_index,
            "source_official_word_ordinal": source_word_ordinal,
            "source_official_word_key_id": source_word_identifier,
            "destination_official_word_row": destination_word_row,
            "destination_official_word_pair_index": destination_word_pair_index,
            "destination_crossing_pattern_index": destination_word_pattern_index,
            "destination_official_word_ordinal": destination_word_ordinal,
            "destination_official_word_key_id": destination_word_identifier,
            "source_and_destination_roof_level_count": 1,
            "source_and_destination_roof_level_j": 0,
            "numeric_F10_F13_F16_attachment_role": "source_official_word",
            "incidence_semantics": (
                "terminal physical face germ is incident to this exact base-R1 "
                "directed path cell; F10/F13/F16 attach to its source official "
                "word and the destination official word is separately registered"
            ),
            "face_is_not_identified_with_path_interior_point": True,
            "source_round71_component_row_sha256": digest(component),
            "source_round72_field_row_sha256": digest(field),
        }
        incidence_rows.append(closed_row(row))
        minimal_rows.append(
            {
                "path_cell_id": expected_path,
                "source_core_id": source_identifier,
                "destination_core_id": destination_identifier,
                "source_official_word_row": source_word_row,
                "source_official_word_key_id": source_word_identifier,
                "destination_official_word_row": destination_word_row,
                "destination_official_word_key_id": destination_word_identifier,
                "component_id": component_identifier,
                "candidate_family_id": component["candidate_family_id"],
                "time_j": 1,
                "connected_rank": 0,
            }
        )
        source_projection_minimal_rows.append(
            {
                "path_cell_id": expected_path,
                "source_core_id": source_identifier,
                "destination_core_id": destination_identifier,
                "word_key_row": source_word_row,
                "official_word_key_id": source_word_identifier,
                "component_id": component_identifier,
                "candidate_family_id": component["candidate_family_id"],
                "time_j": 1,
                "connected_rank": 0,
            }
        )
        grouped[
            (
                source_word_identifier,
                canonical(source_word_row),
                source_word_pair_index,
                source_word_pattern_index,
                source_word_ordinal,
                destination_word_identifier,
                canonical(destination_word_row),
                destination_word_pair_index,
                destination_word_pattern_index,
                destination_word_ordinal,
                expected_path,
                source_identifier,
                destination_identifier,
                str(source_index),
                str(destination_index),
            )
        ].append((component_identifier, row["incidence_row_id"]))

    incidence_rows.sort(
        key=lambda row: (row["source_official_word_key_id"], row["component_id"])
    )
    minimal_rows.sort(
        key=lambda row: (row["source_official_word_key_id"], row["component_id"])
    )
    source_projection_minimal_rows.sort(
        key=lambda row: (row["official_word_key_id"], row["component_id"])
    )
    require(
        digest(source_projection_minimal_rows) == EXPECTED_MINIMAL_MAPPING_ROWS_SHA256,
        "source-projection minimal mapping digest",
    )
    require(len(core_use) == 16 and set(core_use.values()) == {2}, "16 cores times two components")

    edge_rows: list[dict[str, Any]] = []
    source_projection_summary_rows: list[dict[str, Any]] = []
    for (
        source_word_identifier,
        source_word_row_json,
        source_word_pair_index,
        source_word_pattern_index,
        source_word_ordinal,
        destination_word_identifier,
        destination_word_row_json,
        destination_word_pair_index,
        destination_word_pattern_index,
        destination_word_ordinal,
        path_identifier,
        source_identifier,
        destination_identifier,
        source_index_string,
        destination_index_string,
    ), component_pairs in sorted(grouped.items()):
        source_word_row = json.loads(source_word_row_json)
        destination_word_row = json.loads(destination_word_row_json)
        components = sorted(identifier for identifier, _row_id in component_pairs)
        row_ids = sorted(row_id for _identifier, row_id in component_pairs)
        require(len(components) == 2, "two components per edge")
        edge_key = [
            "round128-base-r1-directed-word-to-word-edge-v2",
            source_identifier,
            destination_identifier,
            path_identifier,
            source_word_identifier,
            destination_word_identifier,
        ]
        source_index = int(source_index_string)
        destination_index = int(destination_index_string)
        edge = {
            "edge_row_id": "round128-directed-word-to-word-edge:" + digest(edge_key),
            "source_core_index": source_index,
            "source_core_id": source_identifier,
            "destination_core_index": destination_index,
            "destination_core_id": destination_identifier,
            "path_cell_id": path_identifier,
            "source_official_word_row": source_word_row,
            "source_official_word_pair_index": source_word_pair_index,
            "source_crossing_pattern_index": source_word_pattern_index,
            "source_official_word_ordinal": source_word_ordinal,
            "source_official_word_key_id": source_word_identifier,
            "destination_official_word_row": destination_word_row,
            "destination_official_word_pair_index": destination_word_pair_index,
            "destination_crossing_pattern_index": destination_word_pattern_index,
            "destination_official_word_ordinal": destination_word_ordinal,
            "destination_official_word_key_id": destination_word_identifier,
            "source_and_destination_roof_level_count": 1,
            "component_count": 2,
            "component_ids": components,
            "component_incidence_row_ids": row_ids,
            "numeric_F10_F13_F16_attachment_role": "source_official_word",
            "edge_semantics": (
                "two connected terminal-preimage face components are incident "
                "to one certified positive directed base-R1 path cell; the "
                "source and destination official words are distinct registered roles"
            ),
        }
        edge_rows.append(closed_row(edge))
        source_projection_summary_rows.append(
            {
                "official_word_key_id": source_word_identifier,
                "word_key_row": source_word_row,
                "path_cell_id": path_identifier,
                "source_core_id": source_identifier,
                "destination_core_id": destination_identifier,
                "component_count": 2,
                "component_ids": components,
            }
        )
    edge_rows.sort(key=lambda row: row["source_official_word_key_id"])
    source_projection_summary_rows.sort(key=lambda row: row["official_word_key_id"])
    require(
        len(edge_rows) == len(source_projection_summary_rows) == 16,
        "16 directed word-to-word edge rows",
    )
    require(
        digest(source_projection_summary_rows) == EXPECTED_SUMMARY_ROWS_SHA256,
        "source-projection summary rows digest",
    )
    source_official_ids = sorted(
        row["source_official_word_key_id"] for row in edge_rows
    )
    destination_official_ids = sorted(
        row["destination_official_word_key_id"] for row in edge_rows
    )
    require(len(set(source_official_ids)) == 16, "16 source official IDs")
    require(
        digest(source_official_ids) == EXPECTED_OFFICIAL_WORD_IDS_SHA256,
        "source official ID digest",
    )
    require(
        set(source_official_ids) == set(destination_official_ids),
        "source/destination official word sets agree",
    )
    component_source_word_pairs = sorted(
        [row["component_id"], row["source_official_word_key_id"]]
        for row in incidence_rows
    )
    require(
        digest(component_source_word_pairs) == EXPECTED_COMPONENT_WORD_PAIRS_SHA256,
        "component/source-word pair digest",
    )

    reciprocal_groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for edge in edge_rows:
        reciprocal_groups[
            tuple(sorted([edge["source_core_id"], edge["destination_core_id"]]))
        ].append(edge)
    require(len(reciprocal_groups) == 8, "eight unordered reciprocal core pairs")
    reciprocal_pair_rows: list[dict[str, Any]] = []
    for unordered_core_ids, directed_edges in sorted(reciprocal_groups.items()):
        require(len(directed_edges) == 2, "two directed edges per reciprocal pair")
        first, second = directed_edges
        require(
            first["source_core_id"] == second["destination_core_id"]
            and first["destination_core_id"] == second["source_core_id"],
            "exact reverse core directions",
        )
        require(
            first["source_official_word_key_id"]
            == second["destination_official_word_key_id"]
            and first["destination_official_word_key_id"]
            == second["source_official_word_key_id"],
            "exact reverse official-word directions",
        )
        pair_key = [
            "round128-base-r1-reciprocal-directed-word-pair-v1",
            list(unordered_core_ids),
            sorted(edge["edge_row_id"] for edge in directed_edges),
        ]
        reciprocal_pair_rows.append(
            closed_row(
                {
                    "reciprocal_pair_id": "round128-reciprocal-word-pair:"
                    + digest(pair_key),
                    "unordered_core_ids": list(unordered_core_ids),
                    "directed_edge_row_ids": sorted(
                        edge["edge_row_id"] for edge in directed_edges
                    ),
                    "directed_source_official_word_key_ids": sorted(
                        edge["source_official_word_key_id"]
                        for edge in directed_edges
                    ),
                    "exactly_two_reverse_directions": True,
                }
            )
        )

    ledger = {
        "status": "CERTIFIED_32_BASE_R1_COMPONENT_INCIDENCES_TO_16_DIRECTED_WORD_TO_WORD_EDGES",
        "component_incidence_row_count": 32,
        "directed_source_destination_word_edge_count": 16,
        "reciprocal_unordered_word_pair_count": 8,
        "distinct_path_cell_count": 16,
        "distinct_source_official_word_count": 16,
        "distinct_destination_official_word_count": 16,
        "source_and_destination_official_word_sets_equal": True,
        "components_per_edge": 2,
        "all_source_and_destination_word_roofs": 1,
        "all_roof_level_indices": [0],
        "all_base_parameters": ["s=0"],
        "all_times_j": [1],
        "all_connected_ranks": [0],
        "component_incidence_rows_sha256": digest(incidence_rows),
        "source_destination_word_edge_rows_sha256": digest(edge_rows),
        "reciprocal_pair_rows_sha256": digest(reciprocal_pair_rows),
        "minimal_mapping_rows_sha256": digest(minimal_rows),
        "source_projection_summary_rows_sha256": digest(source_projection_summary_rows),
        "source_official_word_ids_sha256": digest(source_official_ids),
        "destination_official_word_ids_sha256": digest(destination_official_ids),
        "component_source_word_pairs_sha256": digest(component_source_word_pairs),
        "numeric_F10_F13_F16_attachment_role": "source_official_word",
        "word_membership_is_not_domain_measure_or_global_coverage": True,
        "incidence_is_not_face_path_point_equality": True,
        "source_core_index_is_replayed_but_core_id_and_payload_are_immutable": True,
    }
    return incidence_rows, edge_rows, reciprocal_pair_rows, minimal_rows, ledger


# ---------------------------------------------------------------------------
# Round-67 fail-closed owner-root ledger and Round-121 separation.


def identifier_strings(value: Any) -> list[str]:
    rows: list[str] = []
    pattern = re.compile(
        r"^(?:restriction:|rn-restriction:|core:|physical-r1-face-component:"
        r"|base-r1-edge-cell:|path-cell:|gate5-word:)"
    )

    def visit(node: Any) -> None:
        if isinstance(node, dict):
            for child in node.values():
                visit(child)
        elif isinstance(node, list):
            for child in node:
                visit(child)
        elif isinstance(node, str) and pattern.match(node):
            rows.append(node)

    visit(value)
    return rows


def round67_fail_closed_ledger(
    round67_manifest: dict[str, Any],
    round68_manifest: dict[str, Any],
    round69_manifest: dict[str, Any],
) -> dict[str, Any]:
    fixed = round67_manifest["result"]["actual_fixed_j_subroot"]
    require(fixed["status"] == "CERTIFIED_GRAPH_SUPPORTED_PHYSICAL_SUBROOT", "Round67 root")
    require(
        fixed["base_law"] == "finite standard-Borel endpoint-coarea occurrence law m_occ",
        "Round67 occurrence law",
    )
    require(
        "OWNER_TO_EXACT_RETURN_GRAPH_PATH_COMPONENT"
        in round67_manifest["result"]["minimal_spanning_registry"]["open_edges"],
        "Round67 owner/path edge open",
    )
    require(identifier_strings(round67_manifest["result"]) == [], "Round67 has no materialized ID rows")

    common = round68_manifest["result"]["common_root_join"]
    required_fields = [
        "restriction_id",
        "return_component",
        "insertion_time",
        "collision_index",
        "event_signature",
        "primitive_key",
        "owner_key",
        "rank_zero_component",
        "plaque_side",
        "word_cell",
        "endpoint_coordinate",
        "root_coordinate",
    ]
    require(common["required_fields"] == required_fields, "Round68 twelve-field key")
    require(common["actual_joined_fields"] == "0/12", "Round68 zero joined fields")
    require(
        common["status"] == "EXACT_JOIN_CRITERION_CERTIFIED__ACTUAL_CROSSWALK_ABSENT",
        "Round68 absent crosswalk",
    )

    obstruction = round69_manifest["result"]["direct_equality_obstruction"]
    correction = round69_manifest["result"]["typed_incidence_correction"]
    require(obstruction["selected_base_root_occurrence_pair_count"] == 11264, "Round69 pair audit")
    require(obstruction["selected_base_root_occurrence_intersection_count"] == 0, "Round69 empty equality")
    require(obstruction["recordwise_source_point_equality_is_correct_join"] is False, "Round69 typed join")
    require(correction["node_sorts"] == ["path_cell", "physical_face", "one_sided_trace"], "typed nodes")
    require(
        correction["edge_semantics"]
        == "FACE_IS_BOUNDARY_OR_PULLBACK_CARRIER_INCIDENT_TO_PATH_CELL__NOT_EQUAL_TO_INTERIOR_POINT",
        "typed edge",
    )

    return {
        "status": "NOT_CERTIFIED__ROUND67_OCCURRENCE_OWNER_TO_BASE_R1_COMPONENT_CROSSWALK_0_ROWS",
        "round67_fixed_j_root_status": fixed["status"],
        "round67_materialized_recordwise_identifier_count": 0,
        "round67_to_round72_component_crosswalk_row_count": 0,
        "required_recordwise_composite_key_fields": required_fields,
        "required_recordwise_composite_key_field_count": 12,
        "currently_joined_required_fields": "0/12",
        "missing_required_fields": required_fields,
        "round67_declared_retained_key_schema": fixed["retained_keys"],
        "direct_source_point_equality_pair_audit_count": 11264,
        "direct_source_point_equality_intersection_count": 0,
        "correct_join_type": "typed physical-face incidence to path cell",
        "equal_time_j_connected_rank_or_names_are_not_recordwise_key_equality": True,
        "round72_side_is_a_coordinate_face_side_not_a_Round67_plaque_side": True,
        "round72_candidate_family_id_is_not_silently_promoted_to_primitive_key": True,
        "round71_source_or_destination_core_id_is_not_silently_promoted_to_owner_key": True,
        "minimum_new_object": (
            "a nonempty deterministic Borel typed-incidence graph Gamma contained in "
            "Omega_1 x physical_face x path_cell, carrying all twelve recordwise "
            "coordinates plus component/core/path/official-word IDs and an exact "
            "endpoint/root-to-(s,t,p) coordinate map"
        ),
    }


def exact_seed_overlap_and_separation(
    incidence_rows: list[dict[str, Any]],
    cores: tuple[Core, ...],
    pair_index: dict[tuple[str, str], int],
    pattern_index: dict[tuple[str, ...], int],
    precision_bits: int,
) -> dict[str, Any]:
    certificate = closed_result(
        HERE / ROUND121_CERTIFICATE,
        "cm2.round121.rank3-exact-seed-three-leg-recut-f5f6.v1",
    )
    verification = closed_result(
        HERE / ROUND121_VERIFICATION,
        "cm2.round121.rank3-exact-seed-three-leg-recut-f5f6-verification.v1",
    )
    require(verification["verdict"] == "PASS", "Round121 verification PASS")
    require(verification["certificate_sha256"] == PINS[ROUND121_CERTIFICATE], "Round121 verification cert pin")
    exact_words = certificate["whole_seed_owner_candidate_replay"]["official_word_key_ids"]
    require(len(exact_words) == 3 and len(set(exact_words)) == 3, "three exact-seed words")

    incidence_words = {row["source_official_word_key_id"] for row in incidence_rows}
    overlap = sorted(incidence_words & set(exact_words))
    expected_overlap = [
        "gate5-word:346720:53f03ff6fc716b0187c62b5e3cc7971c9e030686426d13ff5eee585f33daeb3e"
    ]
    require(overlap == expected_overlap, "unique exact-seed word overlap")
    overlap_rows = [
        row
        for row in incidence_rows
        if row["source_official_word_key_id"] == overlap[0]
    ]
    require(
        [row["component_id"] for row in overlap_rows]
        == [
            "physical-r1-face-component:5665deaf6fe5dc6163676aa73a59b5de27e6fe71adb067c2cabc12bdbe819b6d",
            "physical-r1-face-component:6414b54d08832086e74ced78c1e7c7052092194e12daa89b744f5b3cccf8b214",
        ],
        "overlap component IDs",
    )
    overlap_destination_words = sorted(
        {row["destination_official_word_key_id"] for row in overlap_rows}
    )
    require(
        overlap_destination_words
        == [
            "gate5-word:102440:cbb373c48bf58a17e8d26dc1623681635b9ea131f736d43871304579b0e30e16"
        ],
        "overlap edge destination is word 102440",
    )
    require(
        exact_words
        == [
            "gate5-word:102441:3ef7afa1895a984d7edeab7005cfcb7daed7ae8aa07f0767bdd9144da94749ba",
            overlap[0],
            "gate5-word:180256:564ba69e20fe29980fb28d97a50efa2326d024c92c36c930bdb4a2157c3335c8",
        ],
        "ordered three exact-seed words",
    )
    require(
        overlap_destination_words[0] not in {exact_words[0], exact_words[2]},
        "destination 102440 is neither exact stage0 nor exact stage2",
    )

    core = cores[16]
    require(
        (
            core.chart_id,
            core.target_id,
            core.crossings,
            core.t0,
            core.t1,
            core.p0,
            core.p1,
        )
        == (
            "W:N",
            "G[1,1]",
            (),
            Q(69, 100),
            Q(7, 10),
            -Q(1, 50),
            Q(1, 50),
        ),
        "correct Gate25 core16 rectangle",
    )
    word_row, pair_ordinal, pattern_ordinal, ordinal, word_identifier = official_word(
        core, pair_index, pattern_index
    )
    require(word_identifier == overlap[0] and ordinal == 346720, "core16 overlap word")
    require(pattern_ordinal == 0 and word_row == ["W:N", "G[1,1]", [], 1], "core16 word row")

    ctx.prec = precision_bits
    values = round121.load_inputs()
    seed = round121.locate_seed(values)
    root_low, root_high, _lower_sign, _upper_sign = round121.isolate_anchor_root(seed)
    whole = round121.raw_state(seed, (root_low, root_high), Q(0), Q(1))
    exact_t = whole["first"]["normal_x"].value
    exact_p = whole["first"]["momentum"].value
    exact_t_lower, exact_t_upper = round121.arb_pair(exact_t)
    exact_p_lower, exact_p_upper = round121.arb_pair(exact_p)
    require(
        Q(1, 2) < exact_t_lower < exact_t_upper < Q(3, 5) < core.t0,
        "strict t-coordinate separation",
    )
    require(
        -Q(1, 2) < exact_p_lower < exact_p_upper < -Q(2, 5) < core.p0,
        "strict p-coordinate separation",
    )
    require(
        certificate["whole_seed_owner_candidate_replay"]["selected_collision_charts"][0] == "N",
        "exact stage1 N chart",
    )
    owners = certificate["whole_seed_owner_candidate_replay"]["ordered_owner_ids"]
    require(owners[:2] == ["W[-1,-1]", "G[0,0]"], "exact absolute first two owners")

    return {
        "status": "CERTIFIED_ONE_SYMBOLIC_WORD_OVERLAP_AND_STRICT_PHYSICAL_COORDINATE_DISJOINTNESS",
        "exact_seed_official_word_count": 3,
        "base_R1_incidence_official_word_count": 16,
        "overlap_official_word_count": 1,
        "overlap_official_word_key_id": overlap[0],
        "overlap_word_key_row": word_row,
        "overlap_word_pair_index": pair_ordinal,
        "overlap_crossing_pattern_index": pattern_ordinal,
        "overlap_official_word_ordinal": ordinal,
        "overlap_component_count": 2,
        "overlap_component_ids": [row["component_id"] for row in overlap_rows],
        "overlap_directed_edge_destination_official_word_key_id": overlap_destination_words[0],
        "overlap_directed_edge_destination_official_word_ordinal": 102440,
        "Round127_exact_preceding_stage0_official_word_key_id": exact_words[0],
        "Round127_exact_following_stage2_official_word_key_id": exact_words[2],
        "destination_word_102440_is_not_exact_stage0_word_102441": True,
        "destination_word_102440_is_not_exact_stage2_word_180256": True,
        "Gate25_core_index": 16,
        "Gate25_core_id": core_id(core),
        "Gate25_core_rectangle": {
            "chart": "W:N",
            "relative_target_lift": "G[1,1]",
            "crossings": [],
            "t": ["69/100", "7/10"],
            "p": ["-1/50", "1/50"],
            "base_parameter": "s=0",
        },
        "Round121_exact_stage1_local_coordinates": {
            "chart": "W:N",
            "relative_target_lift": "G[1,1]",
            "absolute_source_owner": "W[-1,-1]",
            "absolute_target_owner": "G[0,0]",
            "t_equals_first_normal_x_certified_strict_outer_interval": ["1/2", "3/5"],
            "p_equals_first_collision_momentum_certified_strict_outer_interval": [
                "-1/2",
                "-2/5",
            ],
            "tight_Arb_dyadic_endpoints_intentionally_not_materialized": True,
            "source_curve_x_interval": ["0", "1"],
        },
        "strict_separators": {
            "one_half_strictly_below_exact_stage1_t": True,
            "exact_stage1_t_upper_strictly_below": "3/5",
            "three_fifths_strictly_below_core_t_lower": "69/100",
            "minus_one_half_strictly_below_exact_stage1_p": True,
            "exact_stage1_p_upper_strictly_below": "-2/5",
            "minus_two_fifths_strictly_below_core_p_lower": "-1/50",
            "t_rectangles_disjoint": True,
            "p_rectangles_disjoint": True,
        },
        "relative_target_and_absolute_owner_are_not_identified": True,
        "symbolic_word_overlap_only": True,
        "same_physical_root": False,
        "same_physical_subbranch": False,
        "same_operator_block": False,
        "word_equality_cannot_join_Round72_fields_to_Round121_exact_seed_slots": True,
    }


def scoped_locally_certified_nonempty_key_ledger(
    cores: tuple[Core, ...],
    pair_index: dict[tuple[str, str], int],
    pattern_index: dict[tuple[str, ...], int],
) -> dict[str, Any]:
    """Close only the finite Gate25/exact-seed set union, never a global census."""

    round127 = closed_result(
        HERE / ROUND127_CERTIFICATE,
        "cm2.round127.global-return-word-exact-seed-crosswalk.v1",
    )
    round127_verification = closed_result(
        HERE / ROUND127_VERIFICATION,
        "cm2.round127.global-return-word-exact-seed-crosswalk-verification.v1",
    )
    require(round127_verification["status"] == "PASS", "Round127 verification PASS")
    require(
        round127_verification["certificate_sha256"] == PINS[ROUND127_CERTIFICATE],
        "Round127 verification certificate pin",
    )
    exact_rows = round127["exact_path_official_word_registry_incidence_rows"]
    exact_ids = sorted(row["official_word_key_id"] for row in exact_rows)
    require(len(exact_ids) == len(set(exact_ids)) == 3, "Round127 exact three words")
    gate25_ids = sorted(
        official_word(core, pair_index, pattern_index)[4] for core in cores
    )
    require(len(gate25_ids) == len(set(gate25_ids)) == 24, "Gate25 distinct 24 words")
    intersection = sorted(set(gate25_ids) & set(exact_ids))
    union_ids = sorted(set(gate25_ids) | set(exact_ids))
    require(
        intersection
        == [
            "gate5-word:346720:53f03ff6fc716b0187c62b5e3cc7971c9e030686426d13ff5eee585f33daeb3e"
        ],
        "Gate25/Round127 unique intersection",
    )
    require(len(union_ids) == 26, "Gate25/Round127 union count 26")
    symbolic = round127["symbolic_registry_incidence"]
    require(
        symbolic["global_exact_nonempty_candidate_key_count"] is None,
        "Round127 global exact nonempty census null",
    )
    require(
        symbolic["global_complete_nonempty_or_empty_domain_decisions"] is False,
        "Round127 no global domain decisions",
    )
    return {
        "status": "SCOPED_LOCALLY_CERTIFIED_NONEMPTY_KEY_LOWER_BOUND_26",
        "Gate25_locally_certified_nonempty_word_key_count": 24,
        "Round127_exact_path_locally_certified_nonempty_word_key_count": 3,
        "set_intersection_count": 1,
        "set_intersection_official_word_key_ids": intersection,
        "set_union_count": 26,
        "set_union_official_word_key_ids_sha256": digest(union_ids),
        "locally_certified_nonempty_key_lower_bound": 26,
        "global_exact_nonempty_candidate_key_count": None,
        "complete_global_nonempty_or_empty_domain_census": False,
        "lower_bound_is_not_complete_census_or_coverage": True,
        "lower_bound_scope": "Gate25_physical_cores_UNION_Round127_exact_seed_path",
        "all_441280_candidate_domains_decided": False,
    }


def build(precision_bits: int = PRECISION_BITS) -> dict[str, Any]:
    require(precision_bits == PRECISION_BITS, "Round128 frozen precision must be 1024 bits")
    require(flint.__version__ == "0.9.0", "python-flint version")
    validate_pins()

    global_manifest = strict_json(HERE / GLOBAL_MANIFEST)
    gate25_manifest = strict_json(HERE / GATE25_MANIFEST)
    round67_manifest = strict_json(HERE / ROUND67_MANIFEST)
    round68_manifest = strict_json(HERE / ROUND68_MANIFEST)
    round69_manifest = strict_json(HERE / ROUND69_MANIFEST)
    round71_manifest = strict_json(HERE / ROUND71_MANIFEST)
    round71_witnesses = strict_json(HERE / ROUND71_WITNESSES)
    round72_manifest = strict_json(HERE / ROUND72_MANIFEST)
    round72_fields = strict_json(HERE / ROUND72_FIELDS)

    (
        _pairs,
        _patterns,
        pair_index,
        pattern_index,
        global_replay,
    ) = replay_global_registry(global_manifest)
    cores, gate25_replay = replay_gate25_cores(
        gate25_manifest, pair_index, pattern_index
    )
    (
        incidence_rows,
        edge_rows,
        reciprocal_pair_rows,
        minimal_rows,
        incidence_ledger,
    ) = component_incidence(
        round71_manifest,
        round71_witnesses,
        round72_manifest,
        round72_fields,
        cores,
        pair_index,
        pattern_index,
    )
    round67_ledger = round67_fail_closed_ledger(
        round67_manifest, round68_manifest, round69_manifest
    )
    exact_overlap = exact_seed_overlap_and_separation(
        incidence_rows, cores, pair_index, pattern_index, precision_bits
    )
    scoped_nonempty_ledger = scoped_locally_certified_nonempty_key_ledger(
        cores, pair_index, pattern_index
    )

    require(round72_manifest["result"]["strict_frontier"]["Gate5"]
            == "NOT_CERTIFIED__MATURITY_10_OF_18_BLOCKS_0", "Round72 Gate5")
    require(round72_manifest["result"]["strict_frontier"]["CM2"] == "NO-GO_FOR_CLAIM", "Round72 CM2")
    round121_result = closed_result(
        HERE / ROUND121_CERTIFICATE,
        "cm2.round121.rank3-exact-seed-three-leg-recut-f5f6.v1",
    )
    require(round121_result["gate5_global_maturity"] == "10/18", "Round121 global maturity")
    require(round121_result["complete_18_field_block_count"] == 0, "Round121 complete blocks")
    require(round121_result["gate5_block_count"] == 0, "Round121 Gate5 blocks")
    require(round121_result["cm2_verdict"] == "NO-GO_FOR_CLAIM", "Round121 CM2")

    result = {
        "precision_bits": precision_bits,
        "python_flint_version": flint.__version__,
        "provenance": {
            "append_only": True,
            "old_artifacts_modified": False,
            "strict_byte_pins": dict(sorted(PINS.items())),
            "all_input_JSON_loaded_with_duplicate_and_nonfinite_rejection": True,
        },
        "global_candidate_registry_replay": global_replay,
        "Gate25_physical_core_replay": gate25_replay,
        "A_base_R1_component_to_global_word_incidence": {
            **incidence_ledger,
            "component_incidence_rows": incidence_rows,
            "source_destination_word_edge_rows": edge_rows,
            "reciprocal_word_pair_rows": reciprocal_pair_rows,
            "minimal_mapping_rows": minimal_rows,
        },
        "B_Round67_occurrence_owner_crosswalk_fail_closed": round67_ledger,
        "C_exact_seed_overlap_and_coordinate_separation": exact_overlap,
        "C2_scoped_locally_certified_nonempty_key_lower_bound": scoped_nonempty_ledger,
        "D_global_safety_and_nonpromotion": {
            "status": "LOCAL_INCIDENCE_PROGRESS_ONLY__NO_GLOBAL_GATE_UPGRADE",
            "global_candidate_word_count": 441280,
            "locally_incidence_attached_official_word_count": 16,
            "symbolic_membership_fraction": "16/441280",
            "symbolic_membership_fraction_is_not_domain_measure_or_coverage": True,
            "locally_certified_nonempty_key_lower_bound": 26,
            "global_exact_nonempty_candidate_key_count": None,
            "complete_global_nonempty_or_empty_domain_census": False,
            "Round72_numeric_F10_F13_F16_rows_remain_physical_face_component_local": True,
            "incidence_rows_are_not_18_field_operator_slot_rows": True,
            "Round67_owner_to_path_crosswalk_row_count": 0,
            "arbitrary_return_depth_certified": False,
            "all_parameter_fibres_certified": False,
            "global_complete_18_field_block_count": 0,
            "gate5_block_count": 0,
            "gate5_global_maturity": "10/18",
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
            "no_Round72_component_is_promoted_into_a_Round121_exact_seed_block": True,
        },
        "strict_nonclaims": [
            "the 16 official-word memberships are not physical-domain, measure, or global coverage",
            "the 32 component incidences do not identify a face with a path interior point",
            "no Round67 occurrence/owner row is joined to a Round71 or Round72 component",
            "equal time, connected rank, side names, numeric coordinates, or official word alone are not immutable-root equality",
            "the ordinal-346720 overlap is physically disjoint from the Round121 exact stage1 curve inside the common W:N chart",
            "no homogeneous-subbranch, recut, operator-carrier, F18 block, Wiener, Kac, Gate5, or CM2 upgrade is claimed",
        ],
    }
    return json.loads(json.dumps(result, sort_keys=True))


def document(precision_bits: int = PRECISION_BITS) -> dict[str, Any]:
    result = build(precision_bits)
    return {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--precision-bits", type=int, default=PRECISION_BITS)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    try:
        payload = json.dumps(
            document(args.precision_bits),
            indent=2,
            sort_keys=True,
            ensure_ascii=True,
        ) + "\n"
        args.output.write_text(payload, encoding="utf-8")
        return 0
    except (
        Round128Error,
        OSError,
        ValueError,
        KeyError,
        IndexError,
        TypeError,
        ArithmeticError,
    ) as exc:
        print(f"ROUND128_PRODUCER_ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
