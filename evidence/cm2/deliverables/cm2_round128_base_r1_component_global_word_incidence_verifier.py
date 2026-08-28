#!/usr/bin/env python3
"""Independent verifier for the Round128 base-R1/global-word incidence.

The verifier never imports or executes the Round128 producer.  It independently
rebuilds the exact-rational 448 by 985 candidate registry, the 24 Gate25
physical cores, the 32 Round71/72 component incidences, their 16 directed
source/destination official-word edges and eight reciprocal pairs.  It also
replays the Round67 0/12 typed-incidence gap, the scoped 26-key lower bound,
and the strict physical separation of the sole symbolic overlap.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Callable, Iterator

import flint
from flint import arb, ctx


HERE = Path(__file__).resolve().parent
VERIFIER = Path(__file__).resolve()
PRODUCER = HERE / "cm2_round128_base_r1_component_global_word_incidence.py"
CERTIFICATE = (
    HERE / "cm2-round128-base-r1-component-global-word-incidence-2026-07-24.json"
)
OUTPUT = (
    HERE
    / "cm2-round128-base-r1-component-global-word-incidence-verification-2026-07-24.json"
)
CERTIFICATE_SCHEMA = "cm2.round128.base-r1-component-global-word-incidence.v1"
VERIFICATION_SCHEMA = (
    "cm2.round128.base-r1-component-global-word-incidence-verification.v1"
)
PRODUCER_SHA256 = (
    "d218d92a6aa7a929e734c86110e67ec8ebea75b3c57bf74e5a7d3b3e33d32e35"
)
CERTIFICATE_SHA256 = (
    "7c5f513ba9bac5c5381e5504870b783159ebbb622ca155f649429cb65ad7b10e"
)
CERTIFICATE_RESULT_SHA256 = (
    "46601ee43c7ca8051dac51fd608605a814abfb755092ea8225fd3f0f2c755815"
)
PRECISION_BITS = 2048

PINS = {
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json":
        "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42",
    "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json":
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866",
    "cm2-round121-rank3-exact-seed-three-leg-recut-f5f6-2026-07-23.json":
        "ba56b41a41fbf0d77c6467fcb5fc521ef4d6928f65a9f79d5bba8b83c9b4fc6e",
    "cm2-round121-rank3-exact-seed-three-leg-recut-f5f6-verification-2026-07-23.json":
        "ec527c19a8c50025514db0769808ce21aeb53c7d1cc64edb75f1a9c5a6aa3e80",
    "cm2-round127-global-return-word-exact-seed-crosswalk-2026-07-24.json":
        "4aa7cde5e22883dfcb8e59f16e7bd6ab16c4436229c9964384ef72dda0c16408",
    "cm2-round127-global-return-word-exact-seed-crosswalk-verification-2026-07-24.json":
        "5958b4905b8e005886302a6bffc32d15fd1091cf8dbe20b743488e3f91eeb383",
    "cm2-round67-fixed-j-occurrence-owner-root-time-potential-frontier-manifest-2026-07-21.json":
        "97cb410b9e960d8331a37ef9203b040c9b1d86c3ed3d1ba6ba66a28c4e4ff400",
    "cm2-round68-common-root-all-gate-frontier-manifest-2026-07-21.json":
        "a9dd3e825f384f0a36db2745a8677505fb852a76fef2dd2fb9682bdc4573214f",
    "cm2-round69-base-s-return-incidence-all-gate-manifest-2026-07-21.json":
        "08d996d52d6aa8ea3b716a46b51d6ae8f0a6b4b9e24c9fab402afe88059bc838",
    "cm2-round71-r1-nonempty-face-germs-manifest-2026-07-21.json":
        "fb7fd4233d14834ca6a3efc488c2e8f1fcdf97bdeb410a1b93eda8d9b59d50f9",
    "cm2-round71-r1-nonempty-face-witnesses-2026-07-21.json":
        "3226044b8d0718a0d565c7ff9dd6c4736d2b1d28fa784c46443da92e85b61cc6",
    "cm2-round72-r1-component-f10-f13-f16-proof-2026-07-21.json":
        "12c1f1db87030cf63552621a24ac0ebb1adb39933dc420497b425fb3c1f8e8a9",
    "cm2-round72-r1-full-atlas-f10-f13-f16-manifest-2026-07-21.json":
        "4bb012ae54db337cbdaa8cdc02aee55025dd522ccc566a7fb343b57010d4f6f9",
    "cm2_gate25_physical_return_core_registry_cert.py":
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
    "cm2_gate3_candidate_first_hit_cert.py":
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    "cm2_gate5_return_word_three_norm_frontier_cert.py":
        "ddcc250f8700c6a695f96019d9f7824fe98636e20a67685fdc6a3cce77f6d695",
    "cm2_round121_rank3_exact_seed_three_leg_recut_f5f6.py":
        "30c69e1849867841398483749f547a7840d401bc3cc24b9e4ef0a4892ad990ed",
    "cm2_round127_global_return_word_exact_seed_crosswalk.py":
        "ea461b3ed1301149bca350f32190348aca955f0a04ce42663fab23451144b0dd",
    "cm2_round127_global_return_word_exact_seed_crosswalk_verifier.py":
        "24de0b53c872d43f0a0d7422164e5a2a776a1d35879c923bcf5a07afef94e157",
    "cm2_round67_fixed_j_occurrence_owner_root_time_potential_frontier_cert.py":
        "cfb501aff4f321742e3fead9895c596e9105b2a89d064d917646b70c6f91ee8f",
    "cm2_round68_common_root_all_gate_frontier_cert.py":
        "b10da56552faf6e7006943cc8229afc6478fe211526c621511922addca63a27d",
    "cm2_round69_base_s_return_incidence_all_gate_cert.py":
        "17a07346c61920a42eb04e074bc736eb1f78809a4867c130ac7ed86613d67e8f",
    "cm2_round71_r1_nonempty_face_germs_cert.py":
        "ec5b229a7a624ca37f93884d938e26a5e946ff4254edf24cd9a7e7d98d8c6c72",
    "cm2_round72_r1_component_f10_f13_f16_generator.py":
        "20eb60b52acce9173e2685979aa44bd532c02ec10fd2c2d3862a5e10c92d0381",
    "cm2_round72_r1_full_atlas_f10_f13_f16_cert.py":
        "bf0a9ced0b66174b100dfe195666312215ce9a873558c48787669e0f77da04f9",
}

GLOBAL = "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
GATE25 = "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json"
R67 = "cm2-round67-fixed-j-occurrence-owner-root-time-potential-frontier-manifest-2026-07-21.json"
R68 = "cm2-round68-common-root-all-gate-frontier-manifest-2026-07-21.json"
R69 = "cm2-round69-base-s-return-incidence-all-gate-manifest-2026-07-21.json"
R71 = "cm2-round71-r1-nonempty-face-germs-manifest-2026-07-21.json"
R71W = "cm2-round71-r1-nonempty-face-witnesses-2026-07-21.json"
R72 = "cm2-round72-r1-full-atlas-f10-f13-f16-manifest-2026-07-21.json"
R72F = "cm2-round72-r1-component-f10-f13-f16-proof-2026-07-21.json"
R121 = "cm2-round121-rank3-exact-seed-three-leg-recut-f5f6-2026-07-23.json"
R121V = "cm2-round121-rank3-exact-seed-three-leg-recut-f5f6-verification-2026-07-23.json"
R127 = "cm2-round127-global-return-word-exact-seed-crosswalk-2026-07-24.json"
R127V = "cm2-round127-global-return-word-exact-seed-crosswalk-verification-2026-07-24.json"

PAIR_SHA = "ccf4e9e42c7b17f6ebb7f33ec707616bb49ec1d755a817ce141dc92d47056f75"
PATTERN_SHA = "2d655b1b83918b0cc42845e465d05f7309657b776f0acbd3d3003e8ae17bb39d"
STREAM_SHA = "841cb96798c9bd41e1440c8b2cdd93af5d80f2f64d693f2aa00175a440045ab9"
SOURCE_MINIMAL_SHA = "6a19bb49fcde593afc64e14cfb4c25b40151facd92f5cc77e2c11d1239b953b0"
SOURCE_SUMMARY_SHA = "69a1b5460325507d1ac7b5949edc636fef6cdb7051b0f8d7c29653a7b7ee7bad"
OFFICIAL_IDS_SHA = "b1599b17b48895de82be81855ee840382cf2e5c4f65c3b9df7df9c7bae7f7144"
COMPONENT_SOURCE_SHA = "0cb469f08f007d395cd88a438fd48c44e3835b369be49606689557a84c347d95"
OVERLAP_WORD = "gate5-word:346720:53f03ff6fc716b0187c62b5e3cc7971c9e030686426d13ff5eee585f33daeb3e"


class VerificationError(RuntimeError):
    pass


def require(condition: Any, label: str) -> None:
    if not bool(condition):
        raise VerificationError(label)


def canonical(value: Any) -> str:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    )


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise VerificationError(f"duplicate JSON key:{key}")
        result[key] = value
    return result


def reject_number(token: str) -> Any:
    raise VerificationError(f"forbidden JSON number:{token}")


def strict_integer(token: str) -> int:
    if token == "-0":
        raise VerificationError("negative zero forbidden")
    if len(token.lstrip("-")) > 18:
        raise VerificationError("oversized integer")
    value = int(token)
    if abs(value) > 2**63 - 1:
        raise VerificationError("integer outside int64")
    return value


def reject_surrogates(value: Any) -> None:
    if type(value) is str:
        require(
            not any(0xD800 <= ord(char) <= 0xDFFF for char in value),
            "unpaired surrogate",
        )
    elif type(value) is list:
        for item in value:
            reject_surrogates(item)
    elif type(value) is dict:
        for key, item in value.items():
            reject_surrogates(key)
            reject_surrogates(item)


def parse_bytes(raw: bytes, *, certificate_mode: bool) -> Any:
    require(not raw.startswith(b"\xef\xbb\xbf"), "UTF-8 BOM")
    kwargs: dict[str, Any] = {
        "object_pairs_hook": strict_pairs,
        "parse_constant": reject_number,
        "parse_int": strict_integer if certificate_mode else int,
    }
    if certificate_mode:
        kwargs["parse_float"] = reject_number
    value = json.loads(raw.decode("utf-8", errors="strict"), **kwargs)
    reject_surrogates(value)
    return value


def closed_document(path: Path, schema: str) -> dict[str, Any]:
    document = parse_bytes(path.read_bytes(), certificate_mode=True)
    require(type(document) is dict, f"top object:{path.name}")
    require(
        set(document) == {"schema", "result", "result_sha256"},
        f"closed envelope:{path.name}",
    )
    require(document["schema"] == schema, f"schema:{path.name}")
    require(type(document["result"]) is dict, f"result object:{path.name}")
    require(
        document["result_sha256"] == digest(document["result"]),
        f"result digest:{path.name}",
    )
    return document


def upstream(name: str) -> dict[str, Any]:
    path = HERE / name
    require(path.is_file() and not path.is_symlink(), f"pin target:{name}")
    require(sha256(path) == PINS[name], f"byte pin:{name}")
    value = parse_bytes(path.read_bytes(), certificate_mode=False)
    require(type(value) is dict, f"upstream object:{name}")
    return value


def validate_all_pins() -> dict[str, dict[str, Any]]:
    for name, expected in PINS.items():
        path = HERE / name
        require(path.is_file() and not path.is_symlink(), f"pin target:{name}")
        require(sha256(path) == expected, f"byte pin:{name}")
    require(sha256(PRODUCER) == PRODUCER_SHA256, "producer byte pin")
    return {
        name: upstream(name)
        for name in (GLOBAL, GATE25, R67, R68, R69, R71, R71W, R72, R72F)
    }


def qstr(value: Q) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


SOURCE_CHARTS = tuple(
    f"{source}:{cell}"
    for source in ("G", "W")
    for cell in ("E", "W", "N", "S")
)
RADIUS = {"G": Q(9, 25), "W": Q(4, 25)}
EPS = Q(1, 400)
TAU_MAX = Q(3)
ISQ2_LOWER = Q(707, 1000)
ISQ2_UPPER = Q(708, 1000)


@dataclass(frozen=True)
class Target:
    obstacle: str
    ix: int
    iy: int

    @property
    def identifier(self) -> str:
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
        x, y = Q(2 * ix + 1, 2), Q(2 * iy + 1, 2)
        return x - EPS, x + EPS, y, y
    if source == "W" and target.obstacle == "G":
        x, y = Q(2 * ix - 1, 2), Q(2 * iy - 1, 2)
        return x - EPS, x + EPS, y, y
    return Q(ix), Q(ix), Q(iy), Q(iy)


def square_min_abs(lower: Q, upper: Q) -> Q:
    return Q(0) if lower <= 0 <= upper else min(lower * lower, upper * upper)


def support_upper(cell: str, x0: Q, x1: Q, y0: Q, y1: Q) -> Q:
    if cell == "E":
        axis, transverse = x1, max(abs(y0), abs(y1))
    elif cell == "W":
        axis, transverse = -x0, max(abs(y0), abs(y1))
    elif cell == "N":
        axis, transverse = y1, max(abs(x0), abs(x1))
    elif cell == "S":
        axis, transverse = -y0, max(abs(x0), abs(x1))
    else:
        raise VerificationError("source cell")
    return (
        axis + transverse * ISQ2_UPPER
        if axis >= 0
        else axis * ISQ2_LOWER + transverse * ISQ2_UPPER
    )


def retained(source: str, cell: str, target: Target) -> bool:
    if target.obstacle == source and target.ix == target.iy == 0:
        return False
    x0, x1, y0, y1 = vector_interval(source, target)
    distance2 = square_min_abs(x0, x1) + square_min_abs(y0, y1)
    horizon = TAU_MAX + RADIUS[source] + RADIUS[target.obstacle]
    if distance2 >= horizon * horizon:
        return False
    return not (
        support_upper(cell, x0, x1, y0, y1)
        < RADIUS[source] - RADIUS[target.obstacle]
    )


def retained_pairs() -> tuple[tuple[str, str], ...]:
    rows = []
    for chart in SOURCE_CHARTS:
        source, cell = chart.split(":")
        for target in TARGETS:
            if retained(source, cell, target):
                rows.append((chart, target.identifier))
    result = tuple(rows)
    require(len(result) == len(set(result)) == 448, "448 retained pairs")
    return result


def orientations(count: int) -> tuple[int, ...]:
    return (0,) if count == 0 else (-1, 1)


def crossing_patterns() -> Iterator[tuple[str, ...]]:
    for nx in range(5):
        for ny in range(5):
            length = nx + ny
            for sx in orientations(nx):
                for sy in orientations(ny):
                    for x_positions in itertools.combinations(range(length), nx):
                        x_set = set(x_positions)
                        yield tuple(
                            ("X+" if sx > 0 else "X-")
                            if index in x_set
                            else ("Y+" if sy > 0 else "Y-")
                            for index in range(length)
                        )


def word_row(chart: str, target: str, crossings: tuple[str, ...]) -> list[Any]:
    return [chart, target, list(crossings), len(crossings) + 1]


def replay_registry(manifest: dict[str, Any]) -> tuple[Any, ...]:
    result = manifest["result"]
    require(result["schema"] == "cm2.gate5.return-word-three-norm-frontier.v1",
            "global result schema")
    frozen = result["immutable_candidate_key_registry"]
    grammar = result["crossing_grammar"]
    pairs = retained_pairs()
    patterns = tuple(crossing_patterns())
    require(len(patterns) == len(set(patterns)) == 985, "985 patterns")
    require(
        Counter(map(len, patterns))
        == {0: 1, 1: 4, 2: 12, 3: 28, 4: 60, 5: 120, 6: 200, 7: 280, 8: 280},
        "pattern histogram",
    )
    require(digest(pairs) == PAIR_SHA, "pair digest")
    require(digest(patterns) == PATTERN_SHA, "pattern digest")
    stream = hashlib.sha256()
    count = roof_count = 0
    for chart, target in pairs:
        for crossings in patterns:
            row = word_row(chart, target, crossings)
            stream.update(canonical(row).encode())
            stream.update(b"\n")
            count += 1
            roof_count += len(crossings) + 1
    require(count == 441280 and roof_count == 3286976, "global counts")
    require(stream.hexdigest() == STREAM_SHA, "global stream digest")
    require(frozen["candidate_word_key_rows_sha256"] == STREAM_SHA, "frozen stream")
    require(frozen["chart_target_pair_rows_sha256"] == PAIR_SHA, "frozen pairs")
    require(grammar["crossing_pattern_rows_sha256"] == PATTERN_SHA, "frozen patterns")
    pair_index = {row: index for index, row in enumerate(pairs)}
    pattern_index = {row: index for index, row in enumerate(patterns)}
    replay = {
        "source_chart_count": 8,
        "target_lift_count": 162,
        "retained_chart_target_pair_count": 448,
        "crossing_pattern_count_per_pair": 985,
        "candidate_return_word_key_count": 441280,
        "roof_level_prefix_suffix_pair_count": 3286976,
        "chart_target_pair_rows_sha256": PAIR_SHA,
        "crossing_pattern_rows_sha256": PATTERN_SHA,
        "candidate_word_row_stream_sha256": STREAM_SHA,
        "enumeration_independently_reimplemented_with_exact_rationals": True,
    }
    return pairs, patterns, pair_index, pattern_index, replay


@dataclass(frozen=True)
class Core:
    chart: str
    t0: Q
    t1: Q
    p0: Q
    p1: Q
    target: str
    crossings: tuple[str, ...]
    family: str

    @property
    def source(self) -> str:
        return self.chart.split(":")[0]


def physical_cores() -> tuple[Core, ...]:
    rows: list[Core] = []
    axes = {
        "E": (1, 0, "X+"), "W": (-1, 0, "X-"),
        "N": (0, 1, "Y+"), "S": (0, -1, "Y-"),
    }
    for source in ("G", "W"):
        for cell in ("E", "W", "N", "S"):
            ix, iy, token = axes[cell]
            rows.append(Core(
                f"{source}:{cell}", Q(1, 100), Q(1, 50),
                -Q(1, 500), Q(1, 500), f"{source}[{ix},{iy}]",
                () if source == "G" else (token,), "axis_translate",
            ))
    diagonals = {
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
            first, second, target = diagonals[source][direction]
            for cell, sign in (first, second):
                t0, t1 = (
                    (Q(69, 100), Q(7, 10))
                    if sign > 0 else (-Q(7, 10), -Q(69, 100))
                )
                rows.append(Core(
                    f"{source}:{cell}", t0, t1, -Q(1, 50), Q(1, 50),
                    target, (), f"diagonal_{direction}",
                ))
    rows.sort(key=lambda c: (
        c.chart, c.target, c.crossings, c.t0, c.t1, c.p0, c.p1,
    ))
    require(len(rows) == 24, "24 cores")
    return tuple(rows)


def core_payload(core: Core) -> dict[str, Any]:
    return {
        "chart_id": core.chart,
        "t": [qstr(core.t0), qstr(core.t1)],
        "p": [qstr(core.p0), qstr(core.p1)],
        "target_id": core.target,
        "crossings": list(core.crossings),
    }


def core_id(core: Core) -> str:
    return "core:" + digest(core_payload(core))


def official_word(
    core: Core,
    pair_index: dict[tuple[str, str], int],
    pattern_index: dict[tuple[str, ...], int],
) -> tuple[list[Any], int, int, int, str]:
    pair = pair_index[(core.chart, core.target)]
    pattern = pattern_index[core.crossings]
    ordinal = pair * 985 + pattern
    row = word_row(core.chart, core.target, core.crossings)
    return row, pair, pattern, ordinal, f"gate5-word:{ordinal:06d}:{digest(row)}"


def face_id(core: Core, side: str) -> str:
    value = (
        core.t0 if side == "t_lower" else
        core.t1 if side == "t_upper" else
        core.p0 if side == "p_lower" else core.p1
    )
    return "physical-core-face:" + digest({
        "core_id": core_id(core),
        "core_chart_id": core.chart,
        "core_source_obstacle": core.source,
        "side": side,
        "coordinate": side[0],
        "coordinate_value": qstr(value),
        "outward_normal_sign": -1 if side.endswith("lower") else 1,
    })


def path_cell_id(source: str, destination: str) -> str:
    return "base-r1-edge-cell:" + digest({
        "source_core_id": source, "destination_core_id": destination, "s": "0",
    })


def replay_gate25(
    manifest: dict[str, Any],
    cores: tuple[Core, ...],
    pair_index: dict[tuple[str, str], int],
    pattern_index: dict[tuple[str, ...], int],
) -> dict[str, Any]:
    frozen = manifest["result"]["physical_return_core_registry"]
    require(frozen["physical_compact_homogeneous_core_count"] == 24, "Gate25 count")
    require(frozen["all_24_keys_members_of_frozen_441280_envelope"] is True,
            "Gate25 membership")
    require(
        frozen["all_cores_strict_first_hit_against_complete_retained_candidate_list"]
        is True,
        "Gate25 first hit",
    )
    key_rows = [
        canonical(official_word(core, pair_index, pattern_index)[0])
        for core in cores
    ]
    require(len(set(key_rows)) == 24, "Gate25 distinct words")
    require(digest(sorted(key_rows)) == frozen["distinct_key_rows_sha256"],
            "Gate25 key digest")
    return {
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


def witness_component_id(witness: dict[str, Any]) -> str:
    return "physical-r1-face-component:" + digest({
        "candidate_family_id": witness["candidate_family_id"],
        "base_parameter": "s=0",
        "witness_minus": witness["witness_minus"],
        "witness_plus": witness["witness_plus"],
    })


def closed_row(row: dict[str, Any]) -> dict[str, Any]:
    require("row_sha256" not in row, "unclosed input row")
    result = dict(row)
    result["row_sha256"] = digest(result)
    return result


def replay_components(
    documents: dict[str, dict[str, Any]],
    cores: tuple[Core, ...],
    pair_index: dict[tuple[str, str], int],
    pattern_index: dict[tuple[str, ...], int],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]],
           list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    r71 = documents[R71]["result"]
    r72 = documents[R72]["result"]
    witnesses_doc = documents[R71W]
    proof_doc = documents[R72F]
    require(r71["schema"] == "cm2.round71.r1-nonempty-face-germs.v1",
            "Round71 schema")
    require(r72["schema"] == "cm2.round72.r1-full-atlas-f10-f13-f16.v1",
            "Round72 schema")
    require(witnesses_doc["schema"] == "cm2.round71.r1-nonempty-face-witnesses.v1",
            "Round71 witness schema")
    require(proof_doc["schema"] == "cm2.round72.r1-component-f10-f13-f16.v1",
            "Round72 proof schema")

    component_rows = r71["base_fibre_nonempty_face_witness_registry"]["component_rows"]
    field_rows = r72["numeric_local_field_registry"]["component_field_rows"]
    proof_rows = proof_doc["result"]["rows"]
    witnesses = witnesses_doc["rows"]
    require(
        len(component_rows) == len(field_rows) == len(proof_rows)
        == len(witnesses) == 32,
        "32 upstream component rows",
    )
    component_map = {row["component_id"]: row for row in component_rows}
    field_map = {row["component_id"]: row for row in field_rows}
    proof_map = {row["component_id"]: row for row in proof_rows}
    witness_map = {witness_component_id(row): row for row in witnesses}
    identifiers = set(component_map)
    require(
        len(identifiers) == 32
        and identifiers == set(field_map) == set(proof_map) == set(witness_map),
        "exact four-way component join",
    )
    require(field_rows == proof_rows, "Round72 manifest/proof rows")
    require(
        digest(proof_rows)
        == r72["numeric_local_field_registry"]["component_field_rows_sha256"]
        == proof_doc["result"]["rows_sha256"],
        "Round72 field digest",
    )

    incidence_rows: list[dict[str, Any]] = []
    minimal_rows: list[dict[str, Any]] = []
    source_projection_minimal: list[dict[str, Any]] = []
    grouped: dict[tuple[Any, ...], list[tuple[str, str]]] = defaultdict(list)
    core_use: Counter[int] = Counter()
    round69_edges: set[tuple[str, str, str]] = set()

    for component_identifier in sorted(identifiers):
        component = component_map[component_identifier]
        field = field_map[component_identifier]
        witness = witness_map[component_identifier]
        require(
            component["candidate_family_id"] == field["candidate_family_id"]
            == witness["candidate_family_id"],
            "candidate-family join",
        )
        require(field["source_core_index"] == witness["source_core_index"],
                "source core index join")
        require(field["side"] == witness["side"], "Round71/72 face-side join")
        source_index = field["source_core_index"]
        destination_index = witness["destination_core_index"]
        require(
            type(source_index) is int and type(destination_index) is int
            and 0 <= source_index < 24 and 0 <= destination_index < 24,
            "core index ranges",
        )
        source, destination = cores[source_index], cores[destination_index]
        source_identifier = core_id(source)
        destination_identifier = core_id(destination)
        require(
            component["source_core_id"] == witness["source_core_id"]
            == source_identifier,
            "source core ID",
        )
        require(
            component["destination_core_id"] == witness["destination_core_id"]
            == destination_identifier,
            "destination core ID",
        )
        require(
            component["destination_face_id"] == witness["destination_face_id"]
            == face_id(destination, witness["side"]),
            "destination face ID",
        )
        path_identifier = path_cell_id(source_identifier, destination_identifier)
        require(component["path_cell_id"] == path_identifier, "path-cell ID")
        require(component["time_j"] == 1 and component["connected_rank"] == 0,
                "time/rank")
        require(
            component["incidence_relation"]
            == "TERMINAL_CORE_PREIMAGE_FACE_GERM_INCIDENT_TO_BASE_R1_EDGE_CELL",
            "typed incidence",
        )
        traces = component["trace_rows"]
        require(
            [trace["side_label"] for trace in traces] == ["inside", "outside"],
            "trace sides",
        )
        for trace in traces:
            require(
                trace["trace_id"] == "physical-r1-trace:" + digest({
                    "component_id": component_identifier,
                    "side": trace["side_label"],
                }),
                "trace ID",
            )
        source_word = official_word(source, pair_index, pattern_index)
        destination_word = official_word(destination, pair_index, pattern_index)
        (source_row, source_pair, source_pattern, source_ordinal,
         source_word_id) = source_word
        (destination_row, destination_pair, destination_pattern,
         destination_ordinal, destination_word_id) = destination_word
        require(
            source.crossings == destination.crossings == ()
            and source_row[3] == destination_row[3] == 1,
            "unit roof source/destination",
        )
        core_use[source_index] += 1
        round69_edges.add(
            (source_identifier, destination_identifier, path_identifier)
        )
        stable_key = [
            "round128-base-r1-component-directed-word-incidence-v2",
            component_identifier,
            path_identifier,
            source_word_id,
            destination_word_id,
        ]
        row = {
            "incidence_row_id":
                "round128-component-word-incidence:" + digest(stable_key),
            "component_id": component_identifier,
            "candidate_family_id": component["candidate_family_id"],
            "source_core_index": source_index,
            "source_core_index_is_not_the_immutable_key": True,
            "source_core_id": source_identifier,
            "source_core_payload": core_payload(source),
            "destination_core_index": destination_index,
            "destination_core_id": destination_identifier,
            "destination_face_id": component["destination_face_id"],
            "path_cell_id": path_identifier,
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
                "F13_current_variation_strict_upper":
                    field["F13_current_variation_strict_upper"],
                "F16_Piola_flux_cost_strict_upper":
                    field["F16_Piola_flux_cost_strict_upper"],
            },
            "source_official_word_row": source_row,
            "source_official_word_pair_index": source_pair,
            "source_crossing_pattern_index": source_pattern,
            "source_official_word_ordinal": source_ordinal,
            "source_official_word_key_id": source_word_id,
            "destination_official_word_row": destination_row,
            "destination_official_word_pair_index": destination_pair,
            "destination_crossing_pattern_index": destination_pattern,
            "destination_official_word_ordinal": destination_ordinal,
            "destination_official_word_key_id": destination_word_id,
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
        minimal_rows.append({
            "path_cell_id": path_identifier,
            "source_core_id": source_identifier,
            "destination_core_id": destination_identifier,
            "source_official_word_row": source_row,
            "source_official_word_key_id": source_word_id,
            "destination_official_word_row": destination_row,
            "destination_official_word_key_id": destination_word_id,
            "component_id": component_identifier,
            "candidate_family_id": component["candidate_family_id"],
            "time_j": 1,
            "connected_rank": 0,
        })
        source_projection_minimal.append({
            "path_cell_id": path_identifier,
            "source_core_id": source_identifier,
            "destination_core_id": destination_identifier,
            "word_key_row": source_row,
            "official_word_key_id": source_word_id,
            "component_id": component_identifier,
            "candidate_family_id": component["candidate_family_id"],
            "time_j": 1,
            "connected_rank": 0,
        })
        grouped[(
            source_word_id, canonical(source_row), source_pair, source_pattern,
            source_ordinal, destination_word_id, canonical(destination_row),
            destination_pair, destination_pattern, destination_ordinal,
            path_identifier, source_identifier, destination_identifier,
            source_index, destination_index,
        )].append((component_identifier, row["incidence_row_id"]))

    incidence_rows.sort(
        key=lambda row: (row["source_official_word_key_id"], row["component_id"])
    )
    minimal_rows.sort(
        key=lambda row: (row["source_official_word_key_id"], row["component_id"])
    )
    source_projection_minimal.sort(
        key=lambda row: (row["official_word_key_id"], row["component_id"])
    )
    require(digest(source_projection_minimal) == SOURCE_MINIMAL_SHA,
            "legacy source-projection minimal digest")
    require(len(core_use) == 16 and set(core_use.values()) == {2},
            "16 source cores twice")

    edge_rows: list[dict[str, Any]] = []
    source_summaries: list[dict[str, Any]] = []
    for key, component_pairs in sorted(grouped.items()):
        (
            source_word_id, source_row_json, source_pair, source_pattern,
            source_ordinal, destination_word_id, destination_row_json,
            destination_pair, destination_pattern, destination_ordinal,
            path_identifier, source_identifier, destination_identifier,
            source_index, destination_index,
        ) = key
        source_row = json.loads(source_row_json)
        destination_row = json.loads(destination_row_json)
        components = sorted(item[0] for item in component_pairs)
        incidence_ids = sorted(item[1] for item in component_pairs)
        require(len(components) == len(set(components)) == 2,
                "two components per edge")
        edge_key = [
            "round128-base-r1-directed-word-to-word-edge-v2",
            source_identifier, destination_identifier, path_identifier,
            source_word_id, destination_word_id,
        ]
        edge = {
            "edge_row_id":
                "round128-directed-word-to-word-edge:" + digest(edge_key),
            "source_core_index": source_index,
            "source_core_id": source_identifier,
            "destination_core_index": destination_index,
            "destination_core_id": destination_identifier,
            "path_cell_id": path_identifier,
            "source_official_word_row": source_row,
            "source_official_word_pair_index": source_pair,
            "source_crossing_pattern_index": source_pattern,
            "source_official_word_ordinal": source_ordinal,
            "source_official_word_key_id": source_word_id,
            "destination_official_word_row": destination_row,
            "destination_official_word_pair_index": destination_pair,
            "destination_crossing_pattern_index": destination_pattern,
            "destination_official_word_ordinal": destination_ordinal,
            "destination_official_word_key_id": destination_word_id,
            "source_and_destination_roof_level_count": 1,
            "component_count": 2,
            "component_ids": components,
            "component_incidence_row_ids": incidence_ids,
            "numeric_F10_F13_F16_attachment_role": "source_official_word",
            "edge_semantics": (
                "two connected terminal-preimage face components are incident "
                "to one certified positive directed base-R1 path cell; the "
                "source and destination official words are distinct registered roles"
            ),
        }
        edge_rows.append(closed_row(edge))
        source_summaries.append({
            "official_word_key_id": source_word_id,
            "word_key_row": source_row,
            "path_cell_id": path_identifier,
            "source_core_id": source_identifier,
            "destination_core_id": destination_identifier,
            "component_count": 2,
            "component_ids": components,
        })
    edge_rows.sort(key=lambda row: row["source_official_word_key_id"])
    source_summaries.sort(key=lambda row: row["official_word_key_id"])
    require(len(edge_rows) == 16, "16 directed edges")
    require(digest(source_summaries) == SOURCE_SUMMARY_SHA,
            "legacy source summary digest")
    source_ids = sorted(row["source_official_word_key_id"] for row in edge_rows)
    destination_ids = sorted(
        row["destination_official_word_key_id"] for row in edge_rows
    )
    require(
        len(set(source_ids)) == len(set(destination_ids)) == 16
        and set(source_ids) == set(destination_ids),
        "same 16 source/destination words",
    )
    require(digest(source_ids) == digest(destination_ids) == OFFICIAL_IDS_SHA,
            "official ID set digest")
    component_source_pairs = sorted(
        [row["component_id"], row["source_official_word_key_id"]]
        for row in incidence_rows
    )
    require(digest(component_source_pairs) == COMPONENT_SOURCE_SHA,
            "component/source word digest")

    # Round69 independently fixes the same directed base-R1 core graph.
    r69_rows = documents[R69]["result"]["actual_base_s_return_root"]["edge_rows"]
    r69_edges = {
        (row["source_core_id"], row["destination_core_id"]) for row in r69_rows
    }
    require(
        r69_edges
        == {(source, destination) for source, destination, _path in round69_edges}
        and len(r69_edges) == 16,
        "Round69/Round71 exact directed edge set",
    )

    reciprocal_groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for edge in edge_rows:
        reciprocal_groups[
            tuple(sorted((edge["source_core_id"], edge["destination_core_id"])))
        ].append(edge)
    require(len(reciprocal_groups) == 8, "8 reciprocal core pairs")
    reciprocal_rows: list[dict[str, Any]] = []
    for unordered_core_ids, directed in sorted(reciprocal_groups.items()):
        require(len(directed) == 2, "two reciprocal directions")
        first, second = directed
        require(
            first["source_core_id"] == second["destination_core_id"]
            and first["destination_core_id"] == second["source_core_id"],
            "reverse core directions",
        )
        require(
            first["source_official_word_key_id"]
            == second["destination_official_word_key_id"]
            and first["destination_official_word_key_id"]
            == second["source_official_word_key_id"],
            "reverse word directions",
        )
        edge_ids = sorted(edge["edge_row_id"] for edge in directed)
        pair_key = [
            "round128-base-r1-reciprocal-directed-word-pair-v1",
            list(unordered_core_ids), edge_ids,
        ]
        reciprocal_rows.append(closed_row({
            "reciprocal_pair_id":
                "round128-reciprocal-word-pair:" + digest(pair_key),
            "unordered_core_ids": list(unordered_core_ids),
            "directed_edge_row_ids": edge_ids,
            "directed_source_official_word_key_ids": sorted(
                edge["source_official_word_key_id"] for edge in directed
            ),
            "exactly_two_reverse_directions": True,
        }))

    # Extra independent numeric/face census not needed to construct IDs.
    require(
        (min(row["numeric_local_fields"]["F10_integer_upper"]
             for row in incidence_rows),
         max(row["numeric_local_fields"]["F10_integer_upper"]
             for row in incidence_rows),
         sum(row["numeric_local_fields"]["F10_integer_upper"]
             for row in incidence_rows))
        == (3, 39, 480),
        "F10 min/max/sum",
    )
    require(
        sum(len(row["trace_rows"]) for row in incidence_rows) == 64,
        "64 trace incidences",
    )

    ledger = {
        "status":
            "CERTIFIED_32_BASE_R1_COMPONENT_INCIDENCES_TO_16_DIRECTED_WORD_TO_WORD_EDGES",
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
        "reciprocal_pair_rows_sha256": digest(reciprocal_rows),
        "minimal_mapping_rows_sha256": digest(minimal_rows),
        "source_projection_summary_rows_sha256": digest(source_summaries),
        "source_official_word_ids_sha256": digest(source_ids),
        "destination_official_word_ids_sha256": digest(destination_ids),
        "component_source_word_pairs_sha256": digest(component_source_pairs),
        "numeric_F10_F13_F16_attachment_role": "source_official_word",
        "word_membership_is_not_domain_measure_or_global_coverage": True,
        "incidence_is_not_face_path_point_equality": True,
        "source_core_index_is_replayed_but_core_id_and_payload_are_immutable": True,
    }
    return incidence_rows, edge_rows, reciprocal_rows, minimal_rows, ledger


def identifier_strings(value: Any) -> list[str]:
    pattern = re.compile(
        r"^(?:restriction:|rn-restriction:|core:|physical-r1-face-component:"
        r"|base-r1-edge-cell:|path-cell:|gate5-word:)"
    )
    rows: list[str] = []
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


def round67_ledger(documents: dict[str, dict[str, Any]]) -> dict[str, Any]:
    r67_result = documents[R67]["result"]
    fixed = r67_result["actual_fixed_j_subroot"]
    require(fixed["status"] == "CERTIFIED_GRAPH_SUPPORTED_PHYSICAL_SUBROOT",
            "Round67 physical subroot")
    require(
        fixed["base_law"] == "finite standard-Borel endpoint-coarea occurrence law m_occ",
        "Round67 occurrence law",
    )
    require(
        "OWNER_TO_EXACT_RETURN_GRAPH_PATH_COMPONENT"
        in r67_result["minimal_spanning_registry"]["open_edges"],
        "Round67 open owner/path edge",
    )
    require(identifier_strings(r67_result) == [], "Round67 materialized IDs absent")
    required = [
        "restriction_id", "return_component", "insertion_time",
        "collision_index", "event_signature", "primitive_key", "owner_key",
        "rank_zero_component", "plaque_side", "word_cell",
        "endpoint_coordinate", "root_coordinate",
    ]
    common = documents[R68]["result"]["common_root_join"]
    require(common["required_fields"] == required, "Round68 required key")
    require(common["actual_joined_fields"] == "0/12", "Round68 0/12")
    require(
        common["status"]
        == "EXACT_JOIN_CRITERION_CERTIFIED__ACTUAL_CROSSWALK_ABSENT",
        "Round68 absent crosswalk",
    )
    r69 = documents[R69]["result"]
    obstruction = r69["direct_equality_obstruction"]
    correction = r69["typed_incidence_correction"]
    require(
        obstruction["selected_base_root_occurrence_pair_count"] == 11264
        and obstruction["selected_base_root_occurrence_intersection_count"] == 0
        and obstruction["recordwise_source_point_equality_is_correct_join"] is False,
        "Round69 equality obstruction",
    )
    require(
        correction["node_sorts"]
        == ["path_cell", "physical_face", "one_sided_trace"],
        "Round69 typed nodes",
    )
    require(
        correction["edge_semantics"]
        == "FACE_IS_BOUNDARY_OR_PULLBACK_CARRIER_INCIDENT_TO_PATH_CELL__NOT_EQUAL_TO_INTERIOR_POINT",
        "Round69 edge semantics",
    )
    return {
        "status":
            "NOT_CERTIFIED__ROUND67_OCCURRENCE_OWNER_TO_BASE_R1_COMPONENT_CROSSWALK_0_ROWS",
        "round67_fixed_j_root_status": fixed["status"],
        "round67_materialized_recordwise_identifier_count": 0,
        "round67_to_round72_component_crosswalk_row_count": 0,
        "required_recordwise_composite_key_fields": required,
        "required_recordwise_composite_key_field_count": 12,
        "currently_joined_required_fields": "0/12",
        "missing_required_fields": required,
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


def aq(value: Q | int) -> arb:
    value = Q(value)
    return arb(value.numerator) / value.denominator


def arb_interval(lower: Q, upper: Q) -> arb:
    require(lower <= upper, "ordered interval")
    middle = (lower + upper) / 2
    radius = (upper - lower) / 2
    return arb(aq(middle), aq(radius))


def target_center(target: str) -> tuple[arb, arb]:
    obstacle = target[0]
    ix, iy = map(int, target[2:-1].split(","))
    offset = Q(1, 2) if obstacle == "W" else Q(0)
    return aq(Q(ix) + offset), aq(Q(iy) + offset)


def collision(
    qx: arb, qy: arb, ux: arb, uy: arb, target: str
) -> tuple[arb, arb, arb]:
    cx, cy = target_center(target)
    radius = aq(Q(4, 25) if target[0] == "W" else Q(9, 25))
    dx, dy = cx - qx, cy - qy
    longitudinal = ux * dx + uy * dy
    transverse = -uy * dx + ux * dy
    discriminant = radius * radius - transverse * transverse
    require(bool(discriminant > 0), "first collision discriminant")
    flight = longitudinal - discriminant.sqrt()
    require(
        bool(flight > 0) and bool(flight < aq(Q(3))),
        "first collision strict flight window",
    )
    hit_x, hit_y = qx + flight * ux, qy + flight * uy
    return (hit_x - cx) / radius, (hit_y - cy) / radius, transverse / radius


def verify_coarse_geometry(r121_result: dict[str, Any]) -> dict[str, str]:
    """Fresh interval replay from the pinned anchor bracket, not Round128 code."""
    ctx.prec = PRECISION_BITS
    bracket = r121_result["exact_parent_W_witness_rows"][0][
        "anchor_t_unique_root_dyadic_bracket"
    ]
    require(
        type(bracket) is list and len(bracket) == 2
        and all(type(value) is str for value in bracket),
        "anchor bracket type",
    )
    lower, upper = map(Q, bracket)
    require(Q(0) < lower < upper < Q(1), "anchor bracket range")
    tstar = arb_interval(lower, upper)
    theta_star = arb.pi() - tstar.asin()
    x = arb_interval(Q(0), Q(1))
    delta = aq(Q(1, 10**90))
    theta0 = theta_star + aq(Q(25, 61)) * delta * x
    phi0 = aq(Q(1, 16384)).acos() + aq(Q(36, 61)) * delta * x
    c0 = phi0.cos()
    normal_x, normal_y = theta0.cos(), theta0.sin()
    p0 = (arb(1) - c0 * c0).sqrt()
    source_radius = aq(Q(9, 25))
    qx, qy = source_radius * normal_x, source_radius * normal_y
    ux = c0 * normal_x - p0 * normal_y
    uy = c0 * normal_y + p0 * normal_x
    first_nx, first_ny, first_p = collision(
        qx, qy, ux, uy, "W[-1,-1]"
    )
    require(bool(first_nx > aq(Q(1, 2))), "fresh exact t lower")
    require(bool(first_nx < aq(Q(3, 5))), "fresh exact t upper")
    require(bool(first_p > aq(-Q(1, 2))), "fresh exact p lower")
    require(bool(first_p < aq(-Q(2, 5))), "fresh exact p upper")
    require(bool(first_ny > abs(first_nx)), "fresh N chart")
    return {
        "fresh_t_strict_outer_interval": "(1/2,3/5)",
        "fresh_p_strict_outer_interval": "(-1/2,-2/5)",
        "core_t_interval": "[69/100,7/10]",
        "core_p_interval": "[-1/50,1/50]",
    }


def load_closed_pinned(name: str, schema: str) -> dict[str, Any]:
    require(sha256(HERE / name) == PINS[name], f"closed pin:{name}")
    return closed_document(HERE / name, schema)["result"]


def overlap_and_geometry(
    incidence_rows: list[dict[str, Any]],
    cores: tuple[Core, ...],
    pair_index: dict[tuple[str, str], int],
    pattern_index: dict[tuple[str, ...], int],
) -> tuple[dict[str, Any], dict[str, str], list[str]]:
    r121 = load_closed_pinned(
        R121, "cm2.round121.rank3-exact-seed-three-leg-recut-f5f6.v1"
    )
    r121v = load_closed_pinned(
        R121V,
        "cm2.round121.rank3-exact-seed-three-leg-recut-f5f6-verification.v1",
    )
    require(r121v["verdict"] == "PASS", "Round121 PASS")
    require(r121v["certificate_sha256"] == PINS[R121],
            "Round121 verification pin")
    exact_words = r121["whole_seed_owner_candidate_replay"][
        "official_word_key_ids"
    ]
    require(
        exact_words == [
            "gate5-word:102441:3ef7afa1895a984d7edeab7005cfcb7daed7ae8aa07f0767bdd9144da94749ba",
            OVERLAP_WORD,
            "gate5-word:180256:564ba69e20fe29980fb28d97a50efa2326d024c92c36c930bdb4a2157c3335c8",
        ],
        "ordered exact words",
    )
    incidence_words = {row["source_official_word_key_id"] for row in incidence_rows}
    require(sorted(incidence_words & set(exact_words)) == [OVERLAP_WORD],
            "unique exact overlap")
    overlap_rows = [
        row for row in incidence_rows
        if row["source_official_word_key_id"] == OVERLAP_WORD
    ]
    overlap_components = [row["component_id"] for row in overlap_rows]
    require(overlap_components == [
        "physical-r1-face-component:5665deaf6fe5dc6163676aa73a59b5de27e6fe71adb067c2cabc12bdbe819b6d",
        "physical-r1-face-component:6414b54d08832086e74ced78c1e7c7052092194e12daa89b744f5b3cccf8b214",
    ], "two overlap components")
    destination_words = sorted({
        row["destination_official_word_key_id"] for row in overlap_rows
    })
    destination_word = (
        "gate5-word:102440:cbb373c48bf58a17e8d26dc1623681635b9ea131f736d43871304579b0e30e16"
    )
    require(destination_words == [destination_word], "overlap destination")
    core = cores[16]
    require(
        (core.chart, core.target, core.crossings, core.t0, core.t1,
         core.p0, core.p1)
        == ("W:N", "G[1,1]", (), Q(69, 100), Q(7, 10),
            -Q(1, 50), Q(1, 50)),
        "core16 rectangle",
    )
    row, pair, pattern, ordinal, identifier = official_word(
        core, pair_index, pattern_index
    )
    require(
        (row, pair, pattern, ordinal, identifier)
        == (["W:N", "G[1,1]", [], 1], 352, 0, 346720, OVERLAP_WORD),
        "core16 official word",
    )
    require(
        r121["whole_seed_owner_candidate_replay"]["selected_collision_charts"][0]
        == "N",
        "Round121 first chart",
    )
    require(
        r121["whole_seed_owner_candidate_replay"]["ordered_owner_ids"][:2]
        == ["W[-1,-1]", "G[0,0]"],
        "Round121 first owners",
    )
    geometry = verify_coarse_geometry(r121)
    return {
        "status":
            "CERTIFIED_ONE_SYMBOLIC_WORD_OVERLAP_AND_STRICT_PHYSICAL_COORDINATE_DISJOINTNESS",
        "exact_seed_official_word_count": 3,
        "base_R1_incidence_official_word_count": 16,
        "overlap_official_word_count": 1,
        "overlap_official_word_key_id": OVERLAP_WORD,
        "overlap_word_key_row": row,
        "overlap_word_pair_index": pair,
        "overlap_crossing_pattern_index": pattern,
        "overlap_official_word_ordinal": ordinal,
        "overlap_component_count": 2,
        "overlap_component_ids": overlap_components,
        "overlap_directed_edge_destination_official_word_key_id": destination_word,
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
            "t_equals_first_normal_x_certified_strict_outer_interval":
                ["1/2", "3/5"],
            "p_equals_first_collision_momentum_certified_strict_outer_interval":
                ["-1/2", "-2/5"],
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
        "word_equality_cannot_join_Round72_fields_to_Round121_exact_seed_slots":
            True,
    }, geometry, exact_words


def scoped_nonempty(
    cores: tuple[Core, ...],
    pair_index: dict[tuple[str, str], int],
    pattern_index: dict[tuple[str, ...], int],
    exact_words: list[str],
) -> dict[str, Any]:
    r127 = load_closed_pinned(
        R127, "cm2.round127.global-return-word-exact-seed-crosswalk.v1"
    )
    r127v = load_closed_pinned(
        R127V,
        "cm2.round127.global-return-word-exact-seed-crosswalk-verification.v1",
    )
    require(r127v["status"] == "PASS", "Round127 PASS")
    require(r127v["certificate_sha256"] == PINS[R127],
            "Round127 verification pin")
    r127_ids = sorted(
        row["official_word_key_id"]
        for row in r127["exact_path_official_word_registry_incidence_rows"]
    )
    require(r127_ids == sorted(exact_words), "Round127/Round121 exact words")
    gate25_ids = sorted(
        official_word(core, pair_index, pattern_index)[4] for core in cores
    )
    require(len(gate25_ids) == len(set(gate25_ids)) == 24, "24 Gate25 words")
    intersection = sorted(set(gate25_ids) & set(exact_words))
    union_ids = sorted(set(gate25_ids) | set(exact_words))
    require(intersection == [OVERLAP_WORD], "Gate25/exact intersection")
    require(len(union_ids) == 26, "scoped union 26")
    symbolic = r127["symbolic_registry_incidence"]
    require(
        symbolic["global_exact_nonempty_candidate_key_count"] is None
        and symbolic["global_complete_nonempty_or_empty_domain_decisions"] is False,
        "Round127 no global census",
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


def expected_result() -> tuple[dict[str, Any], dict[str, Any]]:
    require(flint.__version__ == "0.9.0", "python-flint version")
    documents = validate_all_pins()
    (_pairs, _patterns, pair_index, pattern_index,
     global_replay) = replay_registry(documents[GLOBAL])
    cores = physical_cores()
    gate25_replay = replay_gate25(
        documents[GATE25], cores, pair_index, pattern_index
    )
    (
        incidence_rows, edge_rows, reciprocal_rows, minimal_rows,
        incidence_ledger,
    ) = replay_components(
        documents, cores, pair_index, pattern_index
    )
    b_ledger = round67_ledger(documents)
    c_ledger, geometry, exact_words = overlap_and_geometry(
        incidence_rows, cores, pair_index, pattern_index
    )
    c2_ledger = scoped_nonempty(
        cores, pair_index, pattern_index, exact_words
    )
    r121 = load_closed_pinned(
        R121, "cm2.round121.rank3-exact-seed-three-leg-recut-f5f6.v1"
    )
    require(
        r121["gate5_global_maturity"] == "10/18"
        and r121["complete_18_field_block_count"] == 0
        and r121["gate5_block_count"] == 0
        and r121["cm2_verdict"] == "NO-GO_FOR_CLAIM",
        "Round121 global safety",
    )
    frontier = documents[R72]["result"]["strict_frontier"]
    require(
        frontier["Gate5"] == "NOT_CERTIFIED__MATURITY_10_OF_18_BLOCKS_0"
        and frontier["CM2"] == "NO-GO_FOR_CLAIM",
        "Round72 safety",
    )
    result = {
        "precision_bits": 1024,
        "python_flint_version": "0.9.0",
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
            "reciprocal_word_pair_rows": reciprocal_rows,
            "minimal_mapping_rows": minimal_rows,
        },
        "B_Round67_occurrence_owner_crosswalk_fail_closed": b_ledger,
        "C_exact_seed_overlap_and_coordinate_separation": c_ledger,
        "C2_scoped_locally_certified_nonempty_key_lower_bound": c2_ledger,
        "D_global_safety_and_nonpromotion": {
            "status": "LOCAL_INCIDENCE_PROGRESS_ONLY__NO_GLOBAL_GATE_UPGRADE",
            "global_candidate_word_count": 441280,
            "locally_incidence_attached_official_word_count": 16,
            "symbolic_membership_fraction": "16/441280",
            "symbolic_membership_fraction_is_not_domain_measure_or_coverage": True,
            "locally_certified_nonempty_key_lower_bound": 26,
            "global_exact_nonempty_candidate_key_count": None,
            "complete_global_nonempty_or_empty_domain_census": False,
            "Round72_numeric_F10_F13_F16_rows_remain_physical_face_component_local":
                True,
            "incidence_rows_are_not_18_field_operator_slot_rows": True,
            "Round67_owner_to_path_crosswalk_row_count": 0,
            "arbitrary_return_depth_certified": False,
            "all_parameter_fibres_certified": False,
            "global_complete_18_field_block_count": 0,
            "gate5_block_count": 0,
            "gate5_global_maturity": "10/18",
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
            "no_Round72_component_is_promoted_into_a_Round121_exact_seed_block":
                True,
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
    audit = {
        "global_registry": global_replay,
        "Gate25": gate25_replay,
        "component_incidence_count": len(incidence_rows),
        "directed_edge_count": len(edge_rows),
        "reciprocal_pair_count": len(reciprocal_rows),
        "geometry": geometry,
        "Round67_joined_fields": "0/12",
        "scoped_nonempty_lower_bound": 26,
    }
    return result, audit


def evaluate_document(
    document: dict[str, Any], expected: dict[str, Any]
) -> None:
    require(type(document) is dict, "top-level object")
    require(
        set(document) == {"schema", "result", "result_sha256"},
        "closed certificate envelope",
    )
    require(document["schema"] == CERTIFICATE_SCHEMA, "certificate schema")
    require(type(document["result"]) is dict, "certificate result object")
    require(
        document["result_sha256"] == digest(document["result"]),
        "certificate result closure",
    )
    require(document["result"] == expected, "independent expected result equality")


def evaluate_bytes(raw: bytes, expected: dict[str, Any]) -> dict[str, Any]:
    document = parse_bytes(raw, certificate_mode=True)
    evaluate_document(document, expected)
    return document


def read_certificate(path: Path, expected: dict[str, Any]) -> dict[str, Any]:
    require(path.is_file() and not path.is_symlink(), "certificate file")
    require(sha256(path) == CERTIFICATE_SHA256, "official certificate byte pin")
    document = evaluate_bytes(path.read_bytes(), expected)
    require(
        document["result_sha256"] == CERTIFICATE_RESULT_SHA256,
        "official certificate result pin",
    )
    return document


def semantic_mutations(
    document: dict[str, Any], expected: dict[str, Any]
) -> list[str]:
    def set_path(value: Any, path: tuple[Any, ...], replacement: Any) -> None:
        node = value
        for key in path[:-1]:
            node = node[key]
        node[path[-1]] = replacement

    def rehash_row(row: dict[str, Any]) -> None:
        row.pop("row_sha256", None)
        row["row_sha256"] = digest(row)

    def area(result: dict[str, Any]) -> dict[str, Any]:
        return result["A_base_R1_component_to_global_word_incidence"]

    def rehash_component_rows(result: dict[str, Any]) -> None:
        a = area(result)
        a["component_incidence_rows_sha256"] = digest(
            a["component_incidence_rows"]
        )

    def rehash_edge_rows(result: dict[str, Any]) -> None:
        a = area(result)
        a["source_destination_word_edge_rows_sha256"] = digest(
            a["source_destination_word_edge_rows"]
        )

    def rehash_pair_rows(result: dict[str, Any]) -> None:
        a = area(result)
        a["reciprocal_pair_rows_sha256"] = digest(
            a["reciprocal_word_pair_rows"]
        )

    def component_change(
        doc: dict[str, Any], change: Callable[[dict[str, Any]], None]
    ) -> None:
        row = area(doc["result"])["component_incidence_rows"][0]
        change(row)
        rehash_row(row)
        rehash_component_rows(doc["result"])

    def edge_change(
        doc: dict[str, Any], change: Callable[[dict[str, Any]], None]
    ) -> None:
        row = area(doc["result"])["source_destination_word_edge_rows"][0]
        change(row)
        rehash_row(row)
        rehash_edge_rows(doc["result"])

    def pair_change(
        doc: dict[str, Any], change: Callable[[dict[str, Any]], None]
    ) -> None:
        row = area(doc["result"])["reciprocal_word_pair_rows"][0]
        change(row)
        rehash_row(row)
        rehash_pair_rows(doc["result"])

    def swap_roles(row: dict[str, Any]) -> None:
        suffixes = (
            "core_index", "core_id", "official_word_row",
            "official_word_pair_index", "crossing_pattern_index",
            "official_word_ordinal", "official_word_key_id",
        )
        for suffix in suffixes:
            source_key, destination_key = f"source_{suffix}", f"destination_{suffix}"
            if source_key in row and destination_key in row:
                row[source_key], row[destination_key] = (
                    row[destination_key], row[source_key]
                )

    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
        ("certificate schema altered",
         lambda d: d.__setitem__("schema", "cm2.round128.tampered.v1")),
        ("producer provenance pin altered",
         lambda d: d["result"]["provenance"]["strict_byte_pins"].__setitem__(
             PRODUCER.name, "0" * 64)),
        ("upstream Round71 pin altered",
         lambda d: d["result"]["provenance"]["strict_byte_pins"].__setitem__(
             R71, "0" * 64)),
        ("global candidate count promoted",
         lambda d: d["result"]["global_candidate_registry_replay"].__setitem__(
             "candidate_return_word_key_count", 441281)),
        ("global registry stream digest altered",
         lambda d: d["result"]["global_candidate_registry_replay"].__setitem__(
             "candidate_word_row_stream_sha256", "0" * 64)),
        ("Gate25 core count altered",
         lambda d: d["result"]["Gate25_physical_core_replay"].__setitem__(
             "physical_core_count", 25)),
        ("Gate25 core ID digest altered",
         lambda d: d["result"]["Gate25_physical_core_replay"].__setitem__(
             "core_ids_sha256", "0" * 64)),
        ("component count altered",
         lambda d: area(d["result"]).__setitem__(
             "component_incidence_row_count", 31)),
        ("component source word row re-signed",
         lambda d: component_change(
             d, lambda row: row.__setitem__(
                 "source_official_word_row", ["W:N", "G[9,9]", [], 1]))),
        ("component source word ID re-signed",
         lambda d: component_change(
             d, lambda row: row.__setitem__(
                 "source_official_word_key_id", "gate5-word:000000:" + "0" * 64))),
        ("component source word ordinal re-signed",
         lambda d: component_change(
             d, lambda row: row.__setitem__(
                 "source_official_word_ordinal", 0))),
        ("component destination word row re-signed",
         lambda d: component_change(
             d, lambda row: row.__setitem__(
                 "destination_official_word_row", ["G:E", "W[9,9]", [], 1]))),
        ("component destination word ID re-signed",
         lambda d: component_change(
             d, lambda row: row.__setitem__(
                 "destination_official_word_key_id",
                 "gate5-word:999999:" + "f" * 64))),
        ("component destination ordinal re-signed",
         lambda d: component_change(
             d, lambda row: row.__setitem__(
                 "destination_official_word_ordinal", 999999))),
        ("component source destination roles swapped and re-signed",
         lambda d: component_change(d, swap_roles)),
        ("component numeric attachment moved to destination",
         lambda d: component_change(
             d, lambda row: row.__setitem__(
                 "numeric_F10_F13_F16_attachment_role",
                 "destination_official_word"))),
        ("component ID orphan re-signed",
         lambda d: component_change(
             d, lambda row: row.__setitem__(
                 "component_id", "physical-r1-face-component:" + "0" * 64))),
        ("component path-cell orphan re-signed",
         lambda d: component_change(
             d, lambda row: row.__setitem__(
                 "path_cell_id", "base-r1-edge-cell:" + "0" * 64))),
        ("component source core orphan re-signed",
         lambda d: component_change(
             d, lambda row: row.__setitem__(
                 "source_core_id", "core:" + "0" * 64))),
        ("component trace orphan re-signed",
         lambda d: component_change(
             d, lambda row: row["trace_rows"][0].__setitem__(
                 "trace_id", "physical-r1-trace:" + "0" * 64))),
        ("component face side altered re-signed",
         lambda d: component_change(
             d, lambda row: row.__setitem__("component_face_side", "t_upper"))),
        ("component F10 altered re-signed",
         lambda d: component_change(
             d, lambda row: row["numeric_local_fields"].__setitem__(
                 "F10_integer_upper", 999))),
        ("component row hash directly altered",
         lambda d: area(d["result"])["component_incidence_rows"][0].__setitem__(
             "row_sha256", "0" * 64)),
        ("component aggregate digest directly altered",
         lambda d: area(d["result"]).__setitem__(
             "component_incidence_rows_sha256", "0" * 64)),
        ("component row order changed with aggregate re-signed",
         lambda d: (
             area(d["result"])["component_incidence_rows"].__setitem__(
                 slice(0, 2),
                 list(reversed(area(d["result"])["component_incidence_rows"][:2]))
             ),
             rehash_component_rows(d["result"]),
         )),
        ("component row deleted with aggregate re-signed",
         lambda d: (
             area(d["result"])["component_incidence_rows"].pop(),
             rehash_component_rows(d["result"]),
         )),
        ("component row duplicated with aggregate re-signed",
         lambda d: (
             area(d["result"])["component_incidence_rows"].append(
                 copy.deepcopy(area(d["result"])["component_incidence_rows"][0])
             ),
             rehash_component_rows(d["result"]),
         )),
        ("edge count altered",
         lambda d: area(d["result"]).__setitem__(
             "directed_source_destination_word_edge_count", 15)),
        ("edge source word ID re-signed",
         lambda d: edge_change(
             d, lambda row: row.__setitem__(
                 "source_official_word_key_id", "gate5-word:000000:" + "0" * 64))),
        ("edge destination word ID re-signed",
         lambda d: edge_change(
             d, lambda row: row.__setitem__(
                 "destination_official_word_key_id",
                 "gate5-word:999999:" + "f" * 64))),
        ("edge source destination roles swapped and re-signed",
         lambda d: edge_change(d, swap_roles)),
        ("edge attachment moved to destination",
         lambda d: edge_change(
             d, lambda row: row.__setitem__(
                 "numeric_F10_F13_F16_attachment_role",
                 "destination_official_word"))),
        ("edge component IDs duplicated and re-signed",
         lambda d: edge_change(
             d, lambda row: row["component_ids"].__setitem__(
                 1, row["component_ids"][0]))),
        ("edge path-cell orphan re-signed",
         lambda d: edge_change(
             d, lambda row: row.__setitem__(
                 "path_cell_id", "base-r1-edge-cell:" + "0" * 64))),
        ("edge direction broken re-signed",
         lambda d: edge_change(
             d, lambda row: row.__setitem__(
                 "destination_core_id", row["source_core_id"]))),
        ("edge row order changed with aggregate re-signed",
         lambda d: (
             area(d["result"])["source_destination_word_edge_rows"].__setitem__(
                 slice(0, 2),
                 list(reversed(
                     area(d["result"])["source_destination_word_edge_rows"][:2]
                 ))
             ),
             rehash_edge_rows(d["result"]),
         )),
        ("reciprocal pair count altered",
         lambda d: area(d["result"]).__setitem__(
             "reciprocal_unordered_word_pair_count", 7)),
        ("reciprocal edge orphan re-signed",
         lambda d: pair_change(
             d, lambda row: row["directed_edge_row_ids"].__setitem__(
                 0, "round128-directed-word-to-word-edge:" + "0" * 64))),
        ("reciprocal direction flag false re-signed",
         lambda d: pair_change(
             d, lambda row: row.__setitem__(
                 "exactly_two_reverse_directions", False))),
        ("reciprocal word IDs duplicated re-signed",
         lambda d: pair_change(
             d, lambda row: row["directed_source_official_word_key_ids"].__setitem__(
                 1, row["directed_source_official_word_key_ids"][0]))),
        ("Round67 zero of twelve promoted",
         lambda d: d["result"][
             "B_Round67_occurrence_owner_crosswalk_fail_closed"
         ].__setitem__("currently_joined_required_fields", "1/12")),
        ("Round67 missing key deleted",
         lambda d: d["result"][
             "B_Round67_occurrence_owner_crosswalk_fail_closed"
         ]["missing_required_fields"].pop()),
        ("Round67 crosswalk row invented",
         lambda d: d["result"][
             "B_Round67_occurrence_owner_crosswalk_fail_closed"
         ].__setitem__("round67_to_round72_component_crosswalk_row_count", 1)),
        ("Round67 required field count altered",
         lambda d: d["result"][
             "B_Round67_occurrence_owner_crosswalk_fail_closed"
         ].__setitem__("required_recordwise_composite_key_field_count", 11)),
        ("overlap official word altered",
         lambda d: d["result"][
             "C_exact_seed_overlap_and_coordinate_separation"
         ].__setitem__("overlap_official_word_key_id", "gate5-word:000000:" + "0" * 64)),
        ("overlap promoted to same physical root",
         lambda d: d["result"][
             "C_exact_seed_overlap_and_coordinate_separation"
         ].__setitem__("same_physical_root", True)),
        ("overlap promoted to same operator block",
         lambda d: d["result"][
             "C_exact_seed_overlap_and_coordinate_separation"
         ].__setitem__("same_operator_block", True)),
        ("destination 102440 changed to exact stage0 102441",
         lambda d: d["result"][
             "C_exact_seed_overlap_and_coordinate_separation"
         ].__setitem__(
             "overlap_directed_edge_destination_official_word_key_id",
             "gate5-word:102441:3ef7afa1895a984d7edeab7005cfcb7daed7ae8aa07f0767bdd9144da94749ba")),
        ("destination 102440 changed to exact stage2 180256",
         lambda d: d["result"][
             "C_exact_seed_overlap_and_coordinate_separation"
         ].__setitem__(
             "overlap_directed_edge_destination_official_word_key_id",
             "gate5-word:180256:564ba69e20fe29980fb28d97a50efa2326d024c92c36c930bdb4a2157c3335c8")),
        ("coarse t interval expanded across core",
         lambda d: d["result"][
             "C_exact_seed_overlap_and_coordinate_separation"
         ]["Round121_exact_stage1_local_coordinates"].__setitem__(
             "t_equals_first_normal_x_certified_strict_outer_interval",
             ["1/2", "7/10"])),
        ("coarse p interval expanded across core",
         lambda d: d["result"][
             "C_exact_seed_overlap_and_coordinate_separation"
         ]["Round121_exact_stage1_local_coordinates"].__setitem__(
             "p_equals_first_collision_momentum_certified_strict_outer_interval",
             ["-1/2", "1/50"])),
        ("overlap component count altered",
         lambda d: d["result"][
             "C_exact_seed_overlap_and_coordinate_separation"
         ].__setitem__("overlap_component_count", 3)),
        ("local lower bound altered",
         lambda d: d["result"][
             "C2_scoped_locally_certified_nonempty_key_lower_bound"
         ].__setitem__("locally_certified_nonempty_key_lower_bound", 27)),
        ("local lower bound promoted to global exact census",
         lambda d: d["result"][
             "C2_scoped_locally_certified_nonempty_key_lower_bound"
         ].__setitem__("global_exact_nonempty_candidate_key_count", 26)),
        ("global domain census falsely completed",
         lambda d: d["result"][
             "C2_scoped_locally_certified_nonempty_key_lower_bound"
         ].__setitem__("complete_global_nonempty_or_empty_domain_census", True)),
        ("scoped union count altered",
         lambda d: d["result"][
             "C2_scoped_locally_certified_nonempty_key_lower_bound"
         ].__setitem__("set_union_count", 27)),
        ("global safety null promoted to 26",
         lambda d: d["result"]["D_global_safety_and_nonpromotion"].__setitem__(
             "global_exact_nonempty_candidate_key_count", 26)),
        ("global complete block invented",
         lambda d: d["result"]["D_global_safety_and_nonpromotion"].__setitem__(
             "global_complete_18_field_block_count", 1)),
        ("Gate5 block invented",
         lambda d: d["result"]["D_global_safety_and_nonpromotion"].__setitem__(
             "gate5_block_count", 1)),
        ("Gate5 promoted",
         lambda d: d["result"]["D_global_safety_and_nonpromotion"].__setitem__(
             "Gate5", "CERTIFIED")),
        ("CM2 promoted",
         lambda d: d["result"]["D_global_safety_and_nonpromotion"].__setitem__(
             "CM2", "GO_FOR_CLAIM")),
        ("arbitrary return depth promoted",
         lambda d: d["result"]["D_global_safety_and_nonpromotion"].__setitem__(
             "arbitrary_return_depth_certified", True)),
        ("strict nonclaim deleted",
         lambda d: d["result"]["strict_nonclaims"].pop()),
        ("unknown result field added",
         lambda d: d["result"].__setitem__("global_upgrade", True)),
    ]
    rejected: list[str] = []
    for label, mutate in mutations:
        candidate = copy.deepcopy(document)
        mutate(candidate)
        candidate["result_sha256"] = digest(candidate["result"])
        try:
            evaluate_document(candidate, expected)
        except Exception:
            rejected.append(label)
        else:
            raise VerificationError(f"semantic mutation accepted:{label}")
    return rejected


def strict_json_attacks(
    document: dict[str, Any], expected: dict[str, Any]
) -> list[str]:
    raw = (
        json.dumps(
            document, sort_keys=True, indent=2, ensure_ascii=True,
            allow_nan=False,
        ) + "\n"
    ).encode()
    attacks: list[tuple[str, bytes]] = [
        (
            "duplicate top-level schema key",
            raw.replace(
                b'{\n  "result":',
                b'{\n  "schema": "duplicate",\n  "result":',
                1,
            ),
        ),
        (
            "duplicate nested status key",
            raw.replace(
                b'"A_base_R1_component_to_global_word_incidence": {',
                b'"A_base_R1_component_to_global_word_incidence": {"status":"duplicate",',
                1,
            ),
        ),
        (
            "floating-point integer",
            raw.replace(b'"precision_bits": 1024', b'"precision_bits": 1024.0', 1),
        ),
        (
            "NaN constant",
            raw.replace(b'"precision_bits": 1024', b'"precision_bits": NaN', 1),
        ),
        (
            "positive Infinity constant",
            raw.replace(b'"precision_bits": 1024', b'"precision_bits": Infinity', 1),
        ),
        (
            "negative Infinity constant",
            raw.replace(b'"precision_bits": 1024', b'"precision_bits": -Infinity', 1),
        ),
        ("UTF-8 BOM", b"\xef\xbb\xbf" + raw),
        ("invalid UTF-8", raw[:-2] + b"\xff}\n"),
        ("top-level array", b"[]\n"),
        ("top-level null", b"null\n"),
        ("trailing second document", raw + b"{}\n"),
        (
            "oversized integer",
            raw.replace(
                b'"precision_bits": 1024',
                b'"precision_bits": 999999999999999999999999999999999999999',
                1,
            ),
        ),
        (
            "negative zero",
            raw.replace(b'"precision_bits": 1024', b'"precision_bits": -0', 1),
        ),
        (
            "leading-zero integer",
            raw.replace(b'"precision_bits": 1024', b'"precision_bits": 01024', 1),
        ),
    ]
    extra_top = copy.deepcopy(document)
    extra_top["extra"] = True
    attacks.append(("closed envelope extra key", canonical(extra_top).encode()))
    extra_result = copy.deepcopy(document)
    extra_result["result"]["extra"] = True
    extra_result["result_sha256"] = digest(extra_result["result"])
    attacks.append(("closed result extra key", canonical(extra_result).encode()))
    stale = copy.deepcopy(document)
    stale["result"]["precision_bits"] = 2048
    attacks.append(("stale outer result digest", canonical(stale).encode()))
    surrogate = copy.deepcopy(document)
    surrogate["result"]["strict_nonclaims"][0] = "\ud800"
    surrogate["result_sha256"] = digest(surrogate["result"])
    attacks.append((
        "unpaired surrogate",
        json.dumps(surrogate, sort_keys=True, ensure_ascii=True).encode(),
    ))
    rejected: list[str] = []
    for label, attack in attacks:
        try:
            evaluate_bytes(attack, expected)
        except Exception:
            rejected.append(label)
        else:
            raise VerificationError(f"strict JSON attack accepted:{label}")
    return rejected


def verification_document(
    certificate_path: Path,
    certificate: dict[str, Any],
    audit: dict[str, Any],
    mutation_labels: list[str],
    strict_labels: list[str],
) -> dict[str, Any]:
    result = {
        "status": "PASS",
        "certificate_schema": CERTIFICATE_SCHEMA,
        "certificate_sha256": sha256(certificate_path),
        "certificate_result_sha256": certificate["result_sha256"],
        "producer_sha256": sha256(PRODUCER),
        "verifier_sha256": sha256(VERIFIER),
        "independence_contract": {
            "Round128_producer_imported": False,
            "Round128_producer_executed": False,
            "global_registry_independently_replayed": True,
            "Gate25_core_definitions_independently_reconstructed": True,
            "Round71_Round72_component_join_independently_replayed": True,
            "Round69_directed_edge_set_independently_cross_checked": True,
            "Round121_geometry_replayed_from_pinned_anchor_bracket_at_2048_bits":
                True,
        },
        "replay_audit": audit,
        "semantic_mutation_test_count": len(mutation_labels),
        "semantic_mutation_rejection_labels": mutation_labels,
        "strict_json_attack_count": len(strict_labels),
        "strict_json_attack_rejection_labels": strict_labels,
        "determinism_contract": {
            "canonical_JSON_sort_keys": True,
            "no_hash_iteration_controls_output": True,
            "verification_replay_is_PYTHONHASHSEED_independent": True,
        },
        "safety": {
            "locally_certified_nonempty_key_lower_bound": 26,
            "global_exact_nonempty_candidate_key_count": None,
            "global_complete_18_field_block_count": 0,
            "Gate5": "NOT_CERTIFIED",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }
    return {
        "schema": VERIFICATION_SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    try:
        require(not args.output.is_symlink(), "output symlink forbidden")
        require(
            not args.output.exists() or args.output.is_file(),
            "output must be absent or a regular file",
        )
        protected_inputs = [
            args.certificate, CERTIFICATE, PRODUCER, VERIFIER,
            *(HERE / name for name in PINS),
        ]
        require(
            all(
                args.output.resolve() != protected.resolve()
                for protected in protected_inputs
            ),
            "output must not resolve to an input or source",
        )
        if args.output.exists():
            require(
                all(
                    not args.output.samefile(protected)
                    for protected in protected_inputs
                ),
                "output hardlink to an input or source forbidden",
            )
        expected, audit = expected_result()
        certificate = read_certificate(args.certificate, expected)
        # Attack suites are filled below; keeping the calls here makes output
        # impossible until every fail-closed self-test has passed.
        mutation_labels = semantic_mutations(certificate, expected)
        strict_labels = strict_json_attacks(certificate, expected)
        document = verification_document(
            args.certificate, certificate, audit, mutation_labels, strict_labels
        )
        payload = json.dumps(
            document, indent=2, sort_keys=True, ensure_ascii=True,
            allow_nan=False,
        ) + "\n"
        args.output.write_text(payload, encoding="utf-8")
        print("PASS")
        print(f"verification_result_sha256={document['result_sha256']}")
        print(f"semantic_mutations={len(mutation_labels)}")
        print(f"strict_json_attacks={len(strict_labels)}")
        return 0
    except (
        VerificationError, OSError, UnicodeError, ValueError, TypeError,
        KeyError, IndexError, ArithmeticError, json.JSONDecodeError,
    ) as exc:
        print(f"ROUND128_VERIFICATION_ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
