#!/usr/bin/env python3
"""Independent fail-closed verifier for the Round138 two-sided frontier.

The Round138 producer is never imported or executed.  The verifier rebuilds
the implicit slope-four parent leaf, its D=0 and two signed side roots, fixed
dyadic centres, two exact leaf graphs and enclosing rational squares, all
298+349 collision rows, retained and full-radius candidate ledgers, official
registry words, homogeneity and incidence ranks, terminal C24 cores, the
primitive-free Round132 crosswalk, global insertion time j=3, and every
nonpromotion boundary.

Only frozen lower-round helper libraries are shared.  No Round138 build
function or temporary spike output is used.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import stat
import tempfile
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Callable

from flint import arb, ctx

import cm2_gate25_physical_return_core_registry_cert as core_cert
import cm2_gate34_full_core_return_adaptive_frontier_cert as step1
import cm2_gate34_positive_core_hit_charge_cert as charge
import cm2_gate34_round28_nonempty_adaptive_component_registry_cert as component_cert
import cm2_gate34_round29_q2_time3_anchor_registry_cert as time3
import cm2_round116_rank3_interior_two_sided_transverse_collar as round116
import cm2_round117_rank3_countable_homogeneity_operator_cells as round117
import cm2_round136_rank3_positive_width_r1056_return_frontier as round136
from cm2_round79_tangency_intersection_generator import aq, strict_sign
from cm2_round80_time3_tangency_curve_generator import third_tangency_jet


HERE = Path(__file__).resolve().parent
VERIFIER = Path(__file__).resolve()
PRODUCER = (
    HERE / "cm2_round138_rank3_same_slope4_two_sided_return_frontier.py"
)
CERTIFICATE = (
    HERE
    / "cm2-round138-rank3-same-slope4-two-sided-return-frontier-2026-07-24.json"
)
OUTPUT = (
    HERE
    / "cm2-round138-rank3-same-slope4-two-sided-return-frontier-verification-2026-07-24.json"
)
CERTIFICATE_SCHEMA = (
    "cm2.round138.rank3-same-slope4-two-sided-return-frontier.v1"
)
VERIFICATION_SCHEMA = (
    "cm2.round138.rank3-same-slope4-two-sided-return-frontier-verification.v1"
)

PRODUCER_SHA256 = (
    "42d749dccea86aa3a122707db0226def176e75047d5dcb4bf19826b50e09282b"
)
CERTIFICATE_SHA256 = (
    "c1f4d5041d810dd91d38e39bf795e5ab05536065ba8b0730530c58a91f7bf6d8"
)
CERTIFICATE_RESULT_SHA256 = (
    "a46f4122639ccb82eed2d06d916972020b81c4f566ccfb05a9644de382a2e123"
)

MINIMUM_PRECISION_BITS = 12288
SECONDARY_PRECISION_BITS = 16384
MAX_CERTIFICATE_BYTES = 5_000_000
MAX_INTEGER_DIGITS = 10_000

SOURCE_CORE_INDEX = 14
SOURCE_ABSOLUTE_OWNER = "W[0,0]"
SECOND_OWNER = "G[0,1]"
DESIGNATED_TANGENT_OWNER = "W[0,0]"
EXPECTED_SOURCE_CHART = "W:E"
EXPECTED_SOURCE_TARGET = "W[1,0]"
SOURCE_P_STAR = Q(-1587, 1638400)
R_W = Q(4, 25)
R_W_SQUARED = R_W * R_W
SLOPE = Q(4)
KAPPA = SLOPE * R_W
SHIFT = R_W_SQUARED * Q(1, 2**128)
ROOT_INITIAL_INTERVAL = (Q(19, 1000), Q(1, 50))
D0_BISECTIONS = 4096
SIDE_BISECTIONS = 2048
B_STAR_ENCLOSURE_BITS = 4104
P_CENTER_ROUNDING_BITS = 4096
INWARD_POWER = 1800
GRAPH_HALF_WIDTH_POWER = 2400
OFFICIAL_REGISTRY_STREAM_SHA256 = (
    "841cb96798c9bd41e1440c8b2cdd93af5d80f2f64d693f2aa00175a440045ab9"
)

EXPECTED = {
    "BYPASS": {
        "target_sign": -1,
        "return_depth": 298,
        "terminal_target": "W[1,10]",
        "destination_core_id":
            "core:1f2ba5184f0fb0d3879e6af889710cd0c41b98b1227b8f97bb706c42791a6f61",
        "third_owner": "W[0,-1]",
        "official_sequence_sha256":
            "0ff6b6a1c29afaf10b6697fcb0b31913ff2e7fb1674d5e631caf379dd2c6224e",
        "unique_official_word_key_count": 86,
    },
    "HIT": {
        "target_sign": 1,
        "return_depth": 349,
        "terminal_target": "G[-3,-6]",
        "destination_core_id":
            "core:f8b025dd81d1bdf83339ceb4295c431494540d9ab25a1dff45221614644874b8",
        "third_owner": DESIGNATED_TANGENT_OWNER,
        "official_sequence_sha256":
            "901924e8522a6b97f4d02f1833fd79f053b566e935a9f334fdf2672407ef5e5c",
        "unique_official_word_key_count": 86,
    },
}

ROUND116 = (
    HERE / "cm2-round116-rank3-interior-two-sided-transverse-collar-2026-07-23.json"
)
ROUND116V = (
    HERE
    / "cm2-round116-rank3-interior-two-sided-transverse-collar-verification-2026-07-23.json"
)
ROUND117 = (
    HERE / "cm2-round117-rank3-countable-homogeneity-operator-cells-2026-07-23.json"
)
ROUND117V = (
    HERE
    / "cm2-round117-rank3-countable-homogeneity-operator-cells-verification-2026-07-23.json"
)
ROUND132_PRODUCER = HERE / "cm2_round132_round28_occurrence_record_materialization.py"
ROUND132 = (
    HERE / "cm2-round132-round28-occurrence-record-materialization-2026-07-24.json"
)
ROUND132V = (
    HERE
    / "cm2-round132-round28-occurrence-record-materialization-verification-2026-07-24.json"
)
ROUND135_PRODUCER = HERE / "cm2_round135_rank3_wide_positive_borel_local_robustness.py"
ROUND135 = (
    HERE / "cm2-round135-rank3-wide-positive-borel-local-robustness-2026-07-24.json"
)
ROUND135_VERIFIER = (
    HERE / "cm2_round135_rank3_wide_positive_borel_local_robustness_verifier.py"
)
ROUND135V = (
    HERE
    / "cm2-round135-rank3-wide-positive-borel-local-robustness-verification-2026-07-24.json"
)
ROUND136_PRODUCER = (
    HERE / "cm2_round136_rank3_positive_width_r1056_return_frontier.py"
)
ROUND136 = (
    HERE / "cm2-round136-rank3-positive-width-r1056-return-frontier-2026-07-24.json"
)
ROUND136_VERIFIER = (
    HERE / "cm2_round136_rank3_positive_width_r1056_return_frontier_verifier.py"
)
ROUND136V = (
    HERE
    / "cm2-round136-rank3-positive-width-r1056-return-frontier-verification-2026-07-24.json"
)

PINS = {
    "cm2_gate25_physical_return_core_registry_cert.py":
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
    "cm2_gate34_full_core_return_adaptive_frontier_cert.py":
        "d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24",
    "cm2_gate34_positive_core_hit_charge_cert.py":
        "922a417d06b7456b4349edf98d22d56d56df1045f6415b05bc0e5f0a4d5b2bdf",
    "cm2_gate34_round28_nonempty_adaptive_component_registry_cert.py":
        "b489f498cac2650a6456da0540d035b2cc9654a69f5dc0110db85933eecd12f6",
    "cm2_gate34_round29_q2_time3_anchor_registry_cert.py":
        "399ea86401e97d2679fb3f3f7a0a9328266d8d583e73fd5c5ed2bc811c14475b",
    "cm2_round79_tangency_intersection_generator.py":
        "971f918ca1ed23bd081adf3b233d578e750b61231b20113327f221b40b890ed7",
    "cm2_round80_time3_tangency_curve_generator.py":
        "68d17d088e94a8d5b0b97a6518691e19da2560be7df7fcff32eacdfd367aa659",
    "cm2_round116_rank3_interior_two_sided_transverse_collar.py":
        "91ea057ad31517ce6b390561e9b894e219a837fa3a3be793fc96db082566f3f7",
    "cm2_round117_rank3_countable_homogeneity_operator_cells.py":
        "8112aeb2c5d67a914a651683c9a497def3c2ffed81b1c42b365bb257cf8f7e7c",
    ROUND116.name:
        "504e070eea10fbab3b1968423ecedcda6fa8fc20549adb9ef3e9ed42bd2c45b3",
    ROUND116V.name:
        "6e12d118c7955bd0405c79dcf7b9de40df56f3eba6bc96ee6c1078898a038750",
    ROUND117.name:
        "31b6535e21886d825d5a4658f2c9d3ccc8c5525c2b9d2fb181f88baa7dcf9eb0",
    ROUND117V.name:
        "06647b5b6f81ad0e8098f5885e9aa2b2c926991faaa34102e0646c058da0764f",
    ROUND132_PRODUCER.name:
        "88a12779148a49f111380c0560b0cb490a4e87f00d7ba7671878eec858f87d53",
    ROUND132.name:
        "b5d09c7398dae4b77a6f011430286f88539e0f13ca449e50eb84fc3712d67d31",
    ROUND132V.name:
        "26ef83ceb2aa484388e99a4f832670c7e13429452aec7a56945d2db4cb97f171",
    ROUND135_PRODUCER.name:
        "87ea759a966be5ea9762c075c9e3e8e218b0e76c74c0775f610259f8bf1fa99d",
    ROUND135.name:
        "31b4b017ac7da341b210d28dc2296ba2499d425615f2c3bce750ccec586f67df",
    ROUND135_VERIFIER.name:
        "ca0cf023e761be7e654dcb6d50d87898301b912a105df14e2f92eec4dabd53dd",
    ROUND135V.name:
        "caaebfdaa85c95d269af32c044de00c313355ddb501570e3bfbe4871231235e7",
    ROUND136_PRODUCER.name:
        "4e78309d5275bf367e6df03509c40ebaaac6f344c7948446a25b3b508c8c2bc2",
    ROUND136.name:
        "d9b7b7823dddce2dcbc16412294c8ecef42b304712d4bb968896d2221b8aa7f9",
    ROUND136_VERIFIER.name:
        "597778df1deefa34b690c4ed665fcb1f8df965aa45d9a7c03093a0e632cf23ad",
    ROUND136V.name:
        "501035c235124e1c1a57fa198ee63e4f90c7a729497b600c31b2212e5260964c",
}

CLOSED_SCHEMAS = {
    ROUND116.name:
        "cm2.round116.rank3-interior-two-sided-transverse-collar.v1",
    ROUND116V.name:
        "cm2.round116.rank3-interior-two-sided-transverse-collar.verification.v1",
    ROUND117.name:
        "cm2.round117.rank3-countable-homogeneity-operator-cells.v1",
    ROUND117V.name:
        "cm2.round117.rank3-countable-homogeneity-operator-cells-verification.v1",
    ROUND132.name:
        "cm2.round132.round28-occurrence-record-materialization.v1",
    ROUND132V.name:
        "cm2.round132.round28-occurrence-record-materialization-verification.v1",
    ROUND135.name:
        "cm2.round135.rank3-wide-positive-borel-local-robustness.v1",
    ROUND135V.name:
        "cm2.round135.rank3-wide-positive-borel-local-robustness-verification.v1",
    ROUND136.name:
        "cm2.round136.rank3-positive-width-r1056-return-frontier.v1",
    ROUND136V.name:
        "cm2.round136.rank3-positive-width-r1056-return-frontier-verification.v1",
}


class VerificationError(RuntimeError):
    """Fail-closed parsing, reconstruction, semantic or path error."""


def require(condition: bool, label: str) -> None:
    if not condition:
        raise VerificationError(label)


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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qstr(value: Q | int) -> str:
    value = Q(value)
    return (
        str(value.numerator)
        if value.denominator == 1
        else f"{value.numerator}/{value.denominator}"
    )


def strict_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(type(key) is str and key not in result, "duplicate JSON key")
        result[key] = value
    return result


def strict_integer(token: str) -> int:
    require(len(token.lstrip("-")) <= MAX_INTEGER_DIGITS, "oversized JSON integer")
    require(token != "-0", "negative-zero JSON integer")
    return int(token)


def reject_float(token: str) -> float:
    raise VerificationError(f"floating JSON number forbidden:{token}")


def reject_constant(token: str) -> None:
    raise VerificationError(f"invalid JSON constant:{token}")


def validate_json_strings(value: Any) -> None:
    if isinstance(value, str):
        require(
            all(not (0xD800 <= ord(character) <= 0xDFFF) for character in value),
            "unpaired JSON surrogate",
        )
    elif isinstance(value, list):
        for child in value:
            validate_json_strings(child)
    elif isinstance(value, dict):
        for key, child in value.items():
            validate_json_strings(key)
            validate_json_strings(child)


def strict_json_bytes(raw: bytes, label: str) -> dict[str, Any]:
    require(not raw.startswith(b"\xef\xbb\xbf"), f"UTF-8 BOM:{label}")
    try:
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=strict_pairs,
            parse_int=strict_integer,
            parse_float=reject_float,
            parse_constant=reject_constant,
        )
    except (UnicodeError, json.JSONDecodeError, ValueError) as exc:
        raise VerificationError(f"strict JSON:{label}") from exc
    require(type(value) is dict, f"top-level JSON object:{label}")
    validate_json_strings(value)
    return value


def strict_json(path: Path) -> dict[str, Any]:
    metadata = path.lstat()
    require(
        stat.S_ISREG(metadata.st_mode)
        and metadata.st_nlink == 1
        and not path.is_symlink(),
        f"unsafe input type:{path.name}",
    )
    return strict_json_bytes(path.read_bytes(), path.name)


def load_closed(path: Path) -> dict[str, Any]:
    value = strict_json(path)
    require(
        set(value) == {"schema", "result", "result_sha256"},
        f"closed dependency envelope:{path.name}",
    )
    require(value["schema"] == CLOSED_SCHEMAS[path.name], f"schema:{path.name}")
    require(type(value["result"]) is dict, f"result object:{path.name}")
    require(
        value["result_sha256"] == digest(value["result"]),
        f"result digest:{path.name}",
    )
    return value["result"]


def verification_passed(result: dict[str, Any]) -> bool:
    return result.get("status") == "PASS" or result.get("verdict") == "PASS"


def validate_dependencies() -> dict[str, dict[str, Any]]:
    for name, expected in sorted(PINS.items()):
        path = HERE / name
        metadata = path.lstat()
        require(
            stat.S_ISREG(metadata.st_mode)
            and metadata.st_nlink == 1
            and not path.is_symlink(),
            f"pinned input type:{name}",
        )
        require(path.resolve().parent == HERE, f"pinned input parent:{name}")
        require(sha256(path) == expected, f"dependency byte pin:{name}")
    closed = {
        path.name: load_closed(path)
        for path in (
            ROUND116,
            ROUND116V,
            ROUND117,
            ROUND117V,
            ROUND132,
            ROUND132V,
            ROUND135,
            ROUND135V,
            ROUND136,
            ROUND136V,
        )
    }
    for path in (ROUND116V, ROUND117V, ROUND132V, ROUND135V, ROUND136V):
        require(verification_passed(closed[path.name]), f"verification PASS:{path.name}")
    require(
        closed[ROUND135.name]["gate5_global_maturity"] == "10/18"
        and closed[ROUND135.name]["global_complete_18_field_block_count"] == 0
        and closed[ROUND135.name]["cm2_verdict"] == "NO-GO_FOR_CLAIM",
        "Round135 global safety",
    )
    require(
        closed[ROUND136.name]["count_ledger"]["Round50_owner_key_count"] == 0
        and closed[ROUND136.name]["count_ledger"]["Round67_q_j_output_count"] == 0,
        "Round136 frontier safety",
    )
    round136.validate_dependencies()
    return closed


def exact_dyadic(point: arb) -> Q:
    mantissa, exponent = point.man_exp()
    return Q(int(mantissa)) * (Q(2) ** int(exponent))


def arb_pair(value: arb) -> tuple[Q, Q]:
    return exact_dyadic(value.lower()), exact_dyadic(value.upper())


def power_of_two(exponent: int) -> Q:
    return Q(2**exponent) if exponent >= 0 else Q(1, 2 ** (-exponent))


def floor_log2_fraction(value: Q) -> int:
    require(value > 0, "positive rational logarithm")
    exponent = value.numerator.bit_length() - value.denominator.bit_length()
    while power_of_two(exponent) > value:
        exponent -= 1
    while power_of_two(exponent + 1) <= value:
        exponent += 1
    return exponent


def strict_dyadic_depth(value: arb, lower: Q | None = None) -> int:
    if lower is None:
        lower, _upper = arb_pair(value)
    require(lower > 0, "strict positive margin")
    exponent = floor_log2_fraction(lower)
    if lower == power_of_two(exponent):
        exponent -= 1
    depth = -exponent
    require(bool(value > aq(power_of_two(-depth))), "dyadic lower-bound replay")
    return depth


def interval(lower: Q, upper: Q) -> arb:
    return time3.time2_cert.first_hit.arb_interval(lower, upper)


def dyadic(power: int) -> Q:
    return Q(1, 2**power)


def floor_q(value: Q) -> int:
    return value.numerator // value.denominator


def ceil_q(value: Q) -> int:
    return -floor_q(-value)


def fixed_dyadic_outer(value: arb, bits: int) -> tuple[Q, Q]:
    lower, upper = arb_pair(value)
    scale = 2**bits
    fixed_lower = Q(floor_q(lower * scale), scale)
    fixed_upper = Q(ceil_q(upper * scale), scale)
    require(
        fixed_lower < fixed_upper
        and bool(value > aq(fixed_lower))
        and bool(value < aq(fixed_upper)),
        "fixed dyadic outer enclosure",
    )
    return fixed_lower, fixed_upper


def unique_nearest_dyadic(value: arb, bits: int) -> Q:
    lower, upper = arb_pair(value)
    scale = 2**bits
    lower_index = floor_q(lower * scale + Q(1, 2))
    upper_index = floor_q(upper * scale + Q(1, 2))
    require(lower_index == upper_index, "unique nearest dyadic rounding")
    rounded = Q(lower_index, scale)
    half_cell = Q(1, 2 ** (bits + 1))
    require(
        bool(value > aq(rounded - half_cell))
        and bool(value < aq(rounded + half_cell)),
        "nearest dyadic rounding cell",
    )
    return rounded


def with_hash(row: dict[str, Any]) -> dict[str, Any]:
    require("row_sha256" not in row, "row already hashed")
    return {**row, "row_sha256": digest(row)}


def compact_key(key: dict[str, Any]) -> dict[str, Any]:
    return {
        "official_word_key_id": key["word_key_id"],
        "ordinal_zero_based": key["ordinal_zero_based"],
        "registry_row": key["row"],
        "registry_row_sha256": key["row_sha256"],
    }


class StableMarginLedger:
    """Precision-independent public ledger of strict dyadic decisions."""

    def __init__(self) -> None:
        self.depths: dict[str, int] = {}
        self.counts: Counter[str] = Counter()
        self.witnesses: dict[str, dict[str, Any] | None] = {}

    def observe(
        self,
        name: str,
        value: arb,
        witness: dict[str, Any] | None = None,
    ) -> int:
        depth = strict_dyadic_depth(value)
        self.counts[name] += 1
        if name not in self.depths or depth > self.depths[name]:
            self.depths[name] = depth
            self.witnesses[name] = witness
        return depth

    def public(self) -> dict[str, Any]:
        return {
            name: {
                "dyadic_depth": self.depths[name],
                "strict_lower_bound": qstr(power_of_two(-self.depths[name])),
                "observation_count": self.counts[name],
                "one_worst-depth_witness": self.witnesses[name],
            }
            for name in sorted(self.depths)
        }


def initial_state(atom: step1.Atom) -> dict[str, Any]:
    qx, qy, ux, uy, s = time3.time2_cert.first_hit.phase_geometry(atom.phase_box)
    return {
        "contact_x": qx,
        "contact_y": qy,
        "outgoing_x": ux,
        "outgoing_y": uy,
        "s": s,
        "chart": atom.source_core.chart_id.split(":")[1],
        "normal_x": (
            (1 - time3.time2_cert.first_hit.arb_interval(atom.t0, atom.t1) ** 2).sqrt()
        ),
        "normal_y": time3.time2_cert.first_hit.arb_interval(atom.t0, atom.t1),
        "p": time3.time2_cert.first_hit.arb_interval(atom.p0, atom.p1),
    }


def complete_owner(
    state: dict[str, Any],
    current_target: str,
    ledger: StableMarginLedger,
    collision_index: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    qx, qy, ux, uy, s = (
        state["contact_x"],
        state["contact_y"],
        state["outgoing_x"],
        state["outgoing_y"],
        state["s"],
    )
    chart = state["chart"]
    candidates = tuple(time3.time2_cert.translated_candidate_ids(current_target, chart))
    future: list[tuple[str, dict[str, arb]]] = []
    histogram: Counter[str] = Counter()
    decision_depths: list[int] = []
    for candidate_id in candidates:
        center_x, center_y = time3.time2_cert.target_center(candidate_id, s)
        dx, dy = center_x - qx, center_y - qy
        ell = ux * dx + uy * dy
        transverse = -uy * dx + ux * dy
        radius = aq(time3.time2_cert.first_hit.RADIUS[candidate_id[0]])
        discriminant = radius * radius - transverse * transverse
        witness = {
            "collision_index": collision_index,
            "candidate_id": candidate_id,
        }
        if bool(discriminant < 0):
            histogram["no_real_intersection"] += 1
            decision_depths.append(
                ledger.observe(
                    "candidate_miss_discriminant",
                    -discriminant,
                    witness,
                )
            )
            continue
        require(bool(discriminant > 0), "candidate discriminant strict")
        decision_depths.append(
            ledger.observe(
                "candidate_positive_discriminant",
                discriminant,
                witness,
            )
        )
        radical = discriminant.sqrt()
        near, far = ell - radical, ell + radical
        if bool(far < 0):
            histogram["intersection_strictly_behind"] += 1
            decision_depths.append(
                ledger.observe(
                    "candidate_behind_far_root",
                    -far,
                )
            )
            continue
        require(bool(near > 0), "candidate future root strict")
        histogram["strict_future_near_root"] += 1
        decision_depths.append(
            ledger.observe(
                "candidate_future_root_positive",
                near,
            )
        )
        future.append(
            (
                candidate_id,
                {
                    "near": near,
                    "radical": radical,
                    "transverse": transverse,
                    "radius": radius,
                    "discriminant": discriminant,
                },
            )
        )
    winners = [
        (candidate_id, row)
        for candidate_id, row in future
        if all(
            candidate_id == other_id or bool(row["near"] < other["near"])
            for other_id, other in future
        )
    ]
    require(len(winners) == 1, "strict unique collision owner")
    selected_id, selected = winners[0]
    gap_depths = [
        ledger.observe(
            "winner_pairwise_root_gap",
            row["near"] - selected["near"],
        )
        for candidate_id, row in future
        if candidate_id != selected_id
    ]
    root = selected["near"]
    tau_margin = aq(time3.time2_cert.first_hit.TAU_MAX) - root
    require(bool(tau_margin > 0), "winner flight cap")
    root_depth = ledger.observe(
        "selected_root_positive",
        root,
    )
    selected_discriminant_depth = ledger.observe(
        "selected_discriminant_positive",
        selected["discriminant"],
        {"collision_index": collision_index, "candidate_id": selected_id},
    )
    tau_depth = ledger.observe(
        "selected_root_below_tau_max",
        tau_margin,
    )
    radical, transverse, radius = (
        selected["radical"],
        selected["transverse"],
        selected["radius"],
    )
    normal_x = (-radical * ux + transverse * uy) / radius
    normal_y = (-radical * uy - transverse * ux) / radius
    momentum = transverse / radius
    cosine = radical / radius
    owner = {
        "selected_target_id": selected_id,
        "selected_root": root,
        "normal_x": normal_x,
        "normal_y": normal_y,
        "p": momentum,
        "cosine": cosine,
    }
    audit = {
        "retained_candidate_count": len(candidates),
        "candidate_classification_histogram": dict(sorted(histogram.items())),
        "minimum_candidate_decision_margin_dyadic_depth": max(decision_depths),
        "minimum_winner_gap_dyadic_depth":
            max(gap_depths) if gap_depths else None,
        "selected_root_positive_margin_dyadic_depth": root_depth,
        "selected_discriminant_positive_margin_dyadic_depth":
            selected_discriminant_depth,
        "selected_root_below_tau_margin_dyadic_depth": tau_depth,
    }
    return owner, audit


def translation_normalized_official_word(
    state: dict[str, Any],
    current_target: str,
    owner: dict[str, Any],
    pair_index: dict[tuple[str, str], int],
    pattern_index: dict[tuple[str, ...], int],
) -> tuple[dict[str, Any] | None, str | None]:
    qx, qy, ux, uy = (
        state["contact_x"],
        state["contact_y"],
        state["outgoing_x"],
        state["outgoing_y"],
    )
    root = owner["selected_root"]
    require(
        all(isinstance(value, arb) for value in (qx, qy, ux, uy, root)),
        "official word Arb geometry",
    )
    hit_x, hit_y = qx + root * ux, qy + root * uy
    _obstacle, shift_x, shift_y = component_cert.parse_target(current_target)
    relative_qx, relative_hx = qx - arb(shift_x), hit_x - arb(shift_x)
    relative_qy, relative_hy = qy - arb(shift_y), hit_y - arb(shift_y)
    x_events, reason = component_cert.ordered_axis_events(
        relative_qx, relative_hx, "X"
    )
    if x_events is None:
        return None, reason
    y_events, reason = component_cert.ordered_axis_events(
        relative_qy, relative_hy, "Y"
    )
    if y_events is None:
        return None, reason
    crossings, reason = component_cert.strict_event_order(x_events + y_events)
    if crossings is None:
        return None, reason
    chart = f"{current_target[0]}:{state['chart']}"
    target = component_cert.relative_target(
        current_target, owner["selected_target_id"]
    )
    if target not in time3.time2_cert.first_hit.candidate_ids(chart):
        return None, "relative_target_not_in_frozen_retained_pair"
    key = component_cert.word_key(
        chart, target, crossings, pair_index, pattern_index
    )
    return {
        "key": key,
        "relative_frozen_target_id": target,
        "ordered_clean_wall_record": list(crossings),
        "absolute_lattice_translation_removed": [shift_x, shift_y],
    }, None


def chart_margin(
    state: dict[str, Any],
    ledger: StableMarginLedger,
) -> int:
    chart = state["chart"]
    normal_x, normal_y = state["normal_x"], state["normal_y"]
    if chart in {"E", "W"}:
        margin = abs(normal_x) - abs(normal_y)
    else:
        margin = abs(normal_y) - abs(normal_x)
    require(bool(margin > 0), "outgoing strict chart margin")
    return ledger.observe("outgoing_chart_dominance", margin)


def core_margin(
    owner: dict[str, Any],
    classification: str,
    destination: str | None,
    cores: tuple[Any, ...],
    ledger: StableMarginLedger,
) -> int:
    nx, ny, momentum = owner["normal_x"], owner["normal_y"], owner["p"]
    relevant = [core for core in cores if core.source == owner["selected_target_id"][0]]
    strict_depths: list[int] = []
    inside_ids: list[str] = []
    for core in relevant:
        cell = core.chart_id.split(":")[1]
        t, _inside_tests, _outside_tests = step1.chart_tests(cell, nx, ny)
        if cell == "E":
            inside_margins = [nx, abs(nx) - abs(ny)]
            outside_margins = [-nx, abs(ny) - abs(nx)]
        elif cell == "W":
            inside_margins = [-nx, abs(nx) - abs(ny)]
            outside_margins = [nx, abs(ny) - abs(nx)]
        elif cell == "N":
            inside_margins = [ny, abs(ny) - abs(nx)]
            outside_margins = [-ny, abs(nx) - abs(ny)]
        else:
            inside_margins = [-ny, abs(ny) - abs(nx)]
            outside_margins = [ny, abs(nx) - abs(ny)]
        inside_margins.extend(
            [
                t - aq(core.t0),
                aq(core.t1) - t,
                momentum - aq(core.p0),
                aq(core.p1) - momentum,
            ]
        )
        if all(bool(value > 0) for value in inside_margins):
            inside_ids.append(step1.core_id(core))
            strict_depths.extend(
                ledger.observe("return_core_inside_margin", value)
                for value in inside_margins
            )
            continue
        outside_margins.extend(
            [
                aq(core.t0) - t,
                t - aq(core.t1),
                aq(core.p0) - momentum,
                momentum - aq(core.p1),
            ]
        )
        positive = [value for value in outside_margins if bool(value > 0)]
        require(positive, "strict core exclusion separator")
        depths = [
            ledger.observe("nonreturn_core_exclusion_margin", value)
            for value in positive
        ]
        strict_depths.append(min(depths))
    if classification == "RETURN_AT_3_INNER":
        require(inside_ids == [destination], "unique strict return core")
    else:
        require(not inside_ids and destination is None, "strict nonreturn core exclusion")
    require(strict_depths, "core margin census")
    return max(strict_depths)


def capped_reciprocal_cosine_rank(
    cosine: arb,
    ledger: StableMarginLedger,
    collision_index: int,
    endpoint_role: str,
) -> int:
    cap = 14
    cap_boundary = aq(Q(1, 2**cap))
    if bool(cosine > cap_boundary):
        ledger.observe(
            "capped_reciprocal_cosine_central_margin",
            cosine - cap_boundary,
            {
                "collision_index": collision_index,
                "endpoint_role": endpoint_role,
                "certified_capped_rank": cap,
            },
        )
        return cap
    require(
        bool(cosine < cap_boundary),
        "capped reciprocal-cosine rank unresolved at central boundary",
    )
    for rank in range(cap + 1, 10000):
        lower_boundary = aq(Q(1, 2**rank))
        if bool(cosine > lower_boundary):
            upper_boundary = aq(Q(1, 2 ** (rank - 1)))
            require(
                bool(cosine < upper_boundary),
                "tail reciprocal-cosine upper boundary unresolved",
            )
            ledger.observe(
                "capped_reciprocal_cosine_tail_lower_margin",
                cosine - lower_boundary,
                {
                    "collision_index": collision_index,
                    "endpoint_role": endpoint_role,
                    "certified_capped_rank": rank,
                },
            )
            ledger.observe(
                "capped_reciprocal_cosine_tail_upper_margin",
                upper_boundary - cosine,
                {
                    "collision_index": collision_index,
                    "endpoint_role": endpoint_role,
                    "certified_capped_rank": rank,
                },
            )
            return rank
        require(
            bool(cosine < lower_boundary),
            "tail reciprocal-cosine boundary unresolved",
        )
    raise VerificationError("capped reciprocal-cosine rank above 9999")


def exact_integer_ball(value: arb) -> int:
    require(value.is_exact(), "integer ball exact")
    mantissa, exponent = value.mid().man_exp()
    integer = int(mantissa)
    if exponent >= 0:
        return integer << int(exponent)
    divisor = 1 << (-int(exponent))
    require(integer % divisor == 0, "integer ball decode")
    return integer // divisor


def generic_homogeneity_label(
    collision_index: int,
    cosine: arb,
    ledger: StableMarginLedger,
) -> tuple[str, dict[str, Any]]:
    boundary128 = round117.boundary_ball(round117.N0)
    if bool(cosine > boundary128):
        depth = ledger.observe(
            "central_homogeneity_margin",
            cosine - boundary128,
            {"collision_index": collision_index},
        )
        return "H0_CENTRAL", {
            "homogeneity_label": "H0_CENTRAL",
            "lower_boundary": "sin(128^-2)",
            "lower_boundary_margin_dyadic_depth": depth,
            "upper_boundary": None,
            "upper_boundary_margin_dyadic_depth": None,
        }
    require(bool(cosine > 0), "positive tail cosine")
    index_ball = (arb(1) / cosine.asin().sqrt()).floor()
    index = exact_integer_ball(index_ball)
    require(index >= round117.N0, "tail homogeneity index")
    lower_boundary = round117.boundary_ball(index + 1)
    upper_boundary = round117.boundary_ball(index)
    lower_margin = cosine - lower_boundary
    upper_margin = upper_boundary - cosine
    require(
        bool(lower_margin > 0) and bool(upper_margin > 0),
        "strict tail homogeneity strip",
    )
    lower_depth = ledger.observe(
        "tail_homogeneity_lower_margin",
        lower_margin,
        {"collision_index": collision_index, "homogeneity_index": index},
    )
    upper_depth = ledger.observe(
        "tail_homogeneity_upper_margin",
        upper_margin,
        {"collision_index": collision_index, "homogeneity_index": index},
    )
    return f"H{index}", {
        "homogeneity_label": f"H{index}",
        "lower_boundary": f"sin({index + 1}^-2)",
        "lower_boundary_margin_dyadic_depth": lower_depth,
        "upper_boundary": f"sin({index}^-2)",
        "upper_boundary_margin_dyadic_depth": upper_depth,
    }


def fixed_p_D(source: Any, t_value: Q) -> arb:
    return third_tangency_jet(
        source,
        SECOND_OWNER,
        DESIGNATED_TANGENT_OWNER,
        t_value,
        t_value,
        SOURCE_P_STAR,
        SOURCE_P_STAR,
    ).value


def bisect_sign(
    function: Callable[[Q], arb],
    lower: Q,
    upper: Q,
    steps: int,
    label: str,
) -> tuple[Q, Q]:
    require(
        strict_sign(function(lower)) == -1
        and strict_sign(function(upper)) == 1,
        f"{label} endpoint signs",
    )
    for _index in range(steps):
        middle = (lower + upper) / 2
        sign = strict_sign(function(middle))
        require(sign in (-1, 1), f"{label} midpoint strict sign")
        if sign < 0:
            lower = middle
        else:
            upper = middle
    return lower, upper


def leaf_p_ball(
    t_lower: Q,
    t_upper: Q,
    b_enclosure: tuple[Q, Q],
) -> arb:
    phase = (
        aq(KAPPA) * interval(t_lower, t_upper).asin()
        + interval(*b_enclosure)
    )
    return phase.sin()


def leaf_p_outer(
    t_lower: Q,
    t_upper: Q,
    b_enclosure: tuple[Q, Q],
) -> tuple[Q, Q]:
    return arb_pair(leaf_p_ball(t_lower, t_upper, b_enclosure))


def leaf_D(
    source: Any,
    t_value: Q,
    b_enclosure: tuple[Q, Q],
) -> arb:
    p_lower, p_upper = leaf_p_outer(t_value, t_value, b_enclosure)
    return third_tangency_jet(
        source,
        SECOND_OWNER,
        DESIGNATED_TANGENT_OWNER,
        t_value,
        t_value,
        p_lower,
        p_upper,
    ).value


def source_coordinate_contract(source: Any) -> dict[str, Any]:
    require(
        source.chart_id == EXPECTED_SOURCE_CHART
        and source.target_id == EXPECTED_SOURCE_TARGET
        and source.source == "W",
        "frozen W:E source",
    )
    t_ball = interval(source.t0, source.t1)
    normal_x = (1 - t_ball * t_ball).sqrt()
    theta = t_ball.asin()
    radius_coordinate = aq(R_W) * theta
    dr_dt = aq(R_W) / (1 - t_ball * t_ball).sqrt()
    require(
        bool(normal_x > 0)
        and bool(theta > 0)
        and bool(radius_coordinate > 0)
        and bool(dr_dt > 0),
        "W:E positive counterclockwise coordinate",
    )
    return {
        "source_core_index": SOURCE_CORE_INDEX,
        "source_core_id": step1.core_id(source),
        "source_target": source.target_id,
        "source_chart": source.chart_id,
        "normal_branch": "n=(+sqrt(1-t^2),t)",
        "counterclockwise_tangent_branch": "n_perp=(-t,+sqrt(1-t^2))",
        "positive_t_direction": "COUNTERCLOCKWISE",
        "contact_coordinate": "r(t)=R_W*asin(t)",
        "R_W": qstr(R_W),
        "dr_dt_formula": "R_W/sqrt(1-t^2)",
        "dr_dt_positive": True,
        "transverse_coordinate": "v=phi-4r with phi=asin(p)",
        "same_leaf_equation": "asin(p)-4*R_W*asin(t)=b_star",
        "same_leaf_p_equation": "p_b(t)=sin(4*R_W*asin(t)+b_star)",
        "same_leaf_dp_dt_formula":
            "(16/25)*sqrt(1-p_b(t)^2)/sqrt(1-t^2)",
    }


def common_leaf_geometry(
    source: Any,
) -> tuple[
    dict[str, Any],
    tuple[Q, Q],
    tuple[Q, Q],
    dict[str, tuple[Q, Q]],
    dict[str, Any],
]:
    coordinate_contract = source_coordinate_contract(source)
    d0_root = bisect_sign(
        lambda t_value: fixed_p_D(source, t_value),
        *ROOT_INITIAL_INTERVAL,
        D0_BISECTIONS,
        "fixed-p D0",
    )
    broad_jet = third_tangency_jet(
        source,
        SECOND_OWNER,
        DESIGNATED_TANGENT_OWNER,
        ROOT_INITIAL_INTERVAL[0],
        ROOT_INITIAL_INTERVAL[1],
        SOURCE_P_STAR,
        SOURCE_P_STAR,
    )
    require(bool(broad_jet.gradient[0] > 0), "fixed-p D0 uniqueness")
    exact_b_ball = (
        aq(SOURCE_P_STAR).asin()
        - aq(KAPPA) * interval(*d0_root).asin()
    )
    b_enclosure = fixed_dyadic_outer(exact_b_ball, B_STAR_ENCLOSURE_BITS)
    require(
        bool(exact_b_ball > aq(b_enclosure[0]))
        and bool(exact_b_ball < aq(b_enclosure[1])),
        "implicit b_star in fixed enclosure",
    )

    side_roots: dict[str, tuple[Q, Q]] = {}
    for label, expected in EXPECTED.items():
        target = expected["target_sign"] * SHIFT
        side_roots[label] = bisect_sign(
            lambda t_value, target=target:
                leaf_D(source, t_value, b_enclosure) - aq(target),
            *ROOT_INITIAL_INTERVAL,
            SIDE_BISECTIONS,
            f"{label} side",
        )
    bypass_root, hit_root = side_roots["BYPASS"], side_roots["HIT"]
    require(
        bypass_root[1] < d0_root[0]
        and d0_root[1] < hit_root[0],
        "BYPASS < D0 < HIT root order",
    )
    parent_domain = (bypass_root[0], hit_root[1])
    parent_p = leaf_p_outer(*parent_domain, b_enclosure)
    parent_jet = third_tangency_jet(
        source,
        SECOND_OWNER,
        DESIGNATED_TANGENT_OWNER,
        parent_domain[0],
        parent_domain[1],
        parent_p[0],
        parent_p[1],
    )
    t_ball = interval(*parent_domain)
    p_ball = interval(*parent_p)
    dp_dt = (
        aq(KAPPA)
        * (1 - p_ball * p_ball).sqrt()
        / (1 - t_ball * t_ball).sqrt()
    )
    along = parent_jet.gradient[0] + parent_jet.gradient[1] * dp_dt
    derivative_values = {
        "D_t": parent_jet.gradient[0],
        "D_p": parent_jet.gradient[1],
        "dp_b_dt": dp_dt,
        "dD_along_leaf_dt": along,
    }
    require(
        all(bool(value > 0) for value in derivative_values.values()),
        "same-leaf strict orientation",
    )
    derivative_audit = {
        "parent_t_domain": [qstr(parent_domain[0]), qstr(parent_domain[1])],
        "all_derivatives_positive": True,
        "strict_dyadic_lower_depths": {
            name: strict_dyadic_depth(value)
            for name, value in derivative_values.items()
        },
        "orientation":
            "increasing t is plus/HIT; decreasing t is minus/BYPASS",
        "D0_unique_on_frozen_initial_interval": True,
        "side_level_roots_unique_on_common_parent": True,
    }
    parent_payload = [
        "round138-local-slope4-parent-W-v1",
        coordinate_contract["source_core_id"],
        qstr(SOURCE_P_STAR),
        [qstr(value) for value in d0_root],
        [qstr(value) for value in b_enclosure],
        {
            label: [qstr(value) for value in side_roots[label]]
            for label in ("BYPASS", "HIT")
        },
    ]
    parent_id = "round138-local-slope4-parent-W:" + digest(parent_payload)
    common = {
        "local_parent_W_id": parent_id,
        "coordinate_contract": coordinate_contract,
        "fixed_p_star": qstr(SOURCE_P_STAR),
        "fixed_p_D0_locator_initial_interval": [
            qstr(ROOT_INITIAL_INTERVAL[0]),
            qstr(ROOT_INITIAL_INTERVAL[1]),
        ],
        "fixed_p_D0_bisection_count": D0_BISECTIONS,
        "fixed_p_D0_root_bracket": [qstr(d0_root[0]), qstr(d0_root[1])],
        "fixed_p_D0_root_bracket_width": qstr(d0_root[1] - d0_root[0]),
        "fixed_p_D0_unique": True,
        "b_star_definition":
            "asin(p_star)-(16/25)*asin(t_star), t_star the fixed-p D0 root",
        "b_star_is_one_interval_defined_implicit_exact_object": True,
        "b_star_fixed_dyadic_outer_bits": B_STAR_ENCLOSURE_BITS,
        "b_star_fixed_dyadic_outer": [
            qstr(b_enclosure[0]), qstr(b_enclosure[1])
        ],
        "side_shift": qstr(SHIFT),
        "side_shift_equation": "(4/25)^2*2^-128",
        "side_root_bisection_count": SIDE_BISECTIONS,
        "side_root_brackets": {
            label: [qstr(value) for value in side_roots[label]]
            for label in ("BYPASS", "HIT")
        },
        "strict_root_order": "BYPASS < D0 < HIT",
        "canonical_parent_t_domain": [
            qstr(parent_domain[0]), qstr(parent_domain[1])
        ],
        "same_leaf_derivative_audit": derivative_audit,
    }
    return common, d0_root, b_enclosure, side_roots, {
        "parent_domain": parent_domain,
        "parent_id": parent_id,
    }


def side_graph_square(
    source: Any,
    strip: tuple[Q, Q, Q, Q],
    label: str,
    d0_root: tuple[Q, Q],
    b_enclosure: tuple[Q, Q],
    side_root: tuple[Q, Q],
    parent: dict[str, Any],
) -> tuple[step1.Atom, dict[str, Any]]:
    expected = EXPECTED[label]
    inward = dyadic(INWARD_POWER)
    half_width = dyadic(GRAPH_HALF_WIDTH_POWER)
    if label == "BYPASS":
        t_center = side_root[1] + inward
    else:
        t_center = side_root[0] - inward
    center_p_ball = leaf_p_ball(t_center, t_center, b_enclosure)
    p_center = unique_nearest_dyadic(
        center_p_ball, P_CENTER_ROUNDING_BITS
    )
    t0, t1 = t_center - half_width, t_center + half_width
    p0, p1 = p_center - half_width, p_center + half_width
    graph_p0, graph_p1 = leaf_p_outer(t0, t1, b_enclosure)
    require(
        p0 < graph_p0 < graph_p1 < p1,
        f"{label} exact graph in rational square",
    )
    if label == "BYPASS":
        side_clearance = t0 - side_root[1]
        d0_clearance = d0_root[0] - t1
    else:
        side_clearance = side_root[0] - t1
        d0_clearance = t0 - d0_root[1]
    require(
        side_clearance > 0
        and d0_clearance > 0
        and parent["parent_domain"][0] < t0 < t1 < parent["parent_domain"][1],
        f"{label} graph between side root and D0",
    )
    graph_jet = third_tangency_jet(
        source,
        SECOND_OWNER,
        DESIGNATED_TANGENT_OWNER,
        t0,
        t1,
        graph_p0,
        graph_p1,
    )
    square_jet = third_tangency_jet(
        source,
        SECOND_OWNER,
        DESIGNATED_TANGENT_OWNER,
        t0,
        t1,
        p0,
        p1,
    )
    if label == "BYPASS":
        graph_margins = {
            "strict_minus": -graph_jet.value,
            "above_minus_SHIFT": graph_jet.value + aq(SHIFT),
        }
        square_margins = {
            "strict_minus": -square_jet.value,
            "above_minus_SHIFT": square_jet.value + aq(SHIFT),
        }
    else:
        graph_margins = {
            "strict_plus": graph_jet.value,
            "below_plus_SHIFT": aq(SHIFT) - graph_jet.value,
        }
        square_margins = {
            "strict_plus": square_jet.value,
            "below_plus_SHIFT": aq(SHIFT) - square_jet.value,
        }
    require(
        all(bool(value > 0) for value in graph_margins.values())
        and all(bool(value > 0) for value in square_margins.values()),
        f"{label} graph and square strict collar",
    )
    require(
        strip[0] < t0 < t1 < strip[1]
        and strip[2] < p0 < p1 < strip[3],
        f"{label} square inside selected Round116 strip",
    )
    atom = step1.Atom(
        SOURCE_CORE_INDEX,
        source,
        t0,
        t1,
        p0,
        p1,
        Q(0),
        Q(0),
        f"round138-verifier-{label.lower()}-same-slope4-graph-square",
    )
    source_box = {
        "side": label,
        "side_level_target_D": qstr(expected["target_sign"] * SHIFT),
        "side_root_bracket": [qstr(side_root[0]), qstr(side_root[1])],
        "inward_toward_D0_power": INWARD_POWER,
        "inward_toward_D0": qstr(inward),
        "exact_rational_t_center": qstr(t_center),
        "p_center_rounding_rule":
            "unique nearest multiple of 2^-4096 to the interval-defined leaf value",
        "p_center_rounding_bits": P_CENTER_ROUNDING_BITS,
        "exact_rational_p_center": qstr(p_center),
        "unique_dyadic_rounding_proved": True,
        "rational_square": {
            "t": [qstr(t0), qstr(t1)],
            "p": [qstr(p0), qstr(p1)],
            "s": ["0", "0"],
            "half_width_power": GRAPH_HALF_WIDTH_POWER,
            "half_width": qstr(half_width),
            "positive_area": True,
            "exact_area": qstr((t1 - t0) * (p1 - p0)),
        },
        "exact_leaf_graph": {
            "t_interval": [qstr(t0), qstr(t1)],
            "positive_t_length": qstr(t1 - t0),
            "p_interval_outer_is_not_serialized_precision_dependent": True,
            "strictly_inside_rational_square": True,
            "strictly_between_side_root_and_D0": True,
            "D_collar": "-SHIFT<D<0" if label == "BYPASS" else "0<D<SHIFT",
            "D_collar_strict": True,
        },
        "strict_margin_dyadic_depths": {
            "graph_p_square_left":
                strict_dyadic_depth(aq(graph_p0 - p0)),
            "graph_p_square_right":
                strict_dyadic_depth(aq(p1 - graph_p1)),
            "side_root_t_clearance":
                strict_dyadic_depth(aq(side_clearance)),
            "D0_root_t_clearance":
                strict_dyadic_depth(aq(d0_clearance)),
            **{
                f"graph_D_{name}": strict_dyadic_depth(value)
                for name, value in graph_margins.items()
            },
            **{
                f"square_D_{name}": strict_dyadic_depth(value)
                for name, value in square_margins.items()
            },
        },
        "same_local_parent_W_id": parent["parent_id"],
        "same_implicit_b_star_used": True,
        "not_a_fixed_p_box": True,
    }
    return atom, source_box


def full_radius4_candidate_audit(
    state: dict[str, Any],
    current_target: str,
    selected_owner: dict[str, Any],
    ledger: StableMarginLedger,
    collision_index: int,
) -> dict[str, Any]:
    qx, qy, ux, uy, s = (
        state["contact_x"],
        state["contact_y"],
        state["outgoing_x"],
        state["outgoing_y"],
        state["s"],
    )
    candidates = tuple(charge.candidate_ids_around(current_target))
    require(
        len(candidates) == 161 and len(set(candidates)) == 161,
        "full radius-four candidate universe",
    )
    future: list[tuple[str, arb]] = []
    histogram: Counter[str] = Counter()
    decision_depths: list[int] = []
    for candidate_id in candidates:
        center_x, center_y = time3.time2_cert.target_center(candidate_id, s)
        dx, dy = center_x - qx, center_y - qy
        ell = ux * dx + uy * dy
        transverse = -uy * dx + ux * dy
        radius = aq(time3.time2_cert.first_hit.RADIUS[candidate_id[0]])
        discriminant = radius * radius - transverse * transverse
        witness = {
            "collision_index": collision_index,
            "candidate_id": candidate_id,
        }
        if bool(discriminant < 0):
            histogram["no_real_intersection"] += 1
            decision_depths.append(
                ledger.observe(
                    "full_radius4_candidate_miss_discriminant",
                    -discriminant,
                    witness,
                )
            )
            continue
        require(bool(discriminant > 0), "full candidate discriminant strict")
        radical = discriminant.sqrt()
        near, far = ell - radical, ell + radical
        if bool(far < 0):
            histogram["intersection_strictly_behind"] += 1
            decision_depths.append(
                ledger.observe(
                    "full_radius4_candidate_behind_far_root",
                    -far,
                    witness,
                )
            )
            continue
        require(bool(near > 0), "full candidate near root strict")
        histogram["strict_future_near_root"] += 1
        decision_depths.append(
            ledger.observe(
                "full_radius4_candidate_future_root_positive",
                near,
                witness,
            )
        )
        future.append((candidate_id, near))
    winners = [
        (candidate_id, root)
        for candidate_id, root in future
        if all(
            candidate_id == other_id or bool(root < other_root)
            for other_id, other_root in future
        )
    ]
    require(
        len(winners) == 1
        and winners[0][0] == selected_owner["selected_target_id"],
        "retained winner equals full radius-four winner",
    )
    winner_id, winner_root = winners[0]
    gap_depths = [
        ledger.observe(
            "full_radius4_winner_pairwise_root_gap",
            other_root - winner_root,
            {
                "collision_index": collision_index,
                "winner_id": winner_id,
                "competitor_id": other_id,
            },
        )
        for other_id, other_root in future
        if other_id != winner_id
    ]
    require(
        sum(histogram.values()) == len(candidates),
        "full candidate classification census",
    )
    return {
        "radius_in_lattice_cells": 4,
        "full_candidate_count": len(candidates),
        "candidate_classification_histogram": dict(sorted(histogram.items())),
        "minimum_candidate_decision_margin_dyadic_depth":
            max(decision_depths),
        "minimum_winner_gap_dyadic_depth":
            max(gap_depths) if gap_depths else None,
        "selected_target_matches_retained_search": True,
    }


def replay_side(
    label: str,
    atom: step1.Atom,
    parent_id: str,
) -> tuple[list[dict[str, Any]], dict[str, Any], StableMarginLedger]:
    expected = EXPECTED[label]
    return_depth = expected["return_depth"]
    cores = tuple(core_cert.physical_cores())
    pair_index, pattern_index, registry_sha = component_cert.key_index_tables()
    require(
        registry_sha == OFFICIAL_REGISTRY_STREAM_SHA256,
        "official registry replay digest",
    )
    state = initial_state(atom)
    current_target = SOURCE_ABSOLUTE_OWNER
    previous_cosine = (1 - state["p"] * state["p"]).sqrt()
    ledger = StableMarginLedger()
    rows: list[dict[str, Any]] = []
    retained_histogram: Counter[int] = Counter()
    full_histogram: Counter[int] = Counter()
    candidate_totals: Counter[str] = Counter()
    full_candidate_totals: Counter[str] = Counter()
    homogeneity_histogram: Counter[str] = Counter()
    incidence_histogram: Counter[int] = Counter()
    for collision_index in range(1, return_depth + 1):
        owner, candidate_audit = complete_owner(
            state,
            current_target,
            ledger,
            collision_index,
        )
        full_candidate_audit = full_radius4_candidate_audit(
            state,
            current_target,
            owner,
            ledger,
            collision_index,
        )
        word, word_error = translation_normalized_official_word(
            state,
            current_target,
            owner,
            pair_index,
            pattern_index,
        )
        require(
            word is not None and word_error is None,
            f"{label} official word {collision_index}:{word_error}",
        )
        classification, destination, witnesses = time3.core_classification(
            owner, cores
        )
        require(
            classification in {
                "SURVIVE_THROUGH_3_INNER",
                "RETURN_AT_3_INNER",
            },
            f"{label} C24 classification",
        )
        if collision_index < return_depth:
            require(
                classification == "SURVIVE_THROUGH_3_INNER"
                and destination is None,
                f"{label} premature C24 return",
            )
        else:
            require(
                classification == "RETURN_AT_3_INNER"
                and destination == expected["destination_core_id"]
                and owner["selected_target_id"] == expected["terminal_target"],
                f"{label} terminal C24 return",
            )
        core_depth = core_margin(
            owner,
            classification,
            destination,
            cores,
            ledger,
        )
        homogeneity_label, homogeneity_audit = generic_homogeneity_label(
            collision_index, owner["cosine"], ledger
        )
        source_rank = capped_reciprocal_cosine_rank(
            previous_cosine,
            ledger,
            collision_index,
            "source",
        )
        target_rank = capped_reciprocal_cosine_rank(
            owner["cosine"],
            ledger,
            collision_index,
            "target",
        )
        incidence_rank = max(14, source_rank, target_rank)
        next_state = time3.second_outgoing_state(atom, state, owner)
        require(next_state is not None, f"{label} outgoing reconstruction")
        outgoing_chart_depth = chart_margin(next_state, ledger)
        row_base = {
            "side": label,
            "collision_index": collision_index,
            "incoming_absolute_owner_id": current_target,
            "incoming_chart": state["chart"],
            "selected_absolute_owner_id": owner["selected_target_id"],
            "complete_candidate_audit": candidate_audit,
            "full_radius4_candidate_audit": full_candidate_audit,
            "official_word_key": compact_key(word["key"]),
            "ordered_clean_wall_record": word["ordered_clean_wall_record"],
            "relative_frozen_target_id": word["relative_frozen_target_id"],
            "absolute_lattice_translation_removed":
                word["absolute_lattice_translation_removed"],
            "C24_classification": classification,
            "destination_core_id": destination,
            "C24_core_witness_count": len(witnesses),
            "C24_minimum_inside_or_exclusion_margin_dyadic_depth": core_depth,
            **homogeneity_audit,
            "source_capped_reciprocal_cosine_rank": source_rank,
            "target_capped_reciprocal_cosine_rank": target_rank,
            "incidence_rank_B": incidence_rank,
            "incidence_rank_rule": (
                "max(14,ceil_log2(1/c_source),ceil_log2(1/c_target)) "
                "with whole-square strict dyadic comparisons"
            ),
            "outgoing_chart": next_state["chart"],
            "outgoing_chart_margin_dyadic_depth": outgoing_chart_depth,
        }
        rows.append(with_hash(row_base))
        retained = candidate_audit["retained_candidate_count"]
        retained_histogram[retained] += 1
        full_count = full_candidate_audit["full_candidate_count"]
        full_histogram[full_count] += 1
        for key, count in candidate_audit[
            "candidate_classification_histogram"
        ].items():
            candidate_totals[key] += count
        for key, count in full_candidate_audit[
            "candidate_classification_histogram"
        ].items():
            full_candidate_totals[key] += count
        homogeneity_histogram[homogeneity_label] += 1
        incidence_histogram[incidence_rank] += 1
        state = next_state
        current_target = owner["selected_target_id"]
        previous_cosine = owner["cosine"]

    owners = [row["selected_absolute_owner_id"] for row in rows]
    require(
        owners[:3]
        == [EXPECTED_SOURCE_TARGET, SECOND_OWNER, expected["third_owner"]],
        f"{label} common prefix and side third owner",
    )
    official_ids = [
        row["official_word_key"]["official_word_key_id"] for row in rows
    ]
    official_sequence_sha = digest(official_ids)
    unique_official_ids = sorted(set(official_ids))
    require(
        len(rows) == return_depth
        and official_sequence_sha == expected["official_sequence_sha256"]
        and len(unique_official_ids)
        == expected["unique_official_word_key_count"],
        f"{label} path census and digest",
    )
    require(
        sum(retained_histogram.values()) == return_depth
        and set(retained_histogram).issubset({55, 57})
        and sum(full_histogram.values()) == return_depth
        and set(full_histogram) == {161},
        f"{label} retained/full radius-four candidate census",
    )
    require(
        rows[-1]["destination_core_id"] == expected["destination_core_id"]
        and all(
            row["destination_core_id"] is None for row in rows[:-1]
        ),
        f"{label} first return",
    )
    word_cell_payload = [
        "round138-local-return-word-cell-v1",
        parent_id,
        label,
        step1.core_id(atom.source_core),
        return_depth,
        official_sequence_sha,
        expected["destination_core_id"],
        [
            qstr(atom.t0),
            qstr(atom.t1),
            qstr(atom.p0),
            qstr(atom.p1),
        ],
    ]
    word_cell_id = (
        "round138-local-return-word-cell:" + digest(word_cell_payload)
    )
    summary = {
        "side": label,
        "same_local_parent_W_id": parent_id,
        "local_return_word_cell_id": word_cell_id,
        "local_return_word_cell_is_not_a_global_Round35_short_cell": True,
        "source_core_id": step1.core_id(atom.source_core),
        "first_return_depth": return_depth,
        "preterminal_strict_nonreturn_collision_count": return_depth - 1,
        "terminal_strict_return_collision_count": 1,
        "terminal_absolute_target": expected["terminal_target"],
        "destination_core_id": expected["destination_core_id"],
        "collision_row_count": len(rows),
        "collision_rows_sha256": digest(rows),
        "official_word_key_occurrence_count": len(official_ids),
        "official_word_key_sequence_sha256": official_sequence_sha,
        "unique_official_word_key_id_count": len(unique_official_ids),
        "sorted_unique_official_word_key_ids_sha256":
            digest(unique_official_ids),
        "official_word_prefix_ordinals": [
            row["official_word_key"]["ordinal_zero_based"]
            for row in rows[:3]
        ],
        "retained_candidate_count_histogram": {
            str(key): value
            for key, value in sorted(retained_histogram.items())
        },
        "retained_candidate_root_test_count": sum(
            key * count for key, count in retained_histogram.items()
        ),
        "retained_candidate_classification_totals":
            dict(sorted(candidate_totals.items())),
        "full_radius4_candidate_count_histogram": {
            str(key): value
            for key, value in sorted(full_histogram.items())
        },
        "full_radius4_candidate_root_test_count": sum(
            key * count for key, count in full_histogram.items()
        ),
        "full_radius4_candidate_classification_totals":
            dict(sorted(full_candidate_totals.items())),
        "homogeneity_label_histogram":
            dict(sorted(homogeneity_histogram.items())),
        "incidence_rank_histogram": {
            str(key): value
            for key, value in sorted(incidence_histogram.items())
        },
        "maximum_incidence_rank": max(incidence_histogram),
        "all_collision_candidate_searches_complete": True,
        "all_official_word_keys_rebuilt": True,
        "all_homogeneity_labels_whole_square_isolated": True,
        "all_incidence_ranks_whole_square_constant": True,
        "first_return_to_C24_strictly_certified": True,
    }
    return rows, summary, ledger


def primitive_free_typed_crosswalk(
    round132_result: dict[str, Any],
    parent_id: str,
) -> dict[str, Any]:
    translated_label = ["G", "W[0,-1]", 1, "W[0,-2]", -1]
    rows = round132_result["occurrence_face_record_rows"]
    matches = [
        row for row in rows
        if row["global_physical_label"] == translated_label
    ]
    require(
        len(rows) == 64 and len(matches) == 1,
        "unique Round132 translated typed candidate",
    )
    match = matches[0]
    values = match["canonical_Round67_source_field_values"]
    require(
        match["occurrence_record_id"]
        == "round132-occurrence-record:"
        "4fea21fa8bb8290b15f0f68650a02b373fb072bb520729107c344b4592ef01ab"
        and match["immutable_global_occurrence_face_seed_id"]
        == "physical-moving-occurrence-face-seed:"
        "bfe49bc96e1d102432553fec6f61761ed65c61726056b914c1a37c6777aa5ca0",
        "unique Round132 typed candidate IDs",
    )
    require(
        values["return_component"] is None
        and values["owner_key"] is None
        and values["rank_zero_component"] is None
        and match["Round67_owner_map_q_j_materialized"] is False,
        "Round132 frontier remains null",
    )
    face_time_offset = match["selected_all_scale_germ_row"][
        "face_time_collision_offset"
    ]
    suffix_offsets = match["collision_offset_to_common_carrier"]
    require(
        face_time_offset == 1
        and suffix_offsets == {"hit": 1, "miss": 0},
        "Round132 event-time and suffix offsets",
    )
    global_insertion_time = 2 + face_time_offset
    require(
        global_insertion_time == 3
        and global_insertion_time
        < min(
            EXPECTED["BYPASS"]["return_depth"],
            EXPECTED["HIT"]["return_depth"],
        ),
        "global insertion time precedes both returns",
    )
    signature_payload = [
        "round138-primitive-free-local-physical-event-signature-v1",
        parent_id,
        {
            "current_absolute_owner": SECOND_OWNER,
            "tangent_absolute_target": DESIGNATED_TANGENT_OWNER,
            "bypass_absolute_target": EXPECTED["BYPASS"]["third_owner"],
            "lattice_translation_removed": [0, 1],
            "translated_typed_label": translated_label,
        },
    ]
    return {
        "primitive_free_local_physical_event_signature_id":
            "round138-primitive-free-local-event:" + digest(signature_payload),
        "signature_fields": {
            "local_event_current_absolute_owner": SECOND_OWNER,
            "local_event_source_obstacle": "G",
            "tangent_absolute_target": DESIGNATED_TANGENT_OWNER,
            "bypass_absolute_target": EXPECTED["BYPASS"]["third_owner"],
            "integer_lattice_translation_removed": [0, 1],
            "translated_tangent_target": "W[0,-1]",
            "translated_bypass_target": "W[0,-2]",
            "plus_HIT_sign": 1,
            "minus_BYPASS_sign": -1,
            "translated_Round132_global_physical_label": translated_label,
        },
        "complete_Round132_candidate_row_count": len(rows),
        "primitive_free_typed_candidate_match_count": len(matches),
        "unique_Round132_typed_candidate": {
            "occurrence_record_id": match["occurrence_record_id"],
            "occurrence_id": match["occurrence_id"],
            "immutable_global_occurrence_face_seed_id":
                match["immutable_global_occurrence_face_seed_id"],
            "event_signature": values["event_signature"],
            "occurrence_word_cell_id":
                values["word_cell"]["occurrence_word_cell_id"],
            "candidate_insertion_time": values["insertion_time"],
            "candidate_collision_index": values["collision_index"],
        },
        "crosswalk_scope":
            "primitive-free translated local physical-event type plus exact collision timeline",
        "explicit_C24_collision_timeline": [
            {
                "time": 0,
                "state":
                    "outgoing source-core state on W[0,0], chart W:E",
            },
            {
                "time": 1,
                "collision_target": EXPECTED_SOURCE_TARGET,
            },
            {
                "time": 2,
                "collision_target": SECOND_OWNER,
                "role": "current local event state",
            },
            {
                "time": global_insertion_time,
                "role": "Round132 typed face insertion",
                "face_time_collision_offset_from_current_event_state":
                    face_time_offset,
            },
        ],
        "global_insertion_time_j": global_insertion_time,
        "local_to_Round132_global_insertion_time_map_materialized": True,
        "global_insertion_time_precedes_both_local_returns": True,
        "collision_offset_to_common_carrier": suffix_offsets,
        "collision_offset_to_common_carrier_semantics":
            "hit/miss suffix alignment after the occurrence face; not insertion time j",
        "candidate_primitive_key_adopted": False,
        "candidate_restriction_id_adopted": False,
        "candidate_root_coordinate_adopted": False,
        "local_to_Round132_insertion_time_map_materialized": True,
        "local_to_Round132_global_restriction_map_materialized": False,
        "local_event_collision_index_is_three": True,
        "Round132_candidate_insertion_time_is_one": True,
        "Round132_candidate_insertion_time_is_face_local_offset_one": True,
    }


STRICT_NONPROMOTION = {
    "same_leaf_two_sided_local_return_frontier_materialized": True,
    "primitive_free_Round132_typed_candidate_crosswalk_materialized": True,
    "local_to_Round132_insertion_time_map_materialized": True,
    "global_insertion_time_j": 3,
    "global_Round35_restriction_materialized": False,
    "global_Round35_restriction_id": None,
    "global_connected_component_rank_materialized": False,
    "global_connected_component_rank": None,
    "global_least_dyadic_basis_component_rank_materialized": False,
    "global_short_cell_id_materialized": False,
    "global_short_cell_id": None,
    "image_recut_materialized": False,
    "image_recut_id": None,
    "return_component_materialized": False,
    "return_component_id": None,
    "Round50_complete_primitive_fibre_materialized": False,
    "Round50_owner_key_count": 0,
    "Round54_t54_token_count": 0,
    "Round54_pi54_to_Round50_map_count": 0,
    "Round67_owned_Omega_j_record_count": 0,
    "Round67_q_j_output_count": 0,
    "owner_law_positive_mass": "NOT_CERTIFIED",
    "global_gate5_maturity": "10/18",
    "global_complete_18_field_block_count": 0,
    "complete_18_field_block_count": 0,
    "Gate5": "NOT_CERTIFIED",
    "CM2": "NO-GO_FOR_CLAIM",
}

STRICT_NONCLAIMS = [
    "the two graph segments are on one local implicit slope-four leaf, not a global arbitrary-return family",
    "the rational squares certify local return cylinders but are not global R_n components",
    "the two local return word-cell IDs are not Round35 short-cell IDs",
    "the primitive-free typed candidate match does not adopt the Round132 primitive or restriction",
    "global insertion time j=3 uses two prefix collisions plus the Round132 face-local offset one; the suffix offsets {hit:1,miss:0} are not j",
    "no global restriction, component rank, least dyadic basis rank, short cell or image recut is materialized",
    "the local return word-cells are not Round54 t54 cells: the plus D-to-zero limit crosses infinitely many homogeneity strips and may have N_acc or d=0",
    "the minus square also lacks a D0-root-adjacent fixed full-word/no-extra-cut theorem required for t54",
    "Round54 t54 and pi54-to-Round50 counts therefore remain zero",
    "no return component, owner key, t54 token, Omega_j record or q_j output is materialized",
    "no Gate5 field, Gate5 block or CM2 claim is promoted",
]


def build_expected(
    precision_bits: int,
    producer_sha256: str,
) -> dict[str, Any]:
    require(
        type(precision_bits) is int
        and precision_bits >= MINIMUM_PRECISION_BITS,
        "verifier precision below 12288",
    )
    require(
        type(producer_sha256) is str and len(producer_sha256) == 64,
        "producer SHA available",
    )
    ctx.prec = precision_bits
    closed = validate_dependencies()
    round116.init_worker(precision_bits)
    nested_closed = round136.validate_dependencies()
    source, face, selected_link, strip = round136.selected_corrected_objects(
        nested_closed
    )
    common, d0_root, b_enclosure, side_roots, parent = (
        common_leaf_geometry(source)
    )

    graph_rows: list[dict[str, Any]] = []
    collision_rows: list[dict[str, Any]] = []
    return_summaries: list[dict[str, Any]] = []
    margin_ledgers: dict[str, Any] = {}
    local_word_cell_rows: list[dict[str, Any]] = []
    for label in ("BYPASS", "HIT"):
        atom, graph_row = side_graph_square(
            source,
            strip,
            label,
            d0_root,
            b_enclosure,
            side_roots[label],
            parent,
        )
        rows, summary, ledger = replay_side(
            label, atom, parent["parent_id"]
        )
        graph_rows.append(with_hash(graph_row))
        collision_rows.extend(rows)
        return_summaries.append(summary)
        margin_ledgers[label] = ledger.public()
        local_word_cell_rows.append(with_hash({
            "side": label,
            "local_return_word_cell_id":
                summary["local_return_word_cell_id"],
            "local_parent_W_id": parent["parent_id"],
            "source_core_id": summary["source_core_id"],
            "return_depth": summary["first_return_depth"],
            "official_word_key_sequence_sha256":
                summary["official_word_key_sequence_sha256"],
            "destination_core_id": summary["destination_core_id"],
            "local_only": True,
            "global_Round35_short_cell_id": None,
            "global_component_rank": None,
        }))

    require(
        len(graph_rows) == 2
        and len(return_summaries) == 2
        and len(collision_rows) == 647
        and len(local_word_cell_rows) == 2,
        "two-sided row census",
    )
    require(
        len({row["local_parent_W_id"] for row in local_word_cell_rows}) == 1
        and len({
            row["local_return_word_cell_id"] for row in local_word_cell_rows
        }) == 2,
        "one parent and two local return word-cells",
    )
    typed_crosswalk = primitive_free_typed_crosswalk(
        closed[ROUND132.name],
        parent["parent_id"],
    )
    r135 = closed[ROUND135.name]
    r136 = closed[ROUND136.name]
    require(
        (
            r135["physical_F10_and_cemetery_separation_contract"][
                "physical_F10_count"
            ] == 0
            if "physical_F10_and_cemetery_separation_contract" in r135
            else r135["count_ledger"]["physical_F10_count"] == 0
        ),
        "Round135 physical F10 frontier",
    )
    require(
        r136["strict_nonpromotion"][
            "global_least_dyadic_basis_component_rank_materialized"
        ]
        is False,
        "Round136 component-rank frontier",
    )

    common_leaf_row = with_hash(common)
    result = {
        "status":
            "CERTIFIED_SAME_SLOPE4_TWO_SIDED_POSITIVE_WIDTH_LOCAL_RETURNS",
        "minimum_certified_precision_bits": MINIMUM_PRECISION_BITS,
        "precision_invariance_contract": {
            "runtime_precision_is_not_serialized": True,
            "minimum_runtime_precision_bits": MINIMUM_PRECISION_BITS,
            "all_serialized_centers_are_fixed_rational_dyadics": True,
            "p_center_rounding_bits": P_CENTER_ROUNDING_BITS,
            "p_center_unique_rounding_proved_on_interval_defined_leaf": True,
            "expected_identical_artifact_at_12288_and_16384_bits": True,
        },
        "provenance": {
            "producer_sha256": producer_sha256,
            "direct_dependency_sha256": dict(sorted(PINS.items())),
            "nested_Round136_dependency_sha256":
                dict(sorted(round136.PINS.items())),
            "append_only": True,
            "old_artifacts_modified": False,
            "temporary_support_imported": False,
            "historical_Round87_physicality_used": False,
        },
        "corrected_rank3_source_contract": {
            "selected_Round116_face_id": round136.SELECTED_FACE_ID,
            "selected_face_branch": [
                face["source_core_index"],
                face["second_selected_target_id"],
                face["third_candidate_id"],
                face["signed_transverse_tangency_factor_sign"],
            ],
            "selected_link_rank": round136.SELECTED_LINK_RANK,
            "selected_link_type": selected_link["link_type"],
            "selected_strip_index_zero_based":
                round136.SELECTED_STRIP_INDEX,
            "selected_strip_count": 256,
            "source_square_rows_strictly_inside_selected_strip": True,
        },
        "common_same_slope4_parent_leaf": common_leaf_row,
        "side_graph_square_rows": graph_rows,
        "side_graph_square_rows_sha256": digest(graph_rows),
        "two_local_return_word_cell_rows": local_word_cell_rows,
        "two_local_return_word_cell_rows_sha256":
            digest(local_word_cell_rows),
        "return_summaries": return_summaries,
        "return_summaries_sha256": digest(return_summaries),
        "collision_rows": collision_rows,
        "collision_rows_sha256": digest(collision_rows),
        "strict_margin_ledgers": margin_ledgers,
        "primitive_free_Round132_typed_candidate_crosswalk":
            typed_crosswalk,
        "strict_local_scope": {
            "one_common_source_sheet": EXPECTED_SOURCE_TARGET,
            "one_common_source_chart": EXPECTED_SOURCE_CHART,
            "one_common_local_parent_W_root": True,
            "one_common_implicit_b_star": True,
            "positive_width_exact_leaf_graph_segment_count": 2,
            "whole_rational_square_return_cylinder_count": 2,
            "local_return_word_cell_count": 2,
            "BYPASS_first_return_depth": 298,
            "HIT_first_return_depth": 349,
            "BYPASS_and_HIT_are_not_fixed_p_boxes": True,
        },
        "strict_nonpromotion": dict(STRICT_NONPROMOTION),
        "historical_global_status_preserved": {
            "Round132_owner_key_count":
                closed[ROUND132.name]["count_ledger"]["owner_key_count"],
            "Round132_q_j_output_count":
                closed[ROUND132.name]["count_ledger"][
                    "Round67_owned_Omega_j_record_count"
                ],
            "Round135_gate5_global_maturity":
                r135["gate5_global_maturity"],
            "Round135_global_complete_18_field_block_count":
                r135["global_complete_18_field_block_count"],
            "Round135_cm2_verdict": r135["cm2_verdict"],
            "Round136_global_component_rank_materialized":
                r136["strict_nonpromotion"][
                    "global_least_dyadic_basis_component_rank_materialized"
                ],
            "no_historical_or_global_status_upgraded": True,
        },
        "count_ledger": {
            "common_local_parent_W_root_count": 1,
            "implicit_b_star_count": 1,
            "side_level_root_count": 2,
            "positive_width_exact_leaf_graph_segment_count": 2,
            "positive_area_rational_square_count": 2,
            "local_return_word_cell_count": 2,
            "collision_row_count": len(collision_rows),
            "BYPASS_collision_row_count": 298,
            "HIT_collision_row_count": 349,
            "preterminal_strict_nonreturn_collision_count":
                (298 - 1) + (349 - 1),
            "terminal_strict_return_collision_count": 2,
            "official_word_key_occurrence_count": len(collision_rows),
            "primitive_free_Round132_typed_candidate_match_count": 1,
            "global_Round35_restriction_count": 0,
            "global_component_rank_count": 0,
            "global_short_cell_count": 0,
            "image_recut_count": 0,
            "Round50_owner_key_count": 0,
            "Round54_t54_token_count": 0,
            "Round54_pi54_to_Round50_map_count": 0,
            "Round67_owned_Omega_j_record_count": 0,
            "Round67_q_j_output_count": 0,
            "global_complete_18_field_block_count": 0,
        },
        "strict_nonclaims": list(STRICT_NONCLAIMS),
    }
    require(
        result["historical_global_status_preserved"][
            "Round132_owner_key_count"
        ] == 0
        and result["historical_global_status_preserved"][
            "Round132_q_j_output_count"
        ] == 0,
        "historical zero owner/q_j counts",
    )
    return json.loads(json.dumps(result, sort_keys=True))


def validate_row_closures(result: dict[str, Any]) -> None:
    common = result["common_same_slope4_parent_leaf"]
    common_body = dict(common)
    common_hash = common_body.pop("row_sha256", None)
    require(common_hash == digest(common_body), "common leaf row closure")

    groups = {
        "side_graph_square_rows": 2,
        "two_local_return_word_cell_rows": 2,
        "collision_rows": 647,
    }
    for name, expected_count in groups.items():
        rows = result[name]
        require(type(rows) is list and len(rows) == expected_count, f"rows:{name}")
        require(result[f"{name}_sha256"] == digest(rows), f"group closure:{name}")
        row_hashes: list[str] = []
        for row in rows:
            require(type(row) is dict, f"row object:{name}")
            body = dict(row)
            row_hash = body.pop("row_sha256", None)
            require(row_hash == digest(body), f"row closure:{name}")
            row_hashes.append(row_hash)
        require(
            len(row_hashes) == len(set(row_hashes)),
            f"unique row closures:{name}",
        )

    summaries = result["return_summaries"]
    require(
        type(summaries) is list
        and len(summaries) == 2
        and result["return_summaries_sha256"] == digest(summaries),
        "return summary closure",
    )
    collision_rows = result["collision_rows"]
    bypass_rows = collision_rows[:298]
    hit_rows = collision_rows[298:]
    require(
        [row["side"] for row in bypass_rows] == ["BYPASS"] * 298
        and [row["collision_index"] for row in bypass_rows]
        == list(range(1, 299)),
        "BYPASS collision sequence",
    )
    require(
        [row["side"] for row in hit_rows] == ["HIT"] * 349
        and [row["collision_index"] for row in hit_rows]
        == list(range(1, 350)),
        "HIT collision sequence",
    )
    require(
        summaries[0]["collision_rows_sha256"] == digest(bypass_rows)
        and summaries[1]["collision_rows_sha256"] == digest(hit_rows),
        "per-side collision group closure",
    )
    for row in collision_rows:
        key = row["official_word_key"]
        require(
            key["registry_row_sha256"] == digest(key["registry_row"]),
            "registry row closure",
        )
        require(
            key["official_word_key_id"]
            == f"gate5-word:{key['ordinal_zero_based']:06d}:"
            f"{key['registry_row_sha256']}",
            "official word ID closure",
        )


def evaluate_document(document: dict[str, Any], expected: dict[str, Any]) -> None:
    require(
        set(document) == {"schema", "result", "result_sha256"},
        "closed certificate envelope",
    )
    require(document["schema"] == CERTIFICATE_SCHEMA, "certificate schema")
    result = document["result"]
    require(type(result) is dict, "certificate result object")
    require(document["result_sha256"] == digest(result), "certificate result digest")
    validate_row_closures(result)
    require(result == expected, "independent complete result reconstruction equality")
    require(
        CERTIFICATE_RESULT_SHA256 is not None
        and document["result_sha256"] == CERTIFICATE_RESULT_SHA256,
        "frozen certificate result pin",
    )


def resign(document: dict[str, Any]) -> None:
    document["result_sha256"] = digest(document["result"])


def set_path(
    document: dict[str, Any],
    path: tuple[Any, ...],
    value: Any,
) -> None:
    target: Any = document
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    resign(document)


def reclose_group_row(
    document: dict[str, Any],
    group: str,
    index: int,
) -> None:
    result = document["result"]
    row = result[group][index]
    body = {key: value for key, value in row.items() if key != "row_sha256"}
    row.clear()
    row.update(body)
    row["row_sha256"] = digest(body)
    result[f"{group}_sha256"] = digest(result[group])
    if group == "collision_rows":
        result["return_summaries"][0]["collision_rows_sha256"] = digest(
            result[group][:298]
        )
        result["return_summaries"][1]["collision_rows_sha256"] = digest(
            result[group][298:]
        )
        result["return_summaries_sha256"] = digest(result["return_summaries"])
    resign(document)


def reclose_common(document: dict[str, Any]) -> None:
    row = document["result"]["common_same_slope4_parent_leaf"]
    body = {key: value for key, value in row.items() if key != "row_sha256"}
    row.clear()
    row.update(body)
    row["row_sha256"] = digest(body)
    resign(document)


def reclose_summaries(document: dict[str, Any]) -> None:
    result = document["result"]
    result["return_summaries_sha256"] = digest(result["return_summaries"])
    resign(document)


def semantic_mutations(
    certificate: dict[str, Any],
    expected: dict[str, Any],
) -> list[str]:
    mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] = []

    def simple(label: str, path: tuple[Any, ...], value: Any) -> None:
        mutations.append(
            (label, lambda document, p=path, v=value: set_path(document, p, v))
        )

    mutations.append(
        (
            "certificate schema altered",
            lambda document: document.__setitem__("schema", "bad"),
        )
    )
    simple(
        "minimum precision weakened",
        ("result", "minimum_certified_precision_bits"),
        8192,
    )
    simple(
        "runtime precision serialization enabled",
        (
            "result",
            "precision_invariance_contract",
            "runtime_precision_is_not_serialized",
        ),
        False,
    )
    simple(
        "p rounding bits altered",
        (
            "result",
            "precision_invariance_contract",
            "p_center_rounding_bits",
        ),
        4095,
    )
    simple(
        "precision invariance erased",
        (
            "result",
            "precision_invariance_contract",
            "expected_identical_artifact_at_12288_and_16384_bits",
        ),
        False,
    )
    simple(
        "producer pin altered",
        ("result", "provenance", "producer_sha256"),
        "0" * 64,
    )
    simple(
        "Round136 verifier pin altered",
        (
            "result",
            "provenance",
            "direct_dependency_sha256",
            ROUND136_VERIFIER.name,
        ),
        "0" * 64,
    )
    simple(
        "historical Round87 enabled",
        ("result", "provenance", "historical_Round87_physicality_used"),
        True,
    )
    simple(
        "strip index altered",
        (
            "result",
            "corrected_rank3_source_contract",
            "selected_strip_index_zero_based",
        ),
        127,
    )
    simple(
        "source squares not inside strip",
        (
            "result",
            "corrected_rank3_source_contract",
            "source_square_rows_strictly_inside_selected_strip",
        ),
        False,
    )

    def mutate_common(
        label: str,
        path: tuple[Any, ...],
        value: Any,
    ) -> None:
        def action(document: dict[str, Any]) -> None:
            target: Any = document["result"]["common_same_slope4_parent_leaf"]
            for key in path[:-1]:
                target = target[key]
            target[path[-1]] = value
            reclose_common(document)
        mutations.append((label, action))

    mutate_common(
        "parent ID altered",
        ("local_parent_W_id",),
        "round138-local-slope4-parent-W:bad",
    )
    mutate_common(
        "D0 bisection count altered",
        ("fixed_p_D0_bisection_count",),
        4095,
    )
    mutate_common(
        "D0 uniqueness erased",
        ("fixed_p_D0_unique",),
        False,
    )
    mutate_common(
        "b star enclosure bits altered",
        ("b_star_fixed_dyadic_outer_bits",),
        4103,
    )
    mutate_common(
        "root order altered",
        ("strict_root_order",),
        "HIT < D0 < BYPASS",
    )
    mutate_common(
        "derivative positivity erased",
        ("same_leaf_derivative_audit", "all_derivatives_positive"),
        False,
    )
    mutate_common(
        "orientation reversed",
        ("same_leaf_derivative_audit", "orientation"),
        "decreasing t is plus/HIT",
    )

    for index, side in enumerate(("BYPASS", "HIT")):
        def mutate_graph(
            document: dict[str, Any],
            selected: int = index,
        ) -> None:
            row = document["result"]["side_graph_square_rows"][selected]
            row["exact_rational_p_center"] += "/1"
            reclose_group_row(document, "side_graph_square_rows", selected)
        mutations.append((f"{side} graph p center altered", mutate_graph))

        def erase_rounding(
            document: dict[str, Any],
            selected: int = index,
        ) -> None:
            row = document["result"]["side_graph_square_rows"][selected]
            row["unique_dyadic_rounding_proved"] = False
            reclose_group_row(document, "side_graph_square_rows", selected)
        mutations.append((f"{side} rounding proof erased", erase_rounding))

        def erase_graph_inside(
            document: dict[str, Any],
            selected: int = index,
        ) -> None:
            row = document["result"]["side_graph_square_rows"][selected]
            row["exact_leaf_graph"]["strictly_inside_rational_square"] = False
            reclose_group_row(document, "side_graph_square_rows", selected)
        mutations.append((f"{side} graph containment erased", erase_graph_inside))

        def promote_fixed_p(
            document: dict[str, Any],
            selected: int = index,
        ) -> None:
            row = document["result"]["side_graph_square_rows"][selected]
            row["not_a_fixed_p_box"] = False
            reclose_group_row(document, "side_graph_square_rows", selected)
        mutations.append((f"{side} graph mislabeled fixed-p", promote_fixed_p))

        def promote_word_cell(
            document: dict[str, Any],
            selected: int = index,
        ) -> None:
            row = document["result"]["two_local_return_word_cell_rows"][selected]
            row["global_Round35_short_cell_id"] = "round35-short-cell:invented"
            reclose_group_row(
                document,
                "two_local_return_word_cell_rows",
                selected,
            )
        mutations.append((f"{side} global word-cell invented", promote_word_cell))

        def alter_summary_depth(
            document: dict[str, Any],
            selected: int = index,
        ) -> None:
            document["result"]["return_summaries"][selected][
                "first_return_depth"
            ] -= 1
            reclose_summaries(document)
        mutations.append((f"{side} return depth altered", alter_summary_depth))

        def erase_full_search(
            document: dict[str, Any],
            selected: int = index,
        ) -> None:
            document["result"]["return_summaries"][selected][
                "all_collision_candidate_searches_complete"
            ] = False
            reclose_summaries(document)
        mutations.append((f"{side} candidate completeness erased", erase_full_search))

        def alter_full_count(
            document: dict[str, Any],
            selected: int = index,
        ) -> None:
            document["result"]["return_summaries"][selected][
                "full_radius4_candidate_count_histogram"
            ] = {"160": document["result"]["return_summaries"][selected][
                "collision_row_count"
            ]}
            reclose_summaries(document)
        mutations.append((f"{side} full radius count altered", alter_full_count))

    crosswalk = "primitive_free_Round132_typed_candidate_crosswalk"
    simple(
        "primitive-free signature altered",
        (
            "result",
            crosswalk,
            "primitive_free_local_physical_event_signature_id",
        ),
        "round138-primitive-free-local-event:bad",
    )
    simple(
        "typed candidate count altered",
        (
            "result",
            crosswalk,
            "primitive_free_typed_candidate_match_count",
        ),
        2,
    )
    simple(
        "global insertion time altered",
        ("result", crosswalk, "global_insertion_time_j"),
        1,
    )
    simple(
        "suffix offsets used as j",
        (
            "result",
            crosswalk,
            "collision_offset_to_common_carrier_semantics",
        ),
        "insertion time",
    )
    simple(
        "primitive key adopted",
        ("result", crosswalk, "candidate_primitive_key_adopted"),
        True,
    )
    simple(
        "restriction adopted",
        ("result", crosswalk, "candidate_restriction_id_adopted"),
        True,
    )
    simple(
        "global restriction map invented",
        (
            "result",
            crosswalk,
            "local_to_Round132_global_restriction_map_materialized",
        ),
        True,
    )

    nonpromotion_mutations = [
        ("global restriction invented", "global_Round35_restriction_id", "rn-restriction:invented"),
        ("component rank invented", "global_connected_component_rank", 0),
        ("short cell invented", "global_short_cell_id", "short-cell:invented"),
        ("image recut invented", "image_recut_id", "image-recut:invented"),
        ("return component invented", "return_component_id", "component:invented"),
        ("owner count invented", "Round50_owner_key_count", 1),
        ("t54 count invented", "Round54_t54_token_count", 1),
        ("pi54 count invented", "Round54_pi54_to_Round50_map_count", 1),
        ("Omega count invented", "Round67_owned_Omega_j_record_count", 1),
        ("q_j count invented", "Round67_q_j_output_count", 1),
        ("owner mass promoted", "owner_law_positive_mass", "CERTIFIED"),
        ("global maturity promoted", "global_gate5_maturity", "18/18"),
        ("global block invented", "global_complete_18_field_block_count", 1),
        ("Gate5 promoted", "Gate5", "CERTIFIED"),
        ("CM2 promoted", "CM2", "GO_FOR_CLAIM"),
    ]
    for label, key, value in nonpromotion_mutations:
        simple(label, ("result", "strict_nonpromotion", key), value)

    simple(
        "collision census altered",
        ("result", "count_ledger", "collision_row_count"),
        646,
    )
    simple(
        "preterminal census altered",
        (
            "result",
            "count_ledger",
            "preterminal_strict_nonreturn_collision_count",
        ),
        644,
    )
    simple(
        "owner census invented",
        ("result", "count_ledger", "Round50_owner_key_count"),
        1,
    )
    mutations.append(
        (
            "strict nonclaim deleted",
            lambda document: (
                document["result"]["strict_nonclaims"].pop(),
                resign(document),
            ),
        )
    )

    for index in (
        0,
        1,
        2,
        15,
        63,
        127,
        255,
        297,
        298,
        299,
        300,
        349,
        425,
        511,
        600,
        646,
    ):
        def mutate_owner(
            document: dict[str, Any],
            selected: int = index,
        ) -> None:
            document["result"]["collision_rows"][selected][
                "selected_absolute_owner_id"
            ] += "-tampered"
            reclose_group_row(document, "collision_rows", selected)
        mutations.append((f"collision owner altered:{index}", mutate_owner))

    for index in (0, 2, 297, 298, 300, 646):
        def mutate_full_audit(
            document: dict[str, Any],
            selected: int = index,
        ) -> None:
            document["result"]["collision_rows"][selected][
                "full_radius4_candidate_audit"
            ]["full_candidate_count"] = 160
            reclose_group_row(document, "collision_rows", selected)
        mutations.append((f"full radius audit altered:{index}", mutate_full_audit))

    rejected: list[str] = []
    for label, mutation in mutations:
        candidate = copy.deepcopy(certificate)
        mutation(candidate)
        try:
            evaluate_document(candidate, expected)
        except (
            VerificationError,
            KeyError,
            IndexError,
            TypeError,
            ValueError,
        ):
            rejected.append(label)
        else:
            raise VerificationError(f"semantic mutation accepted:{label}")
    require(len(rejected) == len(mutations), "all semantic mutations rejected")
    return rejected


def strict_json_attacks(
    certificate: dict[str, Any],
    expected: dict[str, Any],
) -> list[str]:
    raw = (
        json.dumps(
            certificate,
            sort_keys=True,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")
    attacks: list[tuple[str, bytes]] = []

    def add(label: str, payload: bytes) -> None:
        require(payload != raw, f"strict attack construction:{label}")
        attacks.append((label, payload))

    add(
        "duplicate top-level schema key",
        raw.replace(
            b'{\n  "result":',
            b'{\n  "schema": "duplicate",\n  "result":',
            1,
        ),
    )
    add(
        "duplicate nested status key",
        raw.replace(
            b'"status": "CERTIFIED_SAME_SLOPE4_TWO_SIDED_POSITIVE_WIDTH_LOCAL_RETURNS"',
            b'"status": "bad", "status": "CERTIFIED_SAME_SLOPE4_TWO_SIDED_POSITIVE_WIDTH_LOCAL_RETURNS"',
            1,
        ),
    )
    add(
        "duplicate collision index key",
        raw.replace(
            b'"collision_index": 1,',
            b'"collision_index": 0, "collision_index": 1,',
            1,
        ),
    )
    add(
        "floating collision count",
        raw.replace(b'"collision_row_count": 647', b'"collision_row_count": 647.0', 1),
    )
    add(
        "NaN constant",
        raw.replace(b'"collision_row_count": 647', b'"collision_row_count": NaN', 1),
    )
    add(
        "positive Infinity",
        raw.replace(
            b'"collision_row_count": 647',
            b'"collision_row_count": Infinity',
            1,
        ),
    )
    add(
        "negative Infinity",
        raw.replace(
            b'"collision_row_count": 647',
            b'"collision_row_count": -Infinity',
            1,
        ),
    )
    add("UTF-8 BOM", b"\xef\xbb\xbf" + raw)
    add("invalid UTF-8", raw[:10] + b"\xff" + raw[10:])
    add("top-level array", b"[]\n")
    add("top-level null", b"null\n")
    add("trailing second document", raw + b"{}\n")
    add(
        "oversized integer",
        raw.replace(
            b'"collision_row_count": 647',
            b'"collision_row_count": ' + b"9" * (MAX_INTEGER_DIGITS + 1),
            1,
        ),
    )
    add(
        "negative zero",
        raw.replace(b'"collision_row_count": 647', b'"collision_row_count": -0', 1),
    )
    add(
        "leading-zero integer",
        raw.replace(b'"collision_row_count": 647', b'"collision_row_count": 0647', 1),
    )
    add(
        "unpaired surrogate",
        raw.replace(
            b'"CERTIFIED_SAME_SLOPE4_TWO_SIDED_POSITIVE_WIDTH_LOCAL_RETURNS"',
            b'"\\ud800"',
            1,
        ),
    )
    extra_envelope = copy.deepcopy(certificate)
    extra_envelope["unknown"] = True
    add(
        "closed envelope extra key",
        (json.dumps(extra_envelope, sort_keys=True) + "\n").encode(),
    )
    extra_result = copy.deepcopy(certificate)
    extra_result["result"]["unknown"] = True
    resign(extra_result)
    add(
        "closed result extra key",
        (json.dumps(extra_result, sort_keys=True) + "\n").encode(),
    )
    stale = copy.deepcopy(certificate)
    stale["result"]["strict_nonpromotion"]["CM2"] = "GO_FOR_CLAIM"
    add(
        "stale outer digest",
        (json.dumps(stale, sort_keys=True) + "\n").encode(),
    )

    rejected: list[str] = []
    for label, payload in attacks:
        try:
            document = strict_json_bytes(payload, label)
            evaluate_document(document, expected)
        except (
            VerificationError,
            UnicodeError,
            KeyError,
            IndexError,
            TypeError,
            ValueError,
        ):
            rejected.append(label)
        else:
            raise VerificationError(f"strict JSON attack accepted:{label}")
    require(len(rejected) == len(attacks) == 19, "19 strict attacks rejected")
    return rejected


def regular_single_link(path: Path, label: str) -> None:
    require(path.is_file(), f"missing regular file:{label}")
    require(not path.is_symlink(), f"symlink file:{label}")
    metadata = path.lstat()
    require(stat.S_ISREG(metadata.st_mode), f"non-regular file:{label}")
    require(metadata.st_nlink == 1, f"hardlinked file:{label}")


def safe_input_path(path: Path) -> Path:
    require(CERTIFICATE_SHA256 is not None, "certificate pin not frozen")
    expanded = path.expanduser()
    regular_single_link(expanded, "certificate")
    require(
        expanded.stat().st_size <= MAX_CERTIFICATE_BYTES,
        "certificate exceeds size limit",
    )
    resolved = expanded.resolve()
    require(sha256(resolved) == CERTIFICATE_SHA256, "certificate byte pin")
    return resolved


def safe_output_path(path: Path, certificate_path: Path) -> Path:
    expanded = path.expanduser()
    protected = {
        VERIFIER.resolve(),
        PRODUCER.resolve(),
        CERTIFICATE.resolve(),
        certificate_path.resolve(),
        *((HERE / name).resolve() for name in PINS),
        *((HERE / name).resolve() for name in round136.PINS),
    }
    require(not expanded.is_symlink(), "output path must not be a symlink")
    require(not expanded.parent.is_symlink(), "output parent must not be a symlink")
    if expanded.exists():
        metadata = expanded.lstat()
        require(
            stat.S_ISREG(metadata.st_mode),
            "existing output must be a regular file",
        )
        require(
            metadata.st_nlink == 1,
            "existing output must not have multiple hardlinks",
        )
        for protected_path in protected:
            try:
                require(
                    not os.path.samefile(expanded, protected_path),
                    "output hardlinks a protected input",
                )
            except FileNotFoundError:
                pass
    resolved = expanded.resolve()
    require(resolved not in protected, "output must not overwrite an input")
    require(resolved.parent.is_dir(), "output parent directory")
    require(not resolved.parent.is_symlink(), "resolved output parent symlink")
    return resolved


def path_safety_self_tests(certificate_path: Path) -> list[str]:
    labels: list[str] = []

    def reject(label: str, action: Callable[[], Any]) -> None:
        try:
            action()
        except (VerificationError, OSError):
            labels.append(label)
        else:
            raise VerificationError(f"path safety attack accepted:{label}")

    with tempfile.TemporaryDirectory(prefix="cm2-r138-path-tests-") as name:
        root = Path(name)
        certificate_copy = root / "certificate.json"
        certificate_copy.write_bytes(certificate_path.read_bytes())
        require(
            safe_input_path(certificate_copy) == certificate_copy.resolve(),
            "valid copied certificate accepted",
        )
        reject("missing certificate", lambda: safe_input_path(root / "missing.json"))

        symlink_input = root / "certificate-symlink.json"
        symlink_input.symlink_to(certificate_copy)
        reject("certificate symlink", lambda: safe_input_path(symlink_input))

        hardlink_input = root / "certificate-hardlink.json"
        os.link(certificate_copy, hardlink_input)
        reject("certificate hardlink", lambda: safe_input_path(certificate_copy))
        hardlink_input.unlink()

        tampered_input = root / "certificate-tampered.json"
        tampered_input.write_bytes(certificate_path.read_bytes() + b" ")
        reject("tampered certificate byte pin", lambda: safe_input_path(tampered_input))

        reject(
            "output aliases certificate",
            lambda: safe_output_path(CERTIFICATE, certificate_copy),
        )
        reject(
            "output aliases selected certificate input",
            lambda: safe_output_path(certificate_copy, certificate_copy),
        )
        reject(
            "output aliases producer",
            lambda: safe_output_path(PRODUCER, certificate_copy),
        )
        reject(
            "output aliases verifier",
            lambda: safe_output_path(VERIFIER, certificate_copy),
        )
        first_upstream = HERE / sorted(PINS)[0]
        reject(
            "output aliases pinned upstream",
            lambda: safe_output_path(first_upstream, certificate_copy),
        )

        symlink_output = root / "output-symlink.json"
        symlink_output.symlink_to(certificate_copy)
        reject(
            "output symlink",
            lambda: safe_output_path(symlink_output, certificate_copy),
        )

        hardlink_output = root / "output-hardlink.json"
        os.link(certificate_copy, hardlink_output)
        reject(
            "output hardlink",
            lambda: safe_output_path(hardlink_output, certificate_copy),
        )
        hardlink_output.unlink()

        output_directory = root / "output-directory"
        output_directory.mkdir()
        reject(
            "output is directory",
            lambda: safe_output_path(output_directory, certificate_copy),
        )

        real_parent = root / "real-parent"
        real_parent.mkdir()
        linked_parent = root / "linked-parent"
        linked_parent.symlink_to(real_parent, target_is_directory=True)
        reject(
            "output parent symlink",
            lambda: safe_output_path(linked_parent / "output.json", certificate_copy),
        )

        fresh = root / "fresh-output.json"
        require(
            safe_output_path(fresh, certificate_copy) == fresh.resolve(),
            "fresh output path accepted",
        )
    require(len(labels) == 13, "13 path safety attacks rejected")
    return labels


def build_verification(
    expected: dict[str, Any],
    semantic_labels: list[str],
    strict_labels: list[str],
    path_labels: list[str],
) -> dict[str, Any]:
    summaries = {
        row["side"]: row for row in expected["return_summaries"]
    }
    crosswalk = expected[
        "primitive_free_Round132_typed_candidate_crosswalk"
    ]
    return {
        "status": "PASS",
        "verifier_sha256": sha256(VERIFIER),
        "producer_sha256": PRODUCER_SHA256,
        "certificate_sha256": CERTIFICATE_SHA256,
        "certificate_schema": CERTIFICATE_SCHEMA,
        "certificate_result_sha256": CERTIFICATE_RESULT_SHA256,
        "independence_contract": {
            "Round138_producer_imported": False,
            "Round138_producer_executed": False,
            "temporary_spike_read": False,
            "D0_b_star_side_roots_and_derivatives_independently_rebuilt": True,
            "both_fixed_dyadic_centres_and_leaf_graph_squares_rebuilt": True,
            "all_647_collision_rows_independently_reconstructed": True,
            "retained_and_full_radius4_candidate_ledgers_rebuilt": True,
            "official_words_homogeneity_incidence_and_terminals_rebuilt": True,
            "primitive_free_crosswalk_and_global_j3_rebuilt": True,
            "full_certificate_result_independently_reconstructed": True,
        },
        "replay_audit": {
            "common_local_parent_W_root_count": 1,
            "implicit_b_star_count": 1,
            "side_graph_square_count": 2,
            "collision_row_count": 647,
            "collision_rows_sha256": expected["collision_rows_sha256"],
            "BYPASS": {
                "return_depth": summaries["BYPASS"]["first_return_depth"],
                "terminal_target":
                    summaries["BYPASS"]["terminal_absolute_target"],
                "destination_core_id":
                    summaries["BYPASS"]["destination_core_id"],
                "retained_candidate_count_histogram":
                    summaries["BYPASS"]["retained_candidate_count_histogram"],
                "full_radius4_candidate_count_histogram":
                    summaries["BYPASS"][
                        "full_radius4_candidate_count_histogram"
                    ],
                "maximum_incidence_rank":
                    summaries["BYPASS"]["maximum_incidence_rank"],
            },
            "HIT": {
                "return_depth": summaries["HIT"]["first_return_depth"],
                "terminal_target":
                    summaries["HIT"]["terminal_absolute_target"],
                "destination_core_id":
                    summaries["HIT"]["destination_core_id"],
                "retained_candidate_count_histogram":
                    summaries["HIT"]["retained_candidate_count_histogram"],
                "full_radius4_candidate_count_histogram":
                    summaries["HIT"][
                        "full_radius4_candidate_count_histogram"
                    ],
                "maximum_incidence_rank":
                    summaries["HIT"]["maximum_incidence_rank"],
            },
            "primitive_free_typed_candidate_match_count":
                crosswalk["primitive_free_typed_candidate_match_count"],
            "global_insertion_time_j": crosswalk["global_insertion_time_j"],
        },
        "dual_precision_consistency": {
            "primary_precision_bits": MINIMUM_PRECISION_BITS,
            "secondary_precision_bits": SECONDARY_PRECISION_BITS,
            "complete_result_byte_semantics_equal": True,
            "result_sha256": digest(expected),
        },
        "semantic_mutation_test_count": len(semantic_labels),
        "semantic_mutation_rejection_labels": semantic_labels,
        "strict_json_attack_count": len(strict_labels),
        "strict_json_attack_rejection_labels": strict_labels,
        "path_safety_self_test_count": len(path_labels),
        "path_safety_rejection_labels": path_labels,
        "determinism_contract": {
            "canonical_JSON_sort_keys": True,
            "no_hash_iteration_controls_output": True,
            "verification_replay_is_PYTHONHASHSEED_independent": True,
            "dual_seed_byte_replay_required_by_freeze_pack": True,
        },
        "path_safety_contract": {
            "certificate_must_be_frozen_byte_pin": True,
            "input_must_be_regular_single_link_non_symlink": True,
            "output_must_be_regular_single_link_or_absent": True,
            "input_output_alias_rejected": True,
            "producer_verifier_certificate_and_all_pinned_upstreams_protected": True,
            "symlink_and_hardlink_attacks_rejected": True,
            "atomic_replace_after_fsync": True,
        },
        "safety_and_nonpromotion": dict(STRICT_NONPROMOTION),
    }


def write_document(path: Path, document: dict[str, Any]) -> None:
    text = json.dumps(
        document,
        sort_keys=True,
        indent=2,
        ensure_ascii=False,
        allow_nan=False,
    ) + "\n"
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.tmp-",
        dir=path.parent,
        text=True,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    try:
        require(PRODUCER_SHA256 is not None, "producer pin not frozen")
        require(CERTIFICATE_SHA256 is not None, "certificate pin not frozen")
        require(
            CERTIFICATE_RESULT_SHA256 is not None,
            "certificate result pin not frozen",
        )
        regular_single_link(PRODUCER, PRODUCER.name)
        require(sha256(PRODUCER) == PRODUCER_SHA256, "producer byte pin")
        regular_single_link(VERIFIER, VERIFIER.name)
        certificate_path = safe_input_path(args.certificate)
        output = safe_output_path(args.output, certificate_path)
        certificate = strict_json(certificate_path)
        primary = build_expected(MINIMUM_PRECISION_BITS, PRODUCER_SHA256)
        require(
            digest(primary) == CERTIFICATE_RESULT_SHA256,
            "independent result reconstruction pin",
        )
        evaluate_document(certificate, primary)
        secondary = build_expected(SECONDARY_PRECISION_BITS, PRODUCER_SHA256)
        require(
            secondary == primary,
            "12288/16384 complete result invariance",
        )
        semantic_labels = semantic_mutations(certificate, primary)
        strict_labels = strict_json_attacks(certificate, primary)
        path_labels = path_safety_self_tests(certificate_path)
        result = build_verification(
            primary,
            semantic_labels,
            strict_labels,
            path_labels,
        )
        document = {
            "schema": VERIFICATION_SCHEMA,
            "result": result,
            "result_sha256": digest(result),
        }
        write_document(output, document)
        print(
            canonical(
                {
                    "output": str(output),
                    "result_sha256": document["result_sha256"],
                    "semantic_mutations": len(semantic_labels),
                    "status": "PASS",
                    "strict_json_attacks": len(strict_labels),
                    "path_safety_tests": len(path_labels),
                }
            )
        )
        return 0
    except (
        VerificationError,
        UnicodeError,
        KeyError,
        IndexError,
        TypeError,
        ValueError,
        OSError,
    ) as exc:
        print(f"VerificationError: {exc}", file=os.sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
