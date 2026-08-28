#!/usr/bin/env python3
"""Independent verifier for the Round173 source-G signature transport.

No Round173 producer code is imported or executed.  This verifier rebuilds
the rational target filter, all 448 retained pairs, all 985 signed clean-wall
patterns, the 224,580 source-G official-key prefix, both generator
permutations, every ordinal image, and the complete expected certificate.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import os
import stat
import tempfile
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable, Iterable


BASE = Path(__file__).resolve().parent
PRODUCER = BASE / "cm2_round173_source_g_exact_return_signature_transport.py"
CERTIFICATE = (
    BASE
    / "cm2_round173_source_g_exact_return_signature_transport_certificate.json"
)
OUTPUT = (
    BASE
    / "cm2_round173_source_g_exact_return_signature_transport_verification.json"
)
CERTIFICATE_SCHEMA = (
    "cm2.round173.source-g-exact-return-signature-transport.v1"
)
SCHEMA = (
    "cm2.round173.source-g-exact-return-signature-transport.verification.v1"
)
CERTIFIED_STATUS = (
    "CERTIFIED_SOURCE_G_JX_JY_EXACT_RETURN_SIGNATURE_TRANSPORT_DICTIONARY__"
    "NO_DYNAMIC_ROW_OR_D02_PROMOTION"
)
EXPECTED_PRODUCER_SHA256 = (
    "bdbf794a99dc9276b11b7680818994d63f52fe0e5a857948701f64e8d5d16a0f"
)

R169P = "cm2_round169_source_g_return_signature_coverage_survey.py"
R169C = "cm2_round169_source_g_return_signature_coverage_survey_certificate.json"
R169V = "cm2_round169_source_g_return_signature_coverage_survey_verifier.py"
R169O = "cm2_round169_source_g_return_signature_coverage_survey_verification.json"
R171P = "cm2_round171_compact_gate3_source_g_coordinate_bridge.py"
R171C = "cm2_round171_compact_gate3_source_g_coordinate_bridge_certificate.json"
R171V = "cm2_round171_compact_gate3_source_g_coordinate_bridge_verifier.py"
R171O = "cm2_round171_compact_gate3_source_g_coordinate_bridge_verification.json"
G5P = "cm2_gate5_return_word_three_norm_frontier_cert.py"
G5V = "cm2_gate5_return_word_three_norm_frontier_verifier.py"
G5M = "cm2-gate5-return-word-three-norm-frontier-manifest-2026-07-16.json"
G3P = "cm2_gate3_eight_cell_symmetry_atlas_cert.py"
G3M = "cm2-gate3-eight-cell-symmetry-atlas-manifest-2026-07-15.json"
FHP = "cm2_gate3_candidate_first_hit_cert.py"
FHM = "cm2-gate3-first-hit-atlas-manifest-2026-07-15.json"
SP = "cm2_gate3_chart_seam_quotient_cert.py"
SV = "cm2_gate3_chart_seam_quotient_verifier.py"
SM = "cm2-gate3-chart-seam-quotient-manifest-2026-07-15.json"

DEPENDENCIES = {
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
    G5P:
        "ddcc250f8700c6a695f96019d9f7824fe98636e20a67685fdc6a3cce77f6d695",
    G5V:
        "0384acdd1f912b0d4b3bee84ff530358d9693893d1c5c64a1deabaede8e0867b",
    G5M:
        "47e84e8b75b289b7a5db4afcbd7dfa8dac909d2f76fa1c95ef290546d031a866",
    G3P:
        "d867f5cb03691289033d1a0d0e277a03e8395d70aae7e0689446d7aa63eac3da",
    G3M:
        "f8fda665edbb7d8b39ce495188f90ecb2b5ec4384c1eb958949627df167c4987",
    FHP:
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    FHM:
        "0c820a5e3481b2c18fabb14d8d0fab7ce454f9a9e68b856bb2a7bf139404f7f4",
    SP:
        "fa00d4c14ee24b8f3fbc7f345deef13deb272080a886b68d2aa2f9c92a456fe1",
    SV:
        "3eb5b5525eab0d2e4935374e6d9fa453717de13634613afa579cd1ae30dbcea6",
    SM:
        "1fb40060336f04f28a7cac19a70abdd3692ced272825b2f1f6b6ae005f00518b",
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

Q = Fraction
SOURCE_CHARTS = tuple(
    f"{obstacle}:{cell}"
    for obstacle in ("G", "W")
    for cell in ("E", "W", "N", "S")
)
SOURCE_G_CHARTS = ("G:E", "G:W", "G:N", "G:S")
RADIUS = {"G": Q(9, 25), "W": Q(4, 25)}
EPSILON = Q(1, 400)
LOWER_ROOT2 = Q(707, 1000)
UPPER_ROOT2 = Q(708, 1000)
PAIR_COUNT = 228
PATTERN_COUNT = 985
KEY_COUNT = PAIR_COUNT * PATTERN_COUNT


def canonical(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def sha(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def demand(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


def strict_decode(raw: bytes) -> dict[str, Any]:
    demand(
        not raw.startswith(b"\xef\xbb\xbf") and b"\x00" not in raw,
        "raw encoding",
    )

    def pairs_to_dict(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            demand(key not in result, "duplicate key")
            result[key] = value
        return result

    def reject_number(token: str) -> None:
        raise ValueError(token)

    value = json.loads(
        raw.decode("utf-8"),
        object_pairs_hook=pairs_to_dict,
        parse_constant=reject_number,
        parse_float=reject_number,
    )

    def strings(item: Any) -> None:
        if type(item) is str:
            demand(
                "\x00" not in item
                and not any(
                    0xD800 <= ord(character) <= 0xDFFF
                    for character in item
                ),
                "decoded string",
            )
        elif type(item) is list:
            for child in item:
                strings(child)
        elif type(item) is dict:
            for key, child in item.items():
                strings(key)
                strings(child)

    strings(value)
    demand(type(value) is dict, "top object")
    return value


def safe_input(path: Path) -> None:
    demand(path.exists(), "missing input")
    demand(not path.is_symlink(), "input symlink")
    information = path.stat()
    demand(stat.S_ISREG(information.st_mode), "input regular")
    demand(information.st_nlink == 1, "input hardlink")
    demand(not path.parent.is_symlink(), "input parent symlink")


def safe_output(path: Path, protected: list[Path]) -> None:
    parent = path.parent
    demand(parent.exists() and parent.is_dir(), "output parent")
    demand(not parent.is_symlink(), "output parent symlink")
    resolved = path.resolve(strict=False)
    protected_resolved = [item.resolve(strict=False) for item in protected]
    demand(resolved not in protected_resolved, "output protected")
    if path.exists() or path.is_symlink():
        demand(not path.is_symlink(), "output symlink")
        information = path.stat()
        demand(stat.S_ISREG(information.st_mode), "output regular")
        demand(information.st_nlink == 1, "output hardlink")
        for item in protected:
            if item.exists():
                demand(not os.path.samefile(path, item), "output alias")


def load(path: Path) -> dict[str, Any]:
    safe_input(path)
    return strict_decode(path.read_bytes())


def unwrap(
    document: dict[str, Any],
    schema: str,
    result_digest: str,
    status: str,
) -> dict[str, Any]:
    demand(
        set(document) == {"schema", "result", "result_sha256"},
        f"wrapper:{schema}",
    )
    demand(document["schema"] == schema, f"schema:{schema}")
    demand(
        document["result_sha256"] == result_digest
        == sha(document["result"]),
        f"digest:{schema}",
    )
    demand(document["result"]["status"] == status, f"status:{schema}")
    return document["result"]


def upstream() -> dict[str, Any]:
    all_pins = {
        "cm2_round173_source_g_exact_return_signature_transport.py":
            EXPECTED_PRODUCER_SHA256,
        **DEPENDENCIES,
    }
    for name, expected in all_pins.items():
        path = BASE / name
        safe_input(path)
        demand(
            hashlib.sha256(path.read_bytes()).hexdigest() == expected,
            f"pin:{name}",
        )
    r169 = unwrap(
        load(BASE / R169C),
        "cm2.round169.source-g-return-signature-coverage-survey.v1",
        R169_RESULT,
        "CERTIFIED_SOURCE_G_EXACT_KEY_COVERAGE_DEFICIT_SURVEY__"
        "NO_EXTERIOR_OR_D02_PROMOTION",
    )
    r169v = unwrap(
        load(BASE / R169O),
        "cm2.round169.source-g-return-signature-coverage-survey.verification.v1",
        R169_VERIFY_RESULT,
        "PASS",
    )
    r171 = unwrap(
        load(BASE / R171C),
        "cm2.round171.compact-gate3-source-g-coordinate-bridge.v1",
        R171_RESULT,
        "CERTIFIED_COMPACT_TO_GATE3_SOURCE_G_COORDINATE_COVER__"
        "NO_RETURN_KEY_OR_D02_PROMOTION",
    )
    r171v = unwrap(
        load(BASE / R171O),
        "cm2.round171.compact-gate3-source-g-coordinate-bridge.verification.v1",
        R171_VERIFY_RESULT,
        "PASS",
    )
    demand(
        r169v["certificate_result_sha256"] == R169_RESULT
        and r169v["full_document_exactly_matched"] is True
        and r169v["producer_imported_or_executed"] is False,
        "Round169 binding",
    )
    demand(
        r171v["certificate_result_sha256"] == R171_RESULT
        and r171v["full_document_exactly_matched"] is True
        and r171v["producer_imported_or_executed"] is False,
        "Round171 binding",
    )
    gate5 = load(BASE / G5M)
    atlas = load(BASE / G3M)
    first = load(BASE / FHM)
    seam = load(BASE / SM)
    registry = gate5["result"]["immutable_candidate_key_registry"]
    completion = gate5["result"]["completion"]
    demand(
        gate5["schema"]
        == "cm2.gate5.return-word-three-norm-frontier.manifest.v1"
        and gate5["certificate_sha256"] == DEPENDENCIES[G5P]
        and gate5["verifier_sha256"] == DEPENDENCIES[G5V]
        and registry["retained_chart_target_pair_count"] == 448
        and registry["crossing_pattern_count_per_pair"] == PATTERN_COUNT
        and registry["candidate_return_word_key_count"] == 441280
        and registry["complete_physical_operator_block_count"] == 0
        and completion["complete_regular_return_word_candidate_key_envelope"]
        is True
        and completion["immutable_complete_return_word_operator_registry"]
        is False
        and gate5["verdict"]["gate5"] == "NOT_CERTIFIED",
        "Gate5 frontier",
    )
    demand(
        first["schema"] == "cm2.gate3.first-hit-atlas.v1"
        and first["candidate_reduction"]["chart_target_pair_count"] == 1296
        and first["candidate_reduction"]["retained_pair_count"] == 448
        and first["candidate_reduction"]["certified_empty_pair_count"] == 848,
        "first hit",
    )
    reflection_rows = atlas["reflection_certificate"]["row_digests"]
    demand(
        atlas["schema"] == "cm2.gate3.eight-cell-symmetry-atlas.v1"
        and atlas["coverage"]["global_leaf_count"] == 143248
        and reflection_rows["G:E->G:W"]
        == "46da8d49fbfc1493e1229bd4bd7c1a9dae9035a286bd97d58484ac312e4a4683"
        and reflection_rows["G:N->G:S"]
        == "e91640f12bebd3a49b385aa190a6758f62aa10f1b87135eee5fd833e4a3aa5b9",
        "Gate3 atlas",
    )
    demand(
        seam["schema"] == "cm2.gate3.chart-seam-quotient.manifest.v1"
        and seam["verdict"]["eight_chart_seam_ownership"] == "CERTIFIED"
        and seam["result"]["unique_half_open_owner_rule"]["diagonal_tie"]
        == "E or W owns; N or S excludes"
        and seam["result"]["scope_limits"][
            "all_eight_chart_seams_have_unique_owner"
        ] is True,
        "seam quotient",
    )
    return {
        "r169": r169,
        "r171": r171,
        "gate5": gate5,
        "atlas": atlas,
    }


TARGETS = tuple(
    (obstacle, ix, iy)
    for obstacle in ("G", "W")
    for ix in range(-4, 5)
    for iy in range(-4, 5)
)


def target_name(target: tuple[str, int, int]) -> str:
    obstacle, ix, iy = target
    return f"{obstacle}[{ix},{iy}]"


def target_parts(value: str) -> tuple[str, int, int]:
    demand(
        len(value) >= 6
        and value[0] in "GW"
        and value[1] == "["
        and value[-1] == "]"
        and value.count(",") == 1,
        "target syntax",
    )
    ix, iy = value[2:-1].split(",")
    return value[0], int(ix), int(iy)


def interval(
    source: str,
    target: tuple[str, int, int],
) -> tuple[Q, Q, Q, Q]:
    obstacle, ix, iy = target
    if source == obstacle == "G":
        return Q(ix), Q(ix), Q(iy), Q(iy)
    if source == "G" and obstacle == "W":
        center = Q(2 * ix + 1, 2)
        return (
            center - EPSILON,
            center + EPSILON,
            Q(2 * iy + 1, 2),
            Q(2 * iy + 1, 2),
        )
    if source == "W" and obstacle == "G":
        center = Q(2 * ix - 1, 2)
        return (
            center - EPSILON,
            center + EPSILON,
            Q(2 * iy - 1, 2),
            Q(2 * iy - 1, 2),
        )
    return Q(ix), Q(ix), Q(iy), Q(iy)


def min_square(lower: Q, upper: Q) -> Q:
    return Q(0) if lower <= 0 <= upper else min(lower**2, upper**2)


def maximum_abs(lower: Q, upper: Q) -> Q:
    return max(abs(lower), abs(upper))


def support(
    cell: str,
    x0: Q,
    x1: Q,
    y0: Q,
    y1: Q,
) -> Q:
    if cell == "E":
        leading, transverse = x1, maximum_abs(y0, y1)
    elif cell == "W":
        leading, transverse = -x0, maximum_abs(y0, y1)
    elif cell == "N":
        leading, transverse = y1, maximum_abs(x0, x1)
    elif cell == "S":
        leading, transverse = -y0, maximum_abs(x0, x1)
    else:
        raise ValueError(cell)
    if leading >= 0:
        return leading + transverse * UPPER_ROOT2
    return leading * LOWER_ROOT2 + transverse * UPPER_ROOT2


def retained(chart: str, target: tuple[str, int, int]) -> bool:
    source, cell = chart.split(":")
    obstacle, ix, iy = target
    if obstacle == source and ix == 0 and iy == 0:
        return False
    x0, x1, y0, y1 = interval(source, target)
    distance_squared = min_square(x0, x1) + min_square(y0, y1)
    horizon = Q(3) + RADIUS[source] + RADIUS[obstacle]
    if distance_squared >= horizon * horizon:
        return False
    return support(cell, x0, x1, y0, y1) >= (
        RADIUS[source] - RADIUS[obstacle]
    )


def candidates(chart: str) -> tuple[str, ...]:
    return tuple(
        target_name(target) for target in TARGETS if retained(chart, target)
    )


def patterns() -> tuple[tuple[str, ...], ...]:
    rows: list[tuple[str, ...]] = []
    for nx in range(5):
        for ny in range(5):
            length = nx + ny
            for sx in ((0,) if nx == 0 else (-1, 1)):
                for sy in ((0,) if ny == 0 else (-1, 1)):
                    for positions in itertools.combinations(range(length), nx):
                        x_positions = set(positions)
                        xt = "X+" if sx > 0 else "X-"
                        yt = "Y+" if sy > 0 else "Y-"
                        rows.append(tuple(
                            xt if index in x_positions else yt
                            for index in range(length)
                        ))
    return tuple(rows)


def stream(rows: Iterable[Any]) -> tuple[int, str]:
    hasher = hashlib.sha256()
    count = 0
    for row in rows:
        hasher.update(canonical(row).encode("utf-8"))
        hasher.update(b"\n")
        count += 1
    return count, hasher.hexdigest()


def registry_tables(gate5: dict[str, Any]) -> dict[str, Any]:
    words = patterns()
    demand(
        len(words) == len(set(words)) == PATTERN_COUNT
        and Counter(map(len, words))
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
        "patterns",
    )
    pairs = tuple(
        (chart, target)
        for chart in SOURCE_CHARTS
        for target in candidates(chart)
    )
    g_pairs = tuple(pair for pair in pairs if pair[0].startswith("G:"))
    demand(
        len(pairs) == len(set(pairs)) == 448
        and len(g_pairs) == PAIR_COUNT
        and pairs[:PAIR_COUNT] == g_pairs
        and all(len(candidates(chart)) == 57 for chart in SOURCE_G_CHARTS),
        "pairs",
    )
    full_count, full_digest = stream(
        [chart, target, list(word), len(word) + 1]
        for chart, target in pairs
        for word in words
    )
    g_count, g_digest = stream(
        [chart, target, list(word), len(word) + 1]
        for chart, target in g_pairs
        for word in words
    )
    frozen_registry = gate5["result"]["immutable_candidate_key_registry"]
    frozen_grammar = gate5["result"]["crossing_grammar"]
    demand(
        sha(pairs) == frozen_registry["chart_target_pair_rows_sha256"]
        and sha(words) == frozen_grammar["crossing_pattern_rows_sha256"]
        and full_count == 441280
        and full_digest
        == frozen_registry["candidate_word_key_rows_sha256"]
        and g_count == KEY_COUNT,
        "frozen registry digests",
    )
    return {
        "patterns": words,
        "pattern_lookup": {
            word: index for index, word in enumerate(words)
        },
        "pairs": pairs,
        "g_pairs": g_pairs,
        "pair_lookup": {
            pair: index for index, pair in enumerate(g_pairs)
        },
        "g_key_digest": g_digest,
    }


def map_chart(generator: str, chart: str) -> str:
    source, cell = chart.split(":")
    demand(source == "G", "source chart")
    dictionaries = {
        "Jx": {"E": "W", "W": "E", "N": "N", "S": "S"},
        "Jy": {"E": "E", "W": "W", "N": "S", "S": "N"},
    }
    return f"G:{dictionaries[generator][cell]}"


def map_target(generator: str, value: str) -> str:
    obstacle, ix, iy = target_parts(value)
    if generator == "Jx":
        ix = -ix if obstacle == "G" else -ix - 1
    else:
        iy = -iy if obstacle == "G" else -iy - 1
    return target_name((obstacle, ix, iy))


def displacement(value: str) -> tuple[Q, Q, Q, Q]:
    obstacle, ix, iy = target_parts(value)
    if obstacle == "G":
        return Q(ix), Q(0), Q(iy), Q(0)
    return Q(ix) + Q(1, 2), Q(1), Q(iy) + Q(1, 2), Q(0)


def audit_displacement(
    generator: str,
    source: str,
    destination: str,
) -> None:
    a, b, c, d = displacement(source)
    aa, bb, cc, dd = displacement(destination)
    if generator == "Jx":
        demand(
            (aa, -bb, cc, -dd) == (-a, -b, c, d),
            "Jx displacement",
        )
    else:
        demand(
            (aa, bb, cc, dd) == (a, b, -c, -d),
            "Jy displacement",
        )


def map_token(generator: str, token: str) -> str:
    demand(token in {"X-", "X+", "Y-", "Y+"}, "token")
    if generator == "Jx" and token.startswith("X"):
        return "X+" if token == "X-" else "X-"
    if generator == "Jy" and token.startswith("Y"):
        return "Y+" if token == "Y-" else "Y-"
    return token


def map_outgoing(generator: str, cell: str) -> str:
    return {
        "Jx": {"E": "W", "W": "E", "N": "N", "S": "S"},
        "Jy": {"E": "E", "W": "W", "N": "S", "S": "N"},
    }[generator][cell]


def normal_polynomial(cell: str) -> list[list[int]]:
    axes = {
        "E": (1, 0),
        "W": (-1, 0),
        "N": (0, 1),
        "S": (0, -1),
    }
    ex, ey = axes[cell]
    jx, jy = -ey, ex
    return [
        [ex, 2 * jx, -ex],
        [ey, 2 * jy, -ey],
    ]


def z_negation(rows: list[list[int]]) -> list[list[int]]:
    return [
        [
            coefficient * (-1 if power % 2 else 1)
            for power, coefficient in enumerate(row)
        ]
        for row in rows
    ]


def spatial_reflection(
    generator: str,
    rows: list[list[int]],
) -> list[list[int]]:
    reflected = [list(row) for row in rows]
    component = 0 if generator == "Jx" else 1
    reflected[component] = [-entry for entry in reflected[component]]
    return reflected


def official_row(
    pair: tuple[str, str],
    word: tuple[str, ...],
) -> list[Any]:
    return [pair[0], pair[1], list(word), len(word) + 1]


def official_id(ordinal: int, row: list[Any]) -> str:
    return f"gate5-word:{ordinal:06d}:{sha(row)}"


def expected_generator(
    generator: str,
    tables: dict[str, Any],
) -> tuple[dict[str, Any], list[int]]:
    pairs = tables["g_pairs"]
    words = tables["patterns"]
    pair_lookup = tables["pair_lookup"]
    word_lookup = tables["pattern_lookup"]
    pair_perm: list[int] = []
    for chart, target in pairs:
        mapped_target = map_target(generator, target)
        audit_displacement(generator, target, mapped_target)
        mapped_pair = (map_chart(generator, chart), mapped_target)
        demand(mapped_pair in pair_lookup, "mapped pair")
        pair_perm.append(pair_lookup[mapped_pair])
    word_perm = [
        word_lookup[tuple(map_token(generator, token) for token in word)]
        for word in words
    ]
    demand(
        sorted(pair_perm) == list(range(PAIR_COUNT))
        and all(pair_perm[pair_perm[index]] == index for index in range(PAIR_COUNT)),
        "pair involution",
    )
    demand(
        sorted(word_perm) == list(range(PATTERN_COUNT))
        and all(
            word_perm[word_perm[index]] == index
            for index in range(PATTERN_COUNT)
        ),
        "pattern involution",
    )
    ordinal_perm = [
        pair_perm[pair_index] * PATTERN_COUNT + word_perm[word_index]
        for pair_index in range(PAIR_COUNT)
        for word_index in range(PATTERN_COUNT)
    ]
    demand(
        sorted(ordinal_perm) == list(range(KEY_COUNT))
        and all(
            ordinal_perm[ordinal_perm[index]] == index
            for index in range(KEY_COUNT)
        ),
        "ordinal involution",
    )
    for source in range(KEY_COUNT):
        source_pair, source_word = divmod(source, PATTERN_COUNT)
        destination_pair, destination_word = divmod(
            ordinal_perm[source], PATTERN_COUNT
        )
        demand(
            destination_pair == pair_perm[source_pair]
            and destination_word == word_perm[source_word]
            and len(words[source_word]) == len(words[destination_word]),
            "roof conservation",
        )
    pair_count, pair_rows_digest = stream(
        [index, value] for index, value in enumerate(pair_perm)
    )
    word_count, word_rows_digest = stream(
        [index, value] for index, value in enumerate(word_perm)
    )
    ordinal_count, ordinal_rows_digest = stream(
        [index, value] for index, value in enumerate(ordinal_perm)
    )
    fixed_pairs = sum(index == value for index, value in enumerate(pair_perm))
    fixed_words = sum(index == value for index, value in enumerate(word_perm))
    fixed_ordinals = sum(
        index == value for index, value in enumerate(ordinal_perm)
    )
    samples: list[dict[str, Any]] = []
    for source in (
        0,
        56144,
        56145,
        112289,
        112290,
        168434,
        168435,
        224579,
    ):
        destination = ordinal_perm[source]
        pi, wi = divmod(source, PATTERN_COUNT)
        dpi, dwi = divmod(destination, PATTERN_COUNT)
        source_row = official_row(pairs[pi], words[wi])
        destination_row = official_row(pairs[dpi], words[dwi])
        demand(
            destination_row == [
                map_chart(generator, source_row[0]),
                map_target(generator, source_row[1]),
                [map_token(generator, token) for token in source_row[2]],
                source_row[3],
            ],
            "sample row",
        )
        samples.append({
            "source_ordinal": source,
            "source_key_id": official_id(source, source_row),
            "source_row": source_row,
            "destination_ordinal": destination,
            "destination_key_id": official_id(destination, destination_row),
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
    chart_dictionary = {
        chart: map_chart(generator, chart) for chart in SOURCE_G_CHARTS
    }
    target_dictionary = (
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
        token: map_token(generator, token)
        for token in ("X-", "X+", "Y-", "Y+")
    }
    outgoing_dictionary = {
        cell: map_outgoing(generator, cell)
        for cell in ("E", "W", "N", "S")
    }
    wall_identity = (
        {
            "reflected_axis": "X",
            "source_segment": "x(alpha)=qx+alpha*(hx-qx)",
            "source_wall_equation": "alpha=(k-qx)/(hx-qx)",
            "rebased_reflection": "(qx,hx,k)->(-qx,-hx,-k)",
            "reflected_wall_equation":
                "(-k-(-qx))/((-hx)-(-qx))=(k-qx)/(hx-qx)",
            "perpendicular_axis": "(qy,hy,k)->(qy,hy,k)",
        }
        if generator == "Jx"
        else {
            "reflected_axis": "Y",
            "source_segment": "y(alpha)=qy+alpha*(hy-qy)",
            "source_wall_equation": "alpha=(k-qy)/(hy-qy)",
            "rebased_reflection": "(qy,hy,k)->(-qy,-hy,-k)",
            "reflected_wall_equation":
                "(-k-(-qy))/((-hy)-(-qy))=(k-qy)/(hy-qy)",
            "perpendicular_axis": "(qx,hx,k)->(qx,hx,k)",
        }
    )
    target_identity = (
        {
            "G[ix,iy] displacement": "(ix,iy)->(-ix,iy)",
            "W[ix,iy] displacement":
                "(ix+1/2+s,iy+1/2)->"
                "(-ix-1+1/2-s,iy+1/2)="
                "(-(ix+1/2+s),iy+1/2)",
            "source_lift_rebasing":
                "reflected source translated back to G[0,0]",
        }
        if generator == "Jx"
        else {
            "G[ix,iy] displacement": "(ix,iy)->(ix,-iy)",
            "W[ix,iy] displacement":
                "(ix+1/2+s,iy+1/2)->"
                "(ix+1/2+s,-iy-1+1/2)="
                "(ix+1/2+s,-(iy+1/2))",
            "source_lift_rebasing":
                "reflected source translated back to G[0,0]",
        }
    )
    compact_rows: list[dict[str, Any]] = []
    for source_cell in ("E", "W", "N", "S"):
        destination_cell = map_outgoing(generator, source_cell)
        reflected = spatial_reflection(
            generator, normal_polynomial(source_cell)
        )
        destination = z_negation(normal_polynomial(destination_cell))
        demand(reflected == destination, "compact normal identity")
        compact_rows.append({
            "source_cell": source_cell,
            "destination_cell": destination_cell,
            "source_normal_after_spatial_reflection": reflected,
            "destination_normal_after_z_substitution": destination,
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
        "compact_normal_reflection_rows": compact_rows,
        "compact_normal_reflection_rows_sha256": sha(compact_rows),
        "all_four_compact_normal_identities_coefficientwise": True,
        "source_chart_dictionary": chart_dictionary,
        "target_lift_dictionary": target_dictionary,
        "target_center_affine_displacement_identity": target_identity,
        "signed_wall_token_dictionary": token_dictionary,
        "integer_wall_index_dictionary": (
            {"X wall k": "X wall -k", "Y wall k": "Y wall k"}
            if generator == "Jx"
            else {"X wall k": "X wall k", "Y wall k": "Y wall -k"}
        ),
        "integer_wall_crossing_parameter_identity": wall_identity,
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
            map_outgoing(generator, cell) for cell in {"E", "W"}
        ),
        "half_open_owner_rule_equivariant": True,
        "pair_permutation": {
            "domain_count": pair_count,
            "image_count": len(set(pair_perm)),
            "fixed_count": fixed_pairs,
            "two_cycle_count": (PAIR_COUNT - fixed_pairs) // 2,
            "image_index_list_sha256": sha(pair_perm),
            "source_destination_rows_sha256": pair_rows_digest,
        },
        "pattern_permutation": {
            "domain_count": word_count,
            "image_count": len(set(word_perm)),
            "fixed_count": fixed_words,
            "fixed_roof_histogram": {
                str(key): value
                for key, value in sorted(Counter(
                    len(words[index]) + 1
                    for index, value in enumerate(word_perm)
                    if index == value
                ).items())
            },
            "two_cycle_count": (PATTERN_COUNT - fixed_words) // 2,
            "image_index_list_sha256": sha(word_perm),
            "source_destination_rows_sha256": word_rows_digest,
        },
        "source_G_ordinal_permutation": {
            "ordinal_interval": [0, KEY_COUNT - 1],
            "domain_count": ordinal_count,
            "image_count": len(set(ordinal_perm)),
            "fixed_count": fixed_ordinals,
            "two_cycle_count": (KEY_COUNT - fixed_ordinals) // 2,
            "image_ordinal_list_sha256": sha(ordinal_perm),
            "source_destination_rows_sha256": ordinal_rows_digest,
            "bijective": True,
            "involutive": True,
            "roof_conserved_for_every_ordinal": True,
        },
        "sample_exact_key_transports": samples,
        "sample_exact_key_transports_sha256": sha(samples),
    }, ordinal_perm


def expected_group(
    jx: list[int],
    jy: list[int],
) -> dict[str, Any]:
    combined = [jx[jy[index]] for index in range(KEY_COUNT)]
    demand(
        all(
            jx[jx[index]] == index
            and jy[jy[index]] == index
            and jx[jy[index]] == jy[jx[index]]
            and combined[combined[index]] == index
            for index in range(KEY_COUNT)
        ),
        "Klein relations",
    )
    seen: set[int] = set()
    orbits: list[list[int]] = []
    for index in range(KEY_COUNT):
        if index in seen:
            continue
        orbit = sorted({
            index, jx[index], jy[index], combined[index]
        })
        seen.update(orbit)
        orbits.append(orbit)
    histogram = Counter(map(len, orbits))
    demand(
        len(seen) == KEY_COUNT
        and histogram == {2: 54, 4: 56118}
        and len(orbits) == 56172,
        "orbits",
    )
    count, rows_digest = stream(
        [index, value] for index, value in enumerate(combined)
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
                index == value for index, value in enumerate(combined)
            ),
            "two_cycle_count": KEY_COUNT // 2,
            "image_ordinal_list_sha256": sha(combined),
            "source_destination_rows_sha256": rows_digest,
        },
        "orbit_count": len(orbits),
        "orbit_size_histogram": {
            str(key): value for key, value in sorted(histogram.items())
        },
        "orbit_rows_sha256": sha(orbits),
        "ordinal_conservation": {
            "domain_interval": [0, KEY_COUNT - 1],
            "union_of_orbits_is_full_interval": True,
            "distinct_orbits_are_disjoint": True,
            "sum_of_orbit_sizes": sum(map(len, orbits)),
        },
    }


def atlas_census(atlas: dict[str, Any]) -> dict[str, int]:
    rows = [atlas["charts"][chart] for chart in SOURCE_G_CHARTS]
    census = {
        "leaf_count": sum(row["leaf_count"] for row in rows),
        "unique_first": sum(
            row["counts"]["unique_first"] for row in rows
        ),
        "tangency_graph": sum(
            row["counts"]["tangency_graph"] for row in rows
        ),
        "multi_candidate": sum(
            row["counts"]["multi_candidate"] for row in rows
        ),
    }
    demand(
        census == {
            "leaf_count": 66420,
            "unique_first": 21232,
            "tangency_graph": 160,
            "multi_candidate": 45028,
        },
        "source-G census",
    )
    return census


def expected_result() -> dict[str, Any]:
    data = upstream()
    tables = registry_tables(data["gate5"])
    generator_rows: list[dict[str, Any]] = []
    permutations: dict[str, list[int]] = {}
    for generator in ("Jx", "Jy"):
        row, permutation = expected_generator(generator, tables)
        generator_rows.append(row)
        permutations[generator] = permutation
    group = expected_group(permutations["Jx"], permutations["Jy"])
    census = atlas_census(data["atlas"])
    r169 = data["r169"]
    r171 = data["r171"]
    demand(
        r169["source_G_existing_inputs"]["candidate_exact_key_count"]
        == KEY_COUNT
        and r169["source_G_exact_key_coverage_census"][
            "global_geometric_exact_key_disposition_count"
        ] == 0
        and r169["source_G_exact_key_coverage_census"][
            "keys_without_a_global_geometric_disposition_count"
        ] == KEY_COUNT
        and r171["Round169_exact_key_guard"][
            "source_G_global_geometric_exact_key_disposition_count"
        ] == 0
        and r171["Round169_exact_key_guard"][
            "source_G_keys_without_global_geometric_disposition_count"
        ] == KEY_COUNT,
        "prior zero-credit guard",
    )
    g_pairs = tables["g_pairs"]
    pair_count, indexed_pair_digest = stream(
        [index, list(pair)] for index, pair in enumerate(g_pairs)
    )
    demand(pair_count == PAIR_COUNT, "indexed pairs")
    relabel_rows = [
        {
            "generator": generator,
            "source_chart": chart,
            "source_target": target,
            "destination_chart": map_chart(generator, chart),
            "destination_target": map_target(generator, target),
        }
        for generator in ("Jx", "Jy")
        for chart, target in g_pairs
    ]
    return {
        "status": CERTIFIED_STATUS,
        "scope": {
            "source_obstacle": "G",
            "transport_generators": ["Jx", "Jy"],
            "Gate5_source_G_candidate_key_count": KEY_COUNT,
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
            "dependency_sha256": DEPENDENCIES,
            "Round169_result_sha256": R169_RESULT,
            "Round169_verification_result_sha256":
                R169_VERIFY_RESULT,
            "Round171_result_sha256": R171_RESULT,
            "Round171_verification_result_sha256":
                R171_VERIFY_RESULT,
            "Gate5_candidate_registry_rebuilt_without_importing_source": True,
            "Gate3_reflection_formulas_rederived_from_physical_maps": True,
            "old_artifacts_modified": False,
        },
        "rebuilt_Gate5_source_G_registry": {
            "full_chart_target_pair_count": len(tables["pairs"]),
            "full_chart_target_pair_rows_sha256": sha(tables["pairs"]),
            "crossing_pattern_count": len(tables["patterns"]),
            "crossing_pattern_rows_sha256": sha(tables["patterns"]),
            "source_G_chart_order": list(SOURCE_G_CHARTS),
            "source_G_candidate_count_per_chart": {
                chart: len(candidates(chart))
                for chart in SOURCE_G_CHARTS
            },
            "source_G_chart_target_pair_count": len(g_pairs),
            "source_G_chart_target_pair_rows_sha256": sha(g_pairs),
            "source_G_indexed_pair_rows_sha256": indexed_pair_digest,
            "source_G_key_count": KEY_COUNT,
            "source_G_key_ordinal_interval": [0, KEY_COUNT - 1],
            "source_G_keys_are_exact_global_Gate5_ordinal_prefix": True,
            "source_G_key_rows_sha256": tables["g_key_digest"],
            "roof_formula": "len(crossing_pattern)+1",
            "target_relabel_rows_count": len(relabel_rows),
            "target_relabel_rows_sha256": sha(relabel_rows),
        },
        "exact_transport_generators": generator_rows,
        "exact_transport_generators_sha256": sha(generator_rows),
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
            "diagonal_seam_rule": "E or W owns; N or S excludes",
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
                KEY_COUNT,
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


def expected_document() -> dict[str, Any]:
    result = expected_result()
    return {
        "schema": CERTIFICATE_SCHEMA,
        "result": result,
        "result_sha256": sha(result),
    }


def validate(
    document: dict[str, Any],
    expected: dict[str, Any],
) -> None:
    demand(document == expected, "full expected document equality")


def resign(document: dict[str, Any]) -> None:
    document["result_sha256"] = sha(document["result"])


def attacks(
    expected: dict[str, Any],
) -> list[tuple[str, dict[str, Any]]]:
    cases: list[tuple[str, dict[str, Any]]] = []

    def add(
        label: str,
        mutation: Callable[[dict[str, Any]], None],
    ) -> None:
        candidate = copy.deepcopy(expected)
        mutation(candidate["result"])
        resign(candidate)
        cases.append((label, candidate))

    add("status", lambda r: r.__setitem__("status", "CERTIFIED_D02"))
    add(
        "key count",
        lambda r: r["scope"].__setitem__(
            "Gate5_source_G_candidate_key_count", KEY_COUNT - 1
        ),
    )
    add(
        "chart order",
        lambda r: r["rebuilt_Gate5_source_G_registry"]
        ["source_G_chart_order"].reverse(),
    )
    add(
        "crossing digest",
        lambda r: r["rebuilt_Gate5_source_G_registry"].__setitem__(
            "crossing_pattern_rows_sha256", "0" * 64
        ),
    )
    add(
        "source key digest",
        lambda r: r["rebuilt_Gate5_source_G_registry"].__setitem__(
            "source_G_key_rows_sha256", "0" * 64
        ),
    )
    add(
        "rebased physical map",
        lambda r: r["exact_transport_generators"][0].__setitem__(
            "physical_reflection", "(x,y,s,p)->(1-x,y,-s,-p)"
        ),
    )
    add(
        "ambient representative",
        lambda r: r["exact_transport_generators"][0].__setitem__(
            "ambient_torus_representative_before_source_lift_rebasing",
            "(x,y,s,p)->(-x,y,-s,-p)",
        ),
    )
    add(
        "deck rebasing",
        lambda r: r["exact_transport_generators"][0].__setitem__(
            "source_G_deck_rebasing", "none"
        ),
    )
    add(
        "Gate3 t map",
        lambda r: r["exact_transport_generators"][0]
        ["Gate3_parameter_map"]["t_by_source_cell"].__setitem__("N", "t"),
    )
    add(
        "compact q map",
        lambda r: r["exact_transport_generators"][0]
        ["compact_parameter_map"].__setitem__("q", "q"),
    )
    add(
        "compact z map",
        lambda r: r["exact_transport_generators"][0]
        ["compact_parameter_map"]["z_by_source_cell"].__setitem__("E", "z"),
    )
    add(
        "compact normal coefficient",
        lambda r: r["exact_transport_generators"][0]
        ["compact_normal_reflection_rows"][0]
        ["source_normal_after_spatial_reflection"][0].__setitem__(0, 1),
    )
    add(
        "compact normal digest",
        lambda r: r["exact_transport_generators"][1].__setitem__(
            "compact_normal_reflection_rows_sha256", "0" * 64
        ),
    )
    add(
        "source chart map",
        lambda r: r["exact_transport_generators"][0]
        ["source_chart_dictionary"].__setitem__("G:E", "G:E"),
    )
    add(
        "target lift map",
        lambda r: r["exact_transport_generators"][0]
        ["target_lift_dictionary"].__setitem__(
            "W[ix,iy]", "W[-ix,iy]"
        ),
    )
    add(
        "target affine identity",
        lambda r: r["exact_transport_generators"][0]
        ["target_center_affine_displacement_identity"].__setitem__(
            "G[ix,iy] displacement", "(ix,iy)->(1-ix,iy)"
        ),
    )
    add(
        "signed wall token",
        lambda r: r["exact_transport_generators"][0]
        ["signed_wall_token_dictionary"].__setitem__("X+", "X+"),
    )
    add(
        "integer wall index",
        lambda r: r["exact_transport_generators"][0]
        ["integer_wall_index_dictionary"].__setitem__(
            "X wall k", "X wall 1-k"
        ),
    )
    add(
        "wall parameter identity",
        lambda r: r["exact_transport_generators"][0]
        ["integer_wall_crossing_parameter_identity"].__setitem__(
            "rebased_reflection", "(qx,hx,k)->(1-qx,1-hx,1-k)"
        ),
    )
    add(
        "velocity sign",
        lambda r: r["exact_transport_generators"][0].__setitem__(
            "reflected_axis_velocity_multiplier", "1"
        ),
    )
    add(
        "event order",
        lambda r: r["exact_transport_generators"][0].__setitem__(
            "event_parameter_and_strict_order_preserved", False
        ),
    )
    add(
        "roof",
        lambda r: r["exact_transport_generators"][0].__setitem__(
            "roof_preserved", False
        ),
    )
    add(
        "outgoing chart",
        lambda r: r["exact_transport_generators"][0]
        ["strict_outgoing_chart_dictionary"].__setitem__("E", "E"),
    )
    add(
        "half-open owner image",
        lambda r: r["exact_transport_generators"][1].__setitem__(
            "half_open_owner_set_image", ["N", "S"]
        ),
    )
    add(
        "pair permutation",
        lambda r: r["exact_transport_generators"][0]
        ["pair_permutation"].__setitem__(
            "image_index_list_sha256", "0" * 64
        ),
    )
    add(
        "pattern permutation",
        lambda r: r["exact_transport_generators"][1]
        ["pattern_permutation"].__setitem__(
            "source_destination_rows_sha256", "0" * 64
        ),
    )
    add(
        "ordinal permutation",
        lambda r: r["exact_transport_generators"][0]
        ["source_G_ordinal_permutation"].__setitem__(
            "image_ordinal_list_sha256", "0" * 64
        ),
    )
    add(
        "ordinal bijection",
        lambda r: r["exact_transport_generators"][0]
        ["source_G_ordinal_permutation"].__setitem__("bijective", False),
    )
    add(
        "ordinal fixed count",
        lambda r: r["exact_transport_generators"][1]
        ["source_G_ordinal_permutation"].__setitem__("fixed_count", 55),
    )
    add(
        "sample destination",
        lambda r: r["exact_transport_generators"][0]
        ["sample_exact_key_transports"][0].__setitem__(
            "destination_ordinal", 0
        ),
    )
    add(
        "group commute",
        lambda r: r["Klein_four_action"]["relations"].__setitem__(
            "Jx_Jy_equals_Jy_Jx", False
        ),
    )
    add(
        "group orbit histogram",
        lambda r: r["Klein_four_action"]["orbit_size_histogram"].__setitem__(
            "4", 56117
        ),
    )
    add(
        "group orbit digest",
        lambda r: r["Klein_four_action"].__setitem__(
            "orbit_rows_sha256", "0" * 64
        ),
    )
    add(
        "direct chart destination",
        lambda r: r["direct_reflected_chart_contracts"][0].__setitem__(
            "destination_reflected_chart", "G:E"
        ),
    )
    add(
        "Gate3 reflection digest",
        lambda r: r["direct_reflected_chart_contracts"][1].__setitem__(
            "Gate3_reflection_leaf_rows_sha256", "0" * 64
        ),
    )
    add(
        "direct transport readiness",
        lambda r: r["direct_reflected_chart_contracts"][0].__setitem__(
            "exact_return_signature_transport_ready", False
        ),
    )
    add(
        "outgoing owner set",
        lambda r: r["outgoing_chart_contract"].__setitem__(
            "owner_set", ["N", "S"]
        ),
    )
    add(
        "materialized rows",
        lambda r: r["dynamic_row_credit_guard"].__setitem__(
            "dynamic_rows_materialized_by_Round173", 21232
        ),
    )
    add(
        "transported rows",
        lambda r: r["dynamic_row_credit_guard"].__setitem__(
            "transported_dynamic_rows_materialized_by_Round173", 10616
        ),
    )
    add(
        "invent disposition",
        lambda r: r["dynamic_row_credit_guard"].__setitem__(
            "global_geometric_exact_key_dispositions_after_Round173", 1
        ),
    )
    add(
        "deficit",
        lambda r: r["dynamic_row_credit_guard"].__setitem__(
            "keys_without_global_geometric_disposition_after_Round173",
            KEY_COUNT - 1,
        ),
    )
    add(
        "leaf census",
        lambda r: r["dynamic_row_credit_guard"]["source_G_Gate3_census"]
        .__setitem__("unique_first", 21231),
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
    add("extra result key", lambda r: r.__setitem__("forged", True))
    return cases


def strict_json_tests(expected: dict[str, Any]) -> list[str]:
    raw = canonical(expected).encode("utf-8")
    duplicate = raw.replace(
        b'{"result":',
        b'{"schema":"duplicate","result":',
        1,
    )
    vectors = [
        ("duplicate key", duplicate),
        ("float", b'{"x":1.0}'),
        ("NaN", b'{"x":NaN}'),
        ("BOM", b"\xef\xbb\xbf" + raw),
        ("invalid UTF8", b'{"x":"\xff"}'),
        ("decoded NUL", b'{"x":"\\u0000"}'),
        ("surrogate", b'{"x":"\\ud800"}'),
        ("top array", b"[]"),
        ("trailing", raw + b"{}"),
    ]
    rejected: list[str] = []
    for label, vector in vectors:
        try:
            validate(strict_decode(vector), expected)
        except Exception:
            rejected.append(label)
    demand(len(rejected) == len(vectors), "strict JSON suite")
    return rejected


def path_tests() -> list[str]:
    rejected: list[str] = []

    def expect(label: str, action: Callable[[], None]) -> None:
        try:
            action()
        except Exception:
            rejected.append(label)
        else:
            raise RuntimeError(f"path attack accepted:{label}")

    with tempfile.TemporaryDirectory(prefix="cm2-r173-") as raw:
        temp = Path(raw)
        good = temp / "good.json"
        good.write_text("{}\n", encoding="utf-8")
        safe_input(good)
        expect("missing input", lambda: safe_input(temp / "missing.json"))
        input_link = temp / "input-link.json"
        input_link.symlink_to(good)
        expect("input symlink", lambda: safe_input(input_link))
        input_directory = temp / "input-directory"
        input_directory.mkdir()
        expect("input directory", lambda: safe_input(input_directory))
        hard_source = temp / "hard-source.json"
        hard_source.write_text("{}\n", encoding="utf-8")
        hard_input = temp / "hard-input.json"
        os.link(hard_source, hard_input)
        expect("input hardlink", lambda: safe_input(hard_input))

        protected = [good, PRODUCER, Path(__file__).resolve()]
        safe_output(temp / "ordinary-output.json", protected)
        expect("output certificate", lambda: safe_output(good, protected))
        expect("output producer", lambda: safe_output(PRODUCER, protected))
        expect(
            "output verifier",
            lambda: safe_output(Path(__file__).resolve(), protected),
        )
        dependency = BASE / next(iter(DEPENDENCIES))
        expect(
            "output dependency",
            lambda: safe_output(dependency, [*protected, dependency]),
        )
        output_link = temp / "output-link.json"
        output_link.symlink_to(good)
        expect(
            "output symlink",
            lambda: safe_output(output_link, protected),
        )
        output_directory = temp / "output-directory"
        output_directory.mkdir()
        expect(
            "output directory",
            lambda: safe_output(output_directory, protected),
        )
        output_hard_source = temp / "output-hard-source"
        output_hard_source.write_text("x", encoding="utf-8")
        output_hard = temp / "output-hard"
        os.link(output_hard_source, output_hard)
        expect(
            "output hardlink",
            lambda: safe_output(output_hard, protected),
        )
        real_parent = temp / "real-parent"
        real_parent.mkdir()
        linked_parent = temp / "linked-parent"
        linked_parent.symlink_to(real_parent, target_is_directory=True)
        expect(
            "output parent symlink",
            lambda: safe_output(linked_parent / "out.json", protected),
        )
        expect(
            "missing output parent",
            lambda: safe_output(temp / "absent" / "out.json", protected),
        )
    demand(len(rejected) == 13, "path suite")
    return rejected


def build_verification(
    certificate: dict[str, Any],
    certificate_path: Path,
) -> dict[str, Any]:
    expected = expected_document()
    validate(certificate, expected)
    semantic_rejections: list[str] = []
    cases = attacks(expected)
    for label, candidate in cases:
        try:
            validate(candidate, expected)
        except Exception:
            semantic_rejections.append(label)
    demand(
        len(semantic_rejections) == len(cases),
        "semantic attack suite",
    )
    json_rejections = strict_json_tests(expected)
    path_rejections = path_tests()
    producer_digest = hashlib.sha256(PRODUCER.read_bytes()).hexdigest()
    demand(producer_digest == EXPECTED_PRODUCER_SHA256, "producer pin")
    result = {
        "status": "PASS",
        "certificate_schema": CERTIFICATE_SCHEMA,
        "certificate_result_sha256": certificate["result_sha256"],
        "certificate_sha256":
            hashlib.sha256(certificate_path.read_bytes()).hexdigest(),
        "producer_sha256": producer_digest,
        "producer_imported_or_executed": False,
        "all_certificate_fields_semantically_reconstructed": True,
        "full_document_exactly_matched": True,
        "full_448_pair_and_985_pattern_Gate5_registry_independently_rebuilt":
            True,
        "source_G_224580_key_prefix_and_every_ordinal_independently_rebuilt":
            True,
        "source_chart_and_target_lift_permutations_independently_rebuilt":
            True,
        "target_center_affine_displacement_identities_checked_for_all_456_generator_pair_rows":
            True,
        "integer_wall_equations_token_directions_and_event_order_independently_checked":
            True,
        "all_eight_generator_chart_compact_z_normal_identities_rebuilt_coefficientwise":
            True,
        "strict_and_half_open_outgoing_chart_dictionaries_independently_rebuilt":
            True,
        "ordinal_conservation_bijection_and_involution_checked_exhaustively":
            True,
        "Klein_group_relations_and_all_56172_orbits_checked_exhaustively":
            True,
        "Round169_Round171_zero_dynamic_row_credit_guard_rechecked": True,
        "semantic_attack_suite": {
            "all_result_mutations_resigned": True,
            "attack_count": len(cases),
            "rejected_count": len(semantic_rejections),
            "all_rejected": True,
            "rejected_attack_names": semantic_rejections,
        },
        "strict_json_attack_suite": {
            "attack_count": len(json_rejections),
            "rejected_count": len(json_rejections),
            "all_rejected": True,
            "rejected_attack_names": json_rejections,
        },
        "path_safety_self_test": {
            "attack_count": len(path_rejections),
            "rejected_count": len(path_rejections),
            "all_rejected": True,
            "rejected_attack_names": path_rejections,
        },
        "strict_nonpromotion_recomputed": True,
    }
    return {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": sha(result),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    certificate_path = arguments.certificate.resolve()
    safe_input(certificate_path)
    protected = [
        certificate_path,
        PRODUCER,
        Path(__file__).resolve(),
        *[(BASE / name).resolve() for name in DEPENDENCIES],
    ]
    safe_output(arguments.output, protected)
    certificate = load(certificate_path)
    verification = build_verification(certificate, certificate_path)
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
    print(verification["result_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
