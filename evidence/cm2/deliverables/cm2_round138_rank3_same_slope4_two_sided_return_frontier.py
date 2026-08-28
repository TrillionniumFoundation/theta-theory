#!/usr/bin/env python3
"""Round138: two actual returns on one canonical slope-four parent leaf.

Round116 constructs a corrected rank-three two-sided transverse collar, while
Round136 proves one unrelated fixed-p positive-area R1056 return cylinder.
This producer freezes a different and more local object: one exact implicit
slope-four leaf through the fixed-p D3=0 root on the selected W:E source
sheet.  On that *same* leaf it isolates the two levels

    D3 = -(4/25)^2 2^-128,       D3 = +(4/25)^2 2^-128,

moves a certified distance 2^-1800 toward the common D3=0 root, and encloses
positive-width t graph segments in rational squares of half-width 2^-2400.
Complete collision searches then give a BYPASS first return at R298 and a HIT
first return at R349.

The output materializes only two local return word-cells below one local
parent-W/root.  A primitive-free translated physical-event signature selects
one Round132 typed occurrence candidate and fixes the global insertion time
j=3 from the explicit collision timeline.  No global Round35 restriction,
connected-component rank, short-cell/image recut, owner, t54, Omega_j, or q_j
join is asserted.
"""

from __future__ import annotations

import argparse
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
OUTPUT = (
    HERE
    / "cm2-round138-rank3-same-slope4-two-sided-return-frontier-2026-07-24.json"
)
FUTURE_VERIFIER = (
    HERE
    / "cm2_round138_rank3_same_slope4_two_sided_return_frontier_verifier.py"
)
SCHEMA = "cm2.round138.rank3-same-slope4-two-sided-return-frontier.v1"
MINIMUM_PRECISION_BITS = 12288

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
    HERE
    / "cm2-round117-rank3-countable-homogeneity-operator-cells-2026-07-23.json"
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


def require(condition: bool, label: str) -> None:
    if not condition:
        raise RuntimeError(label)


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


def strict_json(path: Path) -> dict[str, Any]:
    metadata = path.lstat()
    require(
        stat.S_ISREG(metadata.st_mode)
        and metadata.st_nlink == 1
        and not path.is_symlink(),
        f"unsafe dependency type: {path.name}",
    )
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=strict_pairs,
        parse_float=lambda token: (_ for _ in ()).throw(
            ValueError(f"floating JSON number forbidden: {token}")
        ),
        parse_constant=lambda token: (_ for _ in ()).throw(
            ValueError(f"invalid JSON constant: {token}")
        ),
    )
    require(type(value) is dict, f"dependency root object: {path.name}")
    return value


def load_closed(path: Path) -> dict[str, Any]:
    value = strict_json(path)
    require(
        set(value) == {"schema", "result", "result_sha256"},
        f"closed dependency envelope: {path.name}",
    )
    require(value["schema"] == CLOSED_SCHEMAS[path.name], f"schema: {path.name}")
    require(
        type(value["result"]) is dict
        and value["result_sha256"] == digest(value["result"]),
        f"result digest: {path.name}",
    )
    return value["result"]


def verification_passed(result: dict[str, Any]) -> bool:
    return result.get("status") == "PASS" or result.get("verdict") == "PASS"


def validate_dependencies() -> dict[str, dict[str, Any]]:
    for name, expected in PINS.items():
        path = HERE / name
        require(
            path.is_file()
            and not path.is_symlink()
            and path.resolve().parent == HERE
            and sha256(path) == expected,
            f"dependency byte pin: {name}",
        )
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
        require(verification_passed(closed[path.name]), f"verification PASS: {path.name}")
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
    # This nested validation freezes the selected Round99/100/102/116 chain
    # used by Round136's formal helper library.
    round136.validate_dependencies()
    return closed


def interval(lower: Q, upper: Q) -> arb:
    return time3.time2_cert.first_hit.arb_interval(lower, upper)


def dyadic(power: int) -> Q:
    return Q(1, 2**power)


def floor_q(value: Q) -> int:
    return value.numerator // value.denominator


def ceil_q(value: Q) -> int:
    return -floor_q(-value)


def arb_pair(value: arb) -> tuple[Q, Q]:
    return round136.arb_pair(value)


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
        depth = round136.strict_dyadic_depth(value)
        self.counts[name] += 1
        if name not in self.depths or depth > self.depths[name]:
            self.depths[name] = depth
            self.witnesses[name] = witness
        return depth

    def public(self) -> dict[str, Any]:
        return {
            name: {
                "dyadic_depth": self.depths[name],
                "strict_lower_bound": qstr(
                    round136.power_of_two(-self.depths[name])
                ),
                "observation_count": self.counts[name],
                "one_worst-depth_witness": self.witnesses[name],
            }
            for name in sorted(self.depths)
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
    b_enclosure = fixed_dyadic_outer(
        exact_b_ball, B_STAR_ENCLOSURE_BITS
    )
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
            name: round136.strict_dyadic_depth(value)
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
        "fixed_p_D0_root_bracket": [
            qstr(d0_root[0]), qstr(d0_root[1])
        ],
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
        f"round138-{label.lower()}-same-slope4-graph-square",
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
                round136.strict_dyadic_depth(aq(graph_p0 - p0)),
            "graph_p_square_right":
                round136.strict_dyadic_depth(aq(p1 - graph_p1)),
            "side_root_t_clearance":
                round136.strict_dyadic_depth(aq(side_clearance)),
            "D0_root_t_clearance":
                round136.strict_dyadic_depth(aq(d0_clearance)),
            **{
                f"graph_D_{name}": round136.strict_dyadic_depth(value)
                for name, value in graph_margins.items()
            },
            **{
                f"square_D_{name}": round136.strict_dyadic_depth(value)
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
            decision_depths.append(ledger.observe(
                "full_radius4_candidate_miss_discriminant",
                -discriminant,
                witness,
            ))
            continue
        require(bool(discriminant > 0), "full candidate discriminant strict")
        radical = discriminant.sqrt()
        near, far = ell - radical, ell + radical
        if bool(far < 0):
            histogram["intersection_strictly_behind"] += 1
            decision_depths.append(ledger.observe(
                "full_radius4_candidate_behind_far_root",
                -far,
                witness,
            ))
            continue
        require(bool(near > 0), "full candidate near root strict")
        histogram["strict_future_near_root"] += 1
        decision_depths.append(ledger.observe(
            "full_radius4_candidate_future_root_positive",
            near,
            witness,
        ))
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
        registry_sha
        == "841cb96798c9bd41e1440c8b2cdd93af5d80f2f64d693f2aa00175a440045ab9",
        "official registry replay digest",
    )
    state = round136.initial_state(atom)
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
        owner, candidate_audit = round136.complete_owner(
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
        word, word_error = round136.translation_normalized_official_word(
            state,
            current_target,
            owner,
            pair_index,
            pattern_index,
        )
        require(
            word is not None and word_error is None,
            f"{label} official word {collision_index}: {word_error}",
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
        core_depth = round136.core_margin(
            owner,
            classification,
            destination,
            cores,
            ledger,
        )
        homogeneity_label, homogeneity_audit = generic_homogeneity_label(
            collision_index, owner["cosine"], ledger
        )
        source_rank = round136.capped_reciprocal_cosine_rank(
            previous_cosine,
            ledger,
            collision_index,
            "source",
        )
        target_rank = round136.capped_reciprocal_cosine_rank(
            owner["cosine"],
            ledger,
            collision_index,
            "target",
        )
        incidence_rank = max(14, source_rank, target_rank)
        next_state = time3.second_outgoing_state(atom, state, owner)
        require(next_state is not None, f"{label} outgoing reconstruction")
        outgoing_chart_depth = round136.chart_margin(next_state, ledger)
        row_base = {
            "side": label,
            "collision_index": collision_index,
            "incoming_absolute_owner_id": current_target,
            "incoming_chart": state["chart"],
            "selected_absolute_owner_id": owner["selected_target_id"],
            "complete_candidate_audit": candidate_audit,
            "full_radius4_candidate_audit": full_candidate_audit,
            "official_word_key": round136.compact_key(word["key"]),
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


def build(precision_bits: int = MINIMUM_PRECISION_BITS) -> dict[str, Any]:
    require(
        type(precision_bits) is int
        and precision_bits >= MINIMUM_PRECISION_BITS,
        "producer precision below 12288",
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
        and len(collision_rows) == 298 + 349
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
        r135["physical_F10_and_cemetery_separation_contract"][
            "physical_F10_count"
        ] == 0
        if "physical_F10_and_cemetery_separation_contract" in r135
        else r135["count_ledger"]["physical_F10_count"] == 0,
        "Round135 physical F10 frontier",
    )
    require(
        r136["strict_nonpromotion"]["global_least_dyadic_basis_component_rank_materialized"]
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
            "producer_sha256": sha256(Path(__file__).resolve()),
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
        "strict_nonpromotion": {
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
        },
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
        "strict_nonclaims": [
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
        ],
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
    result = json.loads(json.dumps(result, sort_keys=True))
    return {
        "schema": SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }


def protected_paths() -> set[Path]:
    return {
        Path(__file__).resolve(),
        FUTURE_VERIFIER.resolve(),
        *((HERE / name).resolve() for name in PINS),
    }


def validate_output_target(path: Path) -> Path:
    """Fail closed on hostile output paths before the expensive replay."""

    require(isinstance(path, Path), "output path type")
    absolute = path.absolute()
    require(
        absolute.name not in {"", ".", ".."},
        "safe output basename",
    )
    parent = absolute.parent
    require(
        parent.exists()
        and parent.is_dir()
        and not parent.is_symlink()
        and parent.resolve() == parent,
        "safe output parent without symlink components",
    )
    require(not absolute.is_symlink(), "output symlink")
    resolved = absolute.resolve(strict=False)
    protected = protected_paths()
    require(resolved not in protected, "output aliases protected input")
    if absolute.exists():
        metadata = absolute.lstat()
        require(
            stat.S_ISREG(metadata.st_mode)
            and metadata.st_nlink == 1,
            "safe existing output",
        )
        require(
            all(not os.path.samefile(absolute, item) for item in protected),
            "output hardlink aliases protected input",
        )
    return resolved


def write_atomic(path: Path, value: dict[str, Any]) -> None:
    resolved = validate_output_target(path)
    protected = {
        *protected_paths(),
    }
    require(resolved not in protected, "output aliases protected input")
    payload = json.dumps(
        value,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
        allow_nan=False,
    ) + "\n"
    descriptor, temporary = tempfile.mkstemp(
        prefix=f".{resolved.name}.",
        suffix=".tmp",
        dir=resolved.parent,
    )
    temporary_path = Path(temporary)
    try:
        with os.fdopen(
            descriptor, "w", encoding="utf-8", newline="\n"
        ) as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, resolved)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument(
        "--precision-bits", type=int, default=MINIMUM_PRECISION_BITS
    )
    args = parser.parse_args()
    validate_output_target(args.output)
    envelope = build(args.precision_bits)
    write_atomic(args.output, envelope)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
