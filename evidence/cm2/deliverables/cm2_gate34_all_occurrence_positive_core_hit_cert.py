#!/usr/bin/env python3
"""Positive all-scale core-hit cylinders for every maximal occurrence.

The frozen two-occurrence charge is imported unchanged.  For each of the
remaining 62 occurrences, a deterministic binary64 pilot proposes one finite
collision word only.  The proposal has no certification status.  Both actual
parameter sides, every scale down to zero, every proposed collision, collision
uniqueness, and the terminal strict core interior are then independently
validated with 2048-bit Arb on an explicit positive source-parameter cylinder.

This certifies one positive core-hit cylinder for all 64 maximal occurrences
and all 128 oriented hit/miss branches.  It does not certify that the displayed
word realizes the first core stopping time, a normalized physical hit fraction,
post-core native dwell, a cemetery tail, or a common strong-space operator.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_positive_core_hit_charge_cert as frozen_charge
import cm2_gate3_global_borel_current_assembly_cert as current
import cm2_gate3_global_physical_subrow_atlas_cert as bulk


Q = Fraction
HERE = Path(__file__).resolve().parent
PRECISION_BITS = 2048
TARGET_PATTERN = re.compile(r"([GW])\[(-?\d+),(-?\d+)\]")
FLOAT_RADIUS = {"G": 0.36, "W": 0.16}

DEPENDENCIES = {
    "cm2-gate34-positive-core-hit-charge-manifest-2026-07-17.json": (
        "961ba5598e0737bc70a4f1cc86f7ccec31ab40d6d2ec028f3b11d2d473165d37"
    ),
    "cm2_gate34_positive_core_hit_charge_cert.py": (
        "922a417d06b7456b4349edf98d22d56d56df1045f6415b05bc0e5f0a4d5b2bdf"
    ),
    "cm2_gate3_global_borel_current_assembly_cert.py": (
        "bf7e9f77063a0d390f8a0337e1591be368ffbc4d2588e9e4fb5c7cbc18859d1b"
    ),
    "cm2_gate3_global_physical_subrow_atlas_cert.py": (
        "0445331455e5cc8d17c3393108e997712502cdb606f65ac57de6e0b698b3c1fc"
    ),
    "cm2-gate25-physical-return-core-registry-manifest-2026-07-16.json": (
        "144f5516ada8b83ca07459582c8cdb07ba09db11ac18a90cff32c6396c6e5a42"
    ),
    "cm2_gate25_physical_return_core_registry_cert.py": (
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb"
    ),
}


NEW_CHARGES = {
    "occ:041e08f7fb169193ca325202": ("G:S", "-2195511682316429/3774388787961921", 2, 80),
    "occ:05ae74f819dc57437881d3ad": ("W:N", "-1848838384371751/2251799813685248", 8, 120),
    "occ:10c2d5afd1cb5e81ffaa29d5": ("G:S", "-209190427418650/1146879586706717", 7, 120),
    "occ:16f866d7f3c505db23c60ce4": ("W:S", "1836526518071135/4021862424955143", 2, 80),
    "occ:18c3ae46502e9b47aa0e030b": ("W:W", "-2289925361497637/4503599627370496", 3, 80),
    "occ:18d2df4a9ad015e30680f2e6": ("W:W", "2289925361497637/4503599627370496", 3, 80),
    "occ:1fd4fb2ba132721b62fe2253": ("G:E", "1164717968971412/2007030524672901", 4, 100),
    "occ:21af5bd490573b8ae8d00d65": ("G:W", "-863762936042868/906326211364939", 2, 80),
    "occ:29a27eee866a3629c2f8497d": ("W:N", "2290038156610217/4503599627370496", 3, 80),
    "occ:3187c5ee1ea12020ca96ed0f": ("G:S", "7596769600478/13059899537643", 2, 80),
    "occ:32c4e41cca29b03c6fb9f033": ("G:E", "-1127307244510214/1182857079561567", 2, 80),
    "occ:37a7fbf85a5bc7047a9892cb": ("W:N", "654963698615636/1434323906163081", 2, 80),
    "occ:390e29a2a7ca627db0759c41": ("G:W", "-4501663475254507/4503599627370496", 16, 180),
    "occ:3f79242e66eae2ab0e5f2822": ("G:W", "-1309841957180431/2251799813685248", 2, 80),
    "occ:4025f53da9ff94a07e12de8f": ("G:W", "-653381120337751/1125899906842624", 4, 100),
    "occ:4301d52490c9d21b2bb39cc4": ("W:E", "197714557960804/432980816614799", 2, 80),
    "occ:478c4c7483e360f6dc3d67c2": ("G:N", "2613524481351001/4503599627370496", 4, 100),
    "occ:4abe194b661dcb43a6b7eb2a": ("G:S", "-1566576746554699/3094083409356989", 9, 120),
    "occ:4bbaa658a8bc28db9d812675": ("W:E", "-572481340374409/1125899906842624", 3, 80),
    "occ:4c3b6428514fb4381623f134": ("W:S", "-358393713499264/704818734093233", 3, 80),
    "occ:4f9ea40f0786791974e45f69": ("G:S", "410727482593613/2251799813685248", 7, 120),
    "occ:535d4dafa3d7af500a377541": ("G:S", "-1127307244510214/1182857079561567", 2, 80),
    "occ:54ca080e1156c32e6a8fa436": ("G:W", "4501663475254507/4503599627370496", 16, 180),
    "occ:56911d21749b02e02d2efa11": ("G:S", "-1927176795391720/2030179142883903", 3, 80),
    "occ:59c1d29788b311d01d4a27e3": ("W:S", "2290038156610217/4503599627370496", 3, 80),
    "occ:5aed1f966c6be5e90f841a12": ("G:N", "-1927176795391720/2030179142883903", 3, 80),
    "occ:6b2541c3e60d8546cb839f91": ("W:S", "1766990784520453/2152113214978911", 8, 120),
    "occ:701fd46d650ebdb6b9a93cde": ("W:S", "-1848838384371751/2251799813685248", 8, 120),
    "occ:7345faf25a39088ab10c82a9": ("G:N", "410727482593613/2251799813685248", 7, 120),
    "occ:7604734fe531ae72afa5461e": ("G:N", "-1566576746554699/3094083409356989", 9, 120),
    "occ:76c36c8217ab522d4312f314": ("G:W", "-791428844681279/2251799813685248", 7, 120),
    "occ:77dfc0dfc59f5309cfda30ce": ("G:N", "3565378070061739/4503599627370496", 19, 200),
    "occ:84cd7d0ee1c6252837c6bd72": ("G:N", "-1127307244510214/1182857079561567", 2, 80),
    "occ:875e628e2ac057ae62922f6b": ("W:N", "1766990784520453/2152113214978911", 8, 120),
    "occ:8909baf356fd5ea238a1f7c9": ("G:W", "1309841957180431/2251799813685248", 2, 80),
    "occ:8a093a396a0c6955a2460bca": ("W:W", "629327767908471/1378183041642274", 2, 80),
    "occ:9185b00a40dfeaf14a360e47": ("G:S", "-2613524481351003/4503599627370496", 4, 100),
    "occ:974a743fd1817bb7942fa846": ("G:S", "2613524481351001/4503599627370496", 4, 100),
    "occ:9b954aa706ac597da3c3e23c": ("W:N", "-358393713499264/704818734093233", 3, 80),
    "occ:9c5df5ed7748e1366f74f5c4": ("G:N", "1127307244510214/1182857079561567", 2, 80),
    "occ:a744ef838795b489595bd746": ("G:W", "791428844681279/2251799813685248", 7, 120),
    "occ:a9b7d86e27c6ecfb800ae7f6": ("G:N", "-209190427418650/1146879586706717", 7, 120),
    "occ:aa60b008ce87edadc6f99342": ("W:N", "-629327767908471/1378183041642274", 2, 80),
    "occ:aa9dccf1a23952c4f550b0d2": ("G:N", "7596769600478/13059899537643", 2, 80),
    "occ:ae0b59086aba8cd47821da1a": ("G:E", "2619683914360863/4503599627370496", 2, 80),
    "occ:b6059b5fe567ac156e363c4d": ("W:E", "572481340374409/1125899906842624", 3, 80),
    "occ:ba9f8bc0b6f4ed215f94feda": ("G:E", "-1024485914576945/2914901582209281", 7, 120),
    "occ:bb57302b485b353f5feb59b2": ("G:S", "3565378070061739/4503599627370496", 19, 200),
    "occ:bbf4f4de092e2481f78d4576": ("G:E", "-3565378070061739/4503599627370496", 19, 200),
    "occ:c0da5dcc90790b01fb21761f": ("G:E", "3565378070061739/4503599627370496", 19, 200),
    "occ:c609ca4c729e401981e944a0": ("G:N", "1140117042529445/2251799813685248", 9, 120),
    "occ:cdfad4c0ed800ea5e54a413a": ("W:E", "-1041317916041572/2280412157271109", 2, 80),
    "occ:d0d4f94a56472898c1d33a79": ("G:E", "-2195511682316429/3774388787961921", 2, 80),
    "occ:d30b72f53d34b0762308a847": ("G:W", "1557633001144714/1634387813735071", 2, 80),
    "occ:d7cb3385faad6e91015d007b": ("G:N", "-1164717968971412/2007030524672901", 4, 100),
    "occ:e00f9b3f2c1f0fc230a892d4": ("G:S", "1127307244510214/1182857079561567", 2, 80),
    "occ:e109ba54d752937d651fff22": ("G:N", "-2195511682316429/3774388787961921", 2, 80),
    "occ:e3836a89c9c3f326b39e0719": ("G:W", "326690560168875/562949953421312", 4, 100),
    "occ:eac71d13a4c9f2b20de38f26": ("G:S", "1140117042529445/2251799813685248", 9, 120),
    "occ:f2273c4a422b917a87e2e71a": ("G:E", "1127307244510214/1182857079561567", 2, 80),
    "occ:f2b7d26da59da0076fd2e89d": ("G:E", "1024485914576945/2914901582209281", 7, 120),
    "occ:f41b98a1b206257c176e9fd5": ("G:E", "-1164717968971412/2007030524672901", 4, 100),
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_target(target_id: str) -> tuple[str, int, int]:
    match = TARGET_PATTERN.fullmatch(target_id)
    assert match is not None
    return match.group(1), int(match.group(2)), int(match.group(3))


def target_center_float(target_id: str) -> tuple[float, float]:
    obstacle, ix, iy = parse_target(target_id)
    return ix + (0.5 if obstacle == "W" else 0.0), iy + (0.5 if obstacle == "W" else 0.0)


def source_normal_float(chart_id: str, z_text: str) -> tuple[float, float]:
    _source, cell = chart_id.split(":")
    coordinate = float(Q(z_text)) / math.sqrt(2.0)
    radical = math.sqrt(1.0 - coordinate * coordinate)
    if cell == "E":
        return radical, coordinate
    if cell == "W":
        return -radical, coordinate
    if cell == "N":
        return coordinate, radical
    assert cell == "S"
    return coordinate, -radical


def collide_float(
    qx: float, qy: float, ux: float, uy: float, target_id: str,
) -> tuple[float, float, float, float, float, float, float]:
    obstacle, _ix, _iy = parse_target(target_id)
    ax, ay = target_center_float(target_id)
    radius = FLOAT_RADIUS[obstacle]
    dx, dy = ax - qx, ay - qy
    ell = ux * dx + uy * dy
    cross = -uy * dx + ux * dy
    discriminant = radius * radius - cross * cross
    assert discriminant > 0.0
    radical = math.sqrt(discriminant)
    root = ell - radical
    assert 1.0e-10 < root < 2.0
    normal_x = (-radical * ux + cross * uy) / radius
    normal_y = (-radical * uy - cross * ux) / radius
    contact_x = ax + radius * normal_x
    contact_y = ay + radius * normal_y
    outgoing_x = (
        (1.0 - 2.0 * discriminant / (radius * radius)) * ux
        + 2.0 * radical * cross / (radius * radius) * uy
    )
    outgoing_y = (
        (1.0 - 2.0 * discriminant / (radius * radius)) * uy
        - 2.0 * radical * cross / (radius * radius) * ux
    )
    return contact_x, contact_y, outgoing_x, outgoing_y, normal_x, normal_y, root


def candidate_ids_around(current_id: str, radius: int = 4) -> Iterable[str]:
    _obstacle, ix0, iy0 = parse_target(current_id)
    for obstacle in ("G", "W"):
        for ix in range(ix0 - radius, ix0 + radius + 1):
            for iy in range(iy0 - radius, iy0 + radius + 1):
                target_id = f"{obstacle}[{ix},{iy}]"
                if target_id != current_id:
                    yield target_id


def nearest_float(
    qx: float, qy: float, ux: float, uy: float, current_id: str,
) -> tuple[str, tuple[float, float, float, float, float, float, float]]:
    candidates = []
    for target_id in candidate_ids_around(current_id):
        obstacle, _ix, _iy = parse_target(target_id)
        ax, ay = target_center_float(target_id)
        radius = FLOAT_RADIUS[obstacle]
        dx, dy = ax - qx, ay - qy
        ell = ux * dx + uy * dy
        cross = -uy * dx + ux * dy
        discriminant = radius * radius - cross * cross
        if ell <= 0.0 or discriminant <= 0.0:
            continue
        root = ell - math.sqrt(discriminant)
        if 1.0e-10 < root < 2.0:
            candidates.append((root, target_id))
    candidates.sort()
    assert candidates
    target_id = candidates[0][1]
    return target_id, collide_float(qx, qy, ux, uy, target_id)


def core_payload(core: Any) -> dict[str, Any]:
    return {
        "chart_id": core.chart_id,
        "t": [str(core.t0), str(core.t1)],
        "p": [str(core.p0), str(core.p1)],
        "target_id": core.target_id,
        "crossings": list(core.crossings),
    }


def core_id(core: Any) -> str:
    return "core:" + canonical_digest(core_payload(core))


def detect_core_float(
    target_id: str, normal_x: float, normal_y: float, ux: float, uy: float,
) -> tuple[str, str] | None:
    source = target_id[0]
    if abs(normal_x) >= abs(normal_y):
        cell = "E" if normal_x >= 0.0 else "W"
        t = normal_y
    else:
        cell = "N" if normal_y >= 0.0 else "S"
        t = normal_x
    p = -ux * normal_y + uy * normal_x
    chart_id = f"{source}:{cell}"
    matches = [
        core for core in core_cert.physical_cores()
        if core.chart_id == chart_id
        and float(core.t0) < t < float(core.t1)
        and float(core.p0) < p < float(core.p1)
    ]
    assert len(matches) <= 1
    if not matches:
        return None
    return core_id(matches[0]), chart_id


def floating_proposal(
    row: dict[str, Any], chart_id: str, z_text: str, expected_time: int,
) -> dict[str, Any]:
    normal_x, normal_y = source_normal_float(chart_id, z_text)
    source_center_x = 0.5 if row["source"] == "W" else 0.0
    source_center_y = 0.5 if row["source"] == "W" else 0.0
    source_radius = FLOAT_RADIUS[row["source"]]
    qx = source_center_x + source_radius * normal_x
    qy = source_center_y + source_radius * normal_y
    target_x, target_y = target_center_float(row["target"])
    target_radius = FLOAT_RADIUS[row["target"][0]]
    dx, dy = target_x - qx, target_y - qy
    distance_squared = dx * dx + dy * dy
    tangent_length = math.sqrt(distance_squared - target_radius * target_radius)
    ux = (
        tangent_length * dx + row["epsilon"] * target_radius * dy
    ) / distance_squared
    uy = (
        tangent_length * dy - row["epsilon"] * target_radius * dx
    ) / distance_squared
    qx, qy, ux, uy, normal_x, normal_y, _root = collide_float(
        qx, qy, ux, uy, row["miss_target"]
    )
    itinerary = [row["miss_target"]]
    current_id = row["miss_target"]
    assert detect_core_float(current_id, normal_x, normal_y, ux, uy) is None
    destination = None
    for step in range(1, expected_time + 1):
        current_id, state = nearest_float(qx, qy, ux, uy, current_id)
        qx, qy, ux, uy, normal_x, normal_y, _root = state
        itinerary.append(current_id)
        destination = detect_core_float(
            current_id, normal_x, normal_y, ux, uy
        )
        if step < expected_time:
            assert destination is None
    assert destination is not None
    destination_core_id, destination_chart = destination
    return {
        "occurrence_id": row["occurrence_id"],
        "source_chart": chart_id,
        "z": z_text,
        "post_suffix_collision_count_to_core": expected_time,
        "suffix_and_future_targets": itinerary,
        "destination_core_id": destination_core_id,
        "destination_chart": destination_chart,
    }


def refresh_arb_constants() -> None:
    ctx.prec = PRECISION_BITS
    bulk.INV_SQRT_TWO = (arb(1) / 2).sqrt()
    bulk.ARB_RADIUS = {
        obstacle: frozen_charge.arbq(radius)
        for obstacle, radius in bulk.R.items()
    }
    bulk.ARB_RADIUS_SQUARED = {
        obstacle: radius * radius
        for obstacle, radius in bulk.ARB_RADIUS.items()
    }
    frozen_charge.bulk.ARB_RADIUS = bulk.ARB_RADIUS


def destination_core_arb(
    chart_id: str, normal_x: arb, normal_y: arb, ux: arb, uy: arb,
) -> dict[str, Any]:
    _source, cell = chart_id.split(":")
    if cell in {"E", "W"}:
        t = normal_y
        assert bool(abs(normal_x) > abs(normal_y))
    else:
        t = normal_x
        assert bool(abs(normal_y) > abs(normal_x))
    p = -ux * normal_y + uy * normal_x
    matches = [
        core for core in core_cert.physical_cores()
        if core.chart_id == chart_id
        and bool(t > frozen_charge.arbq(core.t0))
        and bool(t < frozen_charge.arbq(core.t1))
        and bool(p > frozen_charge.arbq(core.p0))
        and bool(p < frozen_charge.arbq(core.p1))
    ]
    assert len(matches) == 1
    core = matches[0]
    return {
        "core_id": core_id(core),
        "chart_id": chart_id,
        "final_t": str(t),
        "final_p": str(p),
        "strict_interior": True,
    }


def certify_side(
    row: dict[str, Any], proposal: dict[str, Any], side: str, radius_power: int,
) -> dict[str, Any]:
    radius = Q(1, 2**radius_power)
    frozen_charge.BASE_HALF_WIDTH = radius
    frozen_charge.PARAMETER_RADIUS = radius
    frozen_charge.SQRT_DISCRIMINANT_UPPER = Q(
        1, 2 ** ((radius_power - 2) // 2)
    )
    magnitude = frozen_charge.interval(Q(0), radius)
    if side == "hit":
        state = frozen_charge.hit_suffix_state(row, magnitude)
        displacement = row["parameter_coarea_polarity"] * magnitude
        source_collision_count = 2
    else:
        state = frozen_charge.direct_suffix_state(row, magnitude)
        displacement = -row["parameter_coarea_polarity"] * magnitude
        source_collision_count = 1
    qx, qy, ux, uy, normal_x, normal_y, suffix_record = state
    itinerary = proposal["suffix_and_future_targets"]
    assert suffix_record["target"] == itinerary[0] == row["miss_target"]
    step_records = [suffix_record]
    current_id = itinerary[0]
    for expected_id in itinerary[1:]:
        state = frozen_charge.step_expected(
            qx, qy, ux, uy, current_id, expected_id, displacement
        )
        qx, qy, ux, uy, normal_x, normal_y, record = state
        step_records.append(record)
        current_id = expected_id
    expected_time = proposal["post_suffix_collision_count_to_core"]
    assert len(step_records) == expected_time + 1
    destination = destination_core_arb(
        proposal["destination_chart"], normal_x, normal_y, ux, uy
    )
    assert destination["core_id"] == proposal["destination_core_id"]
    payload = {
        "occurrence_id": row["occurrence_id"],
        "side": side,
        "source_chart": proposal["source_chart"],
        "z": proposal["z"],
        "radius_power": radius_power,
        "itinerary": itinerary,
        "core_id": destination["core_id"],
    }
    return {
        "charged_branch_id": "all-core-charge:" + canonical_digest(payload),
        "occurrence_id": row["occurrence_id"],
        "side": side,
        "source_chart": proposal["source_chart"],
        "base_z_center": proposal["z"],
        "base_z_half_width_power": radius_power,
        "parameter_radius_power": radius_power,
        "parameter_magnitude_interval": ["0_open", str(radius)],
        "parameter_sign": (
            row["parameter_coarea_polarity"]
            if side == "hit" else -row["parameter_coarea_polarity"]
        ),
        "source_collision_count_to_regular_suffix": source_collision_count,
        "post_suffix_collision_word_length": expected_time,
        "certified_core_entrance_by_post_suffix_time": expected_time,
        "destination": destination,
        "complete_itinerary": itinerary,
        "every_listed_collision_is_unique_and_regular": True,
        "terminal_core_membership_is_strict": True,
        "step_records_sha256": canonical_digest(step_records),
    }


def load_dependencies() -> dict[str, Any]:
    for name, expected in DEPENDENCIES.items():
        path = HERE / name
        assert path.is_file()
        assert sha256_path(path) == expected
    old_manifest = json.loads(
        (HERE / "cm2-gate34-positive-core-hit-charge-manifest-2026-07-17.json").read_text(
            encoding="utf-8"
        )
    )
    assert old_manifest["verdict"]["positive_all_scale_core_hit_occurrences_2"] == "CERTIFIED"
    assert old_manifest["verdict"]["positive_all_scale_core_hit_oriented_branches_4"] == "CERTIFIED"
    assert old_manifest["result"]["selected_positive_core_hit_charge_registry"]["charged_occurrence_count"] == 2
    return old_manifest


def positive_core_hit_registry(old_manifest: dict[str, Any]) -> dict[str, Any]:
    maximal_rows, _registry = current.load_maximal_rows()
    by_id = {row["occurrence_id"]: row for row in maximal_rows}
    old_occurrences = set(frozen_charge.SELECTED)
    new_occurrences = set(NEW_CHARGES)
    assert len(by_id) == 64
    assert len(old_occurrences) == 2
    assert len(new_occurrences) == 62
    assert old_occurrences.isdisjoint(new_occurrences)
    assert old_occurrences | new_occurrences == set(by_id)

    proposals = []
    for occurrence_id, (chart_id, z_text, expected_time, radius_power) in sorted(
        NEW_CHARGES.items()
    ):
        proposal = floating_proposal(
            by_id[occurrence_id], chart_id, z_text, expected_time
        )
        proposal["radius_power"] = radius_power
        proposals.append(proposal)

    refresh_arb_constants()
    records = []
    for proposal in proposals:
        row = dict(by_id[proposal["occurrence_id"]])
        row["witness"] = dict(row["witness"])
        row["witness"]["chart_id"] = proposal["source_chart"]
        row["witness"]["z"] = proposal["z"]
        for side in ("hit", "miss"):
            records.append(
                certify_side(row, proposal, side, proposal["radius_power"])
            )
    records.sort(key=canonical_json)
    assert len(records) == 124
    assert len({row["charged_branch_id"] for row in records}) == 124
    assert len({row["occurrence_id"] for row in records}) == 62

    radius_histogram: dict[str, int] = {}
    time_histogram: dict[str, int] = {}
    new_volume = Q(0)
    for proposal in proposals:
        radius_power = proposal["radius_power"]
        radius_histogram[str(radius_power)] = (
            radius_histogram.get(str(radius_power), 0) + 1
        )
        time = proposal["post_suffix_collision_count_to_core"]
        time_histogram[str(time)] = time_histogram.get(str(time), 0) + 1
        new_volume += Q(4, 2 ** (2 * radius_power))

    old_registry = old_manifest["result"]["selected_positive_core_hit_charge_registry"]
    total_volume = new_volume + Q(old_registry["labelled_base_parameter_coordinate_volume"])
    radius_histogram["220"] = radius_histogram.get("220", 0) + 2
    time_histogram["20"] = time_histogram.get("20", 0) + 2
    assert radius_histogram == {
        "80": 32, "100": 8, "120": 16, "180": 2, "200": 4, "220": 2,
    }
    assert time_histogram == {
        "2": 22, "3": 10, "4": 8, "7": 8, "8": 4,
        "9": 4, "16": 2, "19": 4, "20": 2,
    }
    assert total_volume > Q(1, 2**153)
    assert total_volume < Q(1, 2**152)
    return {
        "maximal_reference_occurrence_count": 64,
        "maximal_reference_oriented_branch_count": 128,
        "imported_frozen_occurrence_count": 2,
        "imported_frozen_oriented_branch_count": 4,
        "new_Arb_validated_occurrence_count": 62,
        "new_Arb_validated_oriented_branch_count": 124,
        "charged_occurrence_count": 64,
        "charged_oriented_branch_count": 128,
        "all_maximal_occurrence_ids_have_positive_all_scale_cylinders": True,
        "both_oriented_sides_validated_for_every_occurrence": True,
        "floating_pilot_has_proposal_status_only": True,
        "Arb_precision_bits": PRECISION_BITS,
        "radius_power_histogram_by_occurrence": radius_histogram,
        "post_suffix_core_entrance_word_length_histogram_by_occurrence": time_histogram,
        "maximum_certified_post_suffix_core_entrance_word_length": 20,
        "new_62_labelled_base_parameter_coordinate_volume": str(new_volume),
        "all_64_labelled_base_parameter_coordinate_volume": str(total_volume),
        "all_64_labelled_coordinate_volume_strict_lower_bound": "2^-153",
        "all_64_labelled_coordinate_volume_strict_upper_bound": "2^-152",
        "all_new_800_regular_suffix_and_post_suffix_flights_unique": True,
        "all_124_new_terminal_core_memberships_strict": True,
        "charged_occurrence_ids_sha256": canonical_digest(sorted(by_id)),
        "floating_proposals_sha256": canonical_digest(proposals),
        "new_charged_branch_rows_sha256": canonical_digest(records),
        "first_new_charged_branch_id": records[0]["charged_branch_id"],
        "last_new_charged_branch_id": records[-1]["charged_branch_id"],
    }


def build_result() -> dict[str, Any]:
    old_manifest = load_dependencies()
    result: dict[str, Any] = {
        "schema": "cm2.gate34.all-occurrence-positive-core-hit.v1",
        "provenance": {
            "dependency_sha256": dict(DEPENDENCIES),
            "old_artifacts_modified": False,
            "floating_search_role": "proposal_only",
            "admission_engine": "python-flint Arb",
            "precision_bits": PRECISION_BITS,
        },
        "all_occurrence_positive_core_hit_registry": positive_core_hit_registry(
            old_manifest
        ),
        "strict_nonpromotion": {
            "positive_cylinders_cover_entire_maximal_rows": False,
            "labelled_coordinate_volume_is_collision_SRB_fraction": False,
            "displayed_entrance_word_is_first_core_stopping_time": False,
            "uniform_normalized_core_hit_fraction": "NOT_CERTIFIED",
            "post_core_2018_step_no_recut_dwell": "NOT_CERTIFIED",
            "post_core_12108_step_field7_dwell": "NOT_CERTIFIED",
            "fixed_core_multiplier_survival": "NOT_CERTIFIED",
            "common_two_view_restriction": "NOT_CERTIFIED",
            "quantitative_cemetery_tail": "NOT_CERTIFIED",
            "common_strong_space_DQ_MT_DQ_FACE_recovery": "NOT_CERTIFIED",
            "Gate3": "NOT_CERTIFIED",
            "Gate4": "NOT_CERTIFIED",
        },
    }
    result["internal_replay_digest"] = canonical_digest(result)
    return result


def main() -> None:
    print(json.dumps(build_result(), indent=2, sort_keys=True))
    print("POSITIVE_ALL_SCALE_CORE_HIT_OCCURRENCES_64: CERTIFIED")
    print("POSITIVE_ALL_SCALE_CORE_HIT_ORIENTED_BRANCHES_128: CERTIFIED")
    print("MAXIMUM_POST_SUFFIX_CORE_ENTRANCE_WORD_LENGTH_20: CERTIFIED")
    print("FIRST_CORE_STOPPING_TIME: NOT_CERTIFIED")
    print("NATIVE_2018_12108_NO_RECUT_DWELL: NOT_CERTIFIED")
    print("GATE4: NOT_CERTIFIED")


if __name__ == "__main__":
    main()
