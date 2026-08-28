#!/usr/bin/env python3
"""Independent fail-closed verifier for the Round139 minus-D0 H1 collar.

The Round139 producer is never imported or executed.  This verifier uses the
independent Round138 verifier kernel plus byte-pinned lower helpers to rebuild
the deep D0 witness, fixed dyadic collar/cylinder enclosures, both 1648-stage
paths, all retained and 161-candidate radius-four searches, official words,
homogeneity/incidence ranks, and C24 first-return decisions at two precisions.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import stat
import sys
import tempfile
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
from typing import Any, Callable, Iterable

from flint import arb, ctx

import cm2_round138_rank3_same_slope4_two_sided_return_frontier_verifier as base


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

HERE = Path(__file__).resolve().parent
VERIFIER = Path(__file__).resolve()
PRODUCER = (
    HERE / "cm2_round139_rank3_minus_d0_adjacent_h1_collar_return_frontier.py"
)
CERTIFICATE = (
    HERE
    / "cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-2026-07-24.json"
)
OUTPUT = (
    HERE
    / "cm2-round139-rank3-minus-d0-adjacent-h1-collar-return-frontier-verification-2026-07-24.json"
)
CERTIFICATE_SCHEMA = (
    "cm2.round139.rank3-minus-d0-adjacent-h1-collar-return-frontier.v1"
)
VERIFICATION_SCHEMA = (
    "cm2.round139.rank3-minus-d0-adjacent-h1-collar-return-frontier-verification.v1"
)

PRODUCER_SHA256: str | None = (
    "462ffcb41ba24771ce655ddb3ad5f18d5a22c8d0cb443ec1791ea9272d3d512b"
)
CERTIFICATE_SHA256: str | None = (
    "64e91e6b1efcb2675982fbc453b08349b003c8be5b4d236f61e1392aaee045f0"
)
CERTIFICATE_RESULT_SHA256: str | None = (
    "6e8f54c34154ea5ba3c95d4e901bc643c020a0a42e180241ae9053bb24f42236"
)

MINIMUM_PRECISION_BITS = 24576
SECONDARY_PRECISION_BITS = 32768
MAX_CERTIFICATE_BYTES = 10_000_000
MAX_INTEGER_DIGITS = 10_000
NEWTON_ITERATIONS = 5
NEWTON_ROUND_BITS = 23552
ROOT_HALF_WIDTH_POWER = 18432
B_STAR_OUTER_BITS = 16448
COORDINATE_OUTER_BITS = 8192
X_COLLAR_POWER = 5888
RETURN_DEPTH = 1648
ANCHOR_COLLISION_INDEX = 3
ANCHOR = base.DESIGNATED_TANGENT_OWNER
EXPECTED_MINUS_OWNER = "W[0,-1]"
EXPECTED_TERMINAL_OWNER = "G[-7,-13]"
EXPECTED_DESTINATION_CORE_ID = (
    "core:e47f553e056452faa012129434cdbbb6a55cd9671a19ea04e6b8a9f43054c4c2"
)
EXPECTED_OFFICIAL_SEQUENCE_SHA256 = (
    "f504289edce554d47e17a90d7c886586a69f3ec4b64fafd90c718c50ca93221e"
)
EXPECTED_OWNER_SEQUENCE_SHA256 = (
    "c50277af0c038521b8933672d2a5a2b9035473895694c3c2878842274337cac3"
)
EXPECTED_COMPACT_PATH_SHA256 = (
    "c37571201fa15065a7f8e4eeec9df5a79f36e077feac37a1aec7b910970e1f17"
)
OFFICIAL_REGISTRY_SHA256 = (
    "841cb96798c9bd41e1440c8b2cdd93af5d80f2f64d693f2aa00175a440045ab9"
)

R137_PRODUCER = HERE / "cm2_round137_seed_independent_dyadic_basis_rank_contract.py"
R137_CERTIFICATE = (
    HERE / "cm2-round137-seed-independent-dyadic-basis-rank-contract-2026-07-24.json"
)
R137_VERIFIER = (
    HERE / "cm2_round137_seed_independent_dyadic_basis_rank_contract_verifier.py"
)
R137_VERIFICATION = (
    HERE
    / "cm2-round137-seed-independent-dyadic-basis-rank-contract-verification-2026-07-24.json"
)
R138_PRODUCER = (
    HERE / "cm2_round138_rank3_same_slope4_two_sided_return_frontier.py"
)
R138_CERTIFICATE = (
    HERE
    / "cm2-round138-rank3-same-slope4-two-sided-return-frontier-2026-07-24.json"
)
R138_VERIFIER = (
    HERE / "cm2_round138_rank3_same_slope4_two_sided_return_frontier_verifier.py"
)
R138_VERIFICATION = (
    HERE
    / "cm2-round138-rank3-same-slope4-two-sided-return-frontier-verification-2026-07-24.json"
)

PINS = {
    R137_PRODUCER.name:
        "81974ada469f8f24299d7790e16f6380f58b38df151ee67704695aa81c0d08ac",
    R137_CERTIFICATE.name:
        "06918b7bbfdeed9bda41a1220a25b630df6eaaa5f06024757f25a8c9fe7b88bf",
    R137_VERIFIER.name:
        "8d359eb9d397d3c4375d2ae21cc752447f0fb9216d180b59b3517288914fba45",
    R137_VERIFICATION.name:
        "53369532c293d9cb2830a362facef7e4c4040f826f5ddea70519fde9034a1a5c",
    R138_PRODUCER.name:
        "42d749dccea86aa3a122707db0226def176e75047d5dcb4bf19826b50e09282b",
    R138_CERTIFICATE.name:
        "c1f4d5041d810dd91d38e39bf795e5ab05536065ba8b0730530c58a91f7bf6d8",
    R138_VERIFIER.name:
        "7dfb9068696c5c868c614114c72e7c5819270c84c2c2455ad98f5e4f5321f941",
    R138_VERIFICATION.name:
        "1cd9878d03bde25bceb0dcf292d47783fe697de347ca653d1994b72a509015c3",
}

CLOSED_SCHEMAS = {
    R137_CERTIFICATE.name:
        "cm2.round137.seed-independent-dyadic-basis-rank-contract.v1",
    R137_VERIFICATION.name:
        "cm2.round137.seed-independent-dyadic-basis-rank-contract-verification.v1",
    R138_CERTIFICATE.name:
        "cm2.round138.rank3-same-slope4-two-sided-return-frontier.v1",
    R138_VERIFICATION.name:
        "cm2.round138.rank3-same-slope4-two-sided-return-frontier-verification.v1",
}


class VerificationError(RuntimeError):
    pass


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


def with_hash(row: dict[str, Any]) -> dict[str, Any]:
    require("row_sha256" not in row, "row already hashed")
    return {**row, "row_sha256": digest(row)}


class FastMarginLedger:
    def __init__(self) -> None:
        self.depths: dict[str, int] = {}
        self.counts: Counter[str] = Counter()
        self.witnesses: dict[str, dict[str, Any] | None] = {}

    @staticmethod
    def strict_depth(value: arb) -> int:
        lower_bound = value.lower()
        require(bool(lower_bound > 0), "fast ledger strict positive")
        mantissa, exponent = lower_bound.man_exp()
        integer = int(mantissa)
        require(integer > 0, "fast ledger positive mantissa")
        floor_log2 = integer.bit_length() - 1 + int(exponent)
        if integer & (integer - 1) == 0:
            floor_log2 -= 1
        return -floor_log2

    def observe(
        self,
        name: str,
        value: arb,
        witness: dict[str, Any] | None = None,
    ) -> int:
        depth = self.strict_depth(value)
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
                    base.power_of_two(-self.depths[name])
                ),
                "observation_count": self.counts[name],
                "one_worst-depth_witness": self.witnesses[name],
            }
            for name in sorted(self.depths)
        }


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
    document = strict_json(path)
    require(
        set(document) == {"schema", "result", "result_sha256"},
        f"closed dependency envelope:{path.name}",
    )
    require(document["schema"] == CLOSED_SCHEMAS[path.name], f"schema:{path.name}")
    require(
        type(document["result"]) is dict
        and document["result_sha256"] == digest(document["result"]),
        f"result closure:{path.name}",
    )
    return document["result"]


def validate_dependencies() -> dict[str, dict[str, Any]]:
    for name, expected in sorted(PINS.items()):
        path = HERE / name
        metadata = path.lstat()
        require(
            stat.S_ISREG(metadata.st_mode)
            and metadata.st_nlink == 1
            and not path.is_symlink()
            and path.resolve().parent == HERE
            and sha256(path) == expected,
            f"dependency byte pin:{name}",
        )
    closed = {
        path.name: load_closed(path)
        for path in (
            R137_CERTIFICATE,
            R137_VERIFICATION,
            R138_CERTIFICATE,
            R138_VERIFICATION,
        )
    }
    require(
        closed[R137_VERIFICATION.name]["status"] == "PASS"
        and closed[R138_VERIFICATION.name]["status"] == "PASS",
        "Round137/138 verification PASS",
    )
    base.validate_dependencies()
    return closed


def nearest_dyadic(value: Q, bits: int) -> Q:
    scale = 2**bits
    shifted = value * scale + Q(1, 2)
    return Q(shifted.numerator // shifted.denominator, scale)


def fixed_p_jet(source: Any, t_value: Q) -> Any:
    return base.third_tangency_jet(
        source,
        base.SECOND_OWNER,
        ANCHOR,
        t_value,
        t_value,
        base.SOURCE_P_STAR,
        base.SOURCE_P_STAR,
    )


def deep_root_and_b(
    source: Any,
    round138_result: dict[str, Any],
) -> tuple[tuple[Q, Q], tuple[Q, Q], dict[str, Any]]:
    common = round138_result["common_same_slope4_parent_leaf"]
    old_root = tuple(Q(value) for value in common["fixed_p_D0_root_bracket"])
    require(
        bool(fixed_p_jet(source, old_root[0]).value < 0)
        and bool(fixed_p_jet(source, old_root[1]).value > 0),
        "old D0 signs",
    )
    old_full = base.third_tangency_jet(
        source,
        base.SECOND_OWNER,
        ANCHOR,
        old_root[0],
        old_root[1],
        base.SOURCE_P_STAR,
        base.SOURCE_P_STAR,
    )
    require(bool(old_full.gradient[0] > 0), "old D0 uniqueness")
    center = (old_root[0] + old_root[1]) / 2
    for _index in range(NEWTON_ITERATIONS):
        evaluated = fixed_p_jet(source, center)
        value_mid = base.exact_dyadic(evaluated.value.mid())
        derivative_mid = base.exact_dyadic(evaluated.gradient[0].mid())
        require(derivative_mid > 0, "Newton derivative")
        center = nearest_dyadic(
            center - value_mid / derivative_mid, NEWTON_ROUND_BITS
        )
    half = Q(1, 2**ROOT_HALF_WIDTH_POWER)
    root = (center - half, center + half)
    left = fixed_p_jet(source, root[0]).value
    right = fixed_p_jet(source, root[1]).value
    full = base.third_tangency_jet(
        source,
        base.SECOND_OWNER,
        ANCHOR,
        root[0],
        root[1],
        base.SOURCE_P_STAR,
        base.SOURCE_P_STAR,
    )
    require(
        old_root[0] < root[0] < root[1] < old_root[1]
        and bool(left < 0)
        and bool(right > 0)
        and bool(full.gradient[0] > 0),
        "deep D0 isolation",
    )
    exact_b = (
        base.aq(base.SOURCE_P_STAR).asin()
        - base.aq(base.KAPPA) * base.interval(*root).asin()
    )
    b_enclosure = base.fixed_dyadic_outer(exact_b, B_STAR_OUTER_BITS)
    old_b = tuple(Q(value) for value in common["b_star_fixed_dyadic_outer"])
    require(
        old_b[0] < b_enclosure[0] < b_enclosure[1] < old_b[1],
        "deep b nested",
    )
    row = with_hash({
        "same_Round138_local_parent_W_id": common["local_parent_W_id"],
        "same_exact_fixed_p_D0_root": True,
        "same_exact_implicit_b_star": True,
        "old_Round138_D0_root_bracket": [qstr(value) for value in old_root],
        "old_Round138_b_star_outer": [qstr(value) for value in old_b],
        "witness_locator":
            "five fixed-rounding point Newton steps; not used as the proof",
        "newton_iteration_count": NEWTON_ITERATIONS,
        "newton_rounding_bits": NEWTON_ROUND_BITS,
        "deep_D0_root_bracket": [qstr(value) for value in root],
        "deep_D0_root_bracket_width": qstr(root[1] - root[0]),
        "deep_D0_root_bracket_width_floor_log2":
            base.floor_log2_fraction(root[1] - root[0]),
        "deep_D0_endpoint_signs": [-1, 1],
        "deep_D0_D_t_strict_positive": True,
        "deep_D0_unique": True,
        "deep_D0_D_t_margin_dyadic_depth":
            base.strict_dyadic_depth(full.gradient[0]),
        "b_star_fixed_dyadic_outer_bits": B_STAR_OUTER_BITS,
        "b_star_fixed_dyadic_outer": [qstr(value) for value in b_enclosure],
        "b_star_outer_nested_in_Round138": True,
        "formal_root_proof":
            "strict endpoint signs plus D_t>0 on the whole deep bracket",
    })
    return root, b_enclosure, row


def fixed_outer(value: arb) -> tuple[Q, Q]:
    raw_lower, raw_upper = base.arb_pair(value)
    scale = 2**COORDINATE_OUTER_BITS
    fixed_lower = Q(base.floor_q(raw_lower * scale) - 1, scale)
    fixed_upper = Q(base.ceil_q(raw_upper * scale) + 1, scale)
    require(
        fixed_lower < fixed_upper
        and bool(value > base.aq(fixed_lower))
        and bool(value < base.aq(fixed_upper)),
        "fixed padded coordinate outer",
    )
    return fixed_lower, fixed_upper


def leaf_p_ball(
    t_lower: Q,
    t_upper: Q,
    b_enclosure: tuple[Q, Q],
) -> arb:
    phase = (
        base.aq(base.KAPPA) * base.interval(t_lower, t_upper).asin()
        + base.interval(*b_enclosure)
    )
    return phase.sin()


def x_collar(
    source: Any,
    root: tuple[Q, Q],
    b_enclosure: tuple[Q, Q],
    parent_id: str,
    strip: tuple[Q, Q, Q, Q],
) -> tuple[Any, dict[str, Any]]:
    ell = Q(1, 2**X_COLLAR_POWER)
    root_r_ball = base.aq(base.R_W) * base.interval(*root).asin()
    delta_r_ball = base.aq(ell) / base.aq(17).sqrt()
    endpoint_r_ball = root_r_ball - delta_r_ball
    root_r = fixed_outer(root_r_ball)
    delta_r = fixed_outer(delta_r_ball)
    endpoint_r = fixed_outer(endpoint_r_ball)
    r_hull = (endpoint_r[0], root_r[1])
    t0, t1 = fixed_outer(
        (
            base.aq(Q(1, 1) / base.R_W)
            * base.interval(*r_hull)
        ).sin()
    )
    p0, p1 = fixed_outer(leaf_p_ball(t0, t1, b_enclosure))
    require(
        strip[0] < t0 < t1 < strip[1]
        and strip[2] < p0 < p1 < strip[3]
        and source.t0 < t0 < t1 < source.t1
        and source.p0 < p0 < p1 < source.p1,
        "collar inside selected strip",
    )
    atom = base.step1.Atom(
        base.SOURCE_CORE_INDEX,
        source,
        t0,
        t1,
        p0,
        p1,
        Q(0),
        Q(0),
        "round139-minus-d0-adjacent-h1-x-collar-k5888",
    )
    far_t = fixed_outer(
        (
            base.aq(Q(1, 1) / base.R_W) * endpoint_r_ball
        ).sin()
    )
    far_p = fixed_outer(
        (
            base.aq(base.SOURCE_P_STAR).asin()
            - base.aq(4) * delta_r_ball
        ).sin()
    )
    far_D = base.third_tangency_jet(
        source,
        base.SECOND_OWNER,
        ANCHOR,
        far_t[0],
        far_t[1],
        far_p[0],
        far_p[1],
    ).value
    require(bool(far_D < 0), "far endpoint minus")
    graph_jet = base.third_tangency_jet(
        source, base.SECOND_OWNER, ANCHOR, t0, t1, p0, p1
    )
    t_interval, p_interval = base.interval(t0, t1), base.interval(p0, p1)
    dp_dt = (
        base.aq(base.KAPPA)
        * (1 - p_interval * p_interval).sqrt()
        / (1 - t_interval * t_interval).sqrt()
    )
    along = graph_jet.gradient[0] + graph_jet.gradient[1] * dp_dt
    require(bool(along > 0), "collar D monotone")
    row = with_hash({
        "same_Round138_local_parent_W_id": parent_id,
        "mode": "CANONICAL_H1_ARCLENGTH_X_ONE_SIDED_EXACT_LEAF_COLLAR",
        "canonical_coordinate":
            "x=sqrt(17)*r, r=(4/25)*asin(t), v=asin(p)-4r=b_star",
        "H1_arclength_identity_on_fixed_v_leaf": "dx=sqrt(17)*dr",
        "x_collar_power": X_COLLAR_POWER,
        "ell": qstr(ell),
        "exact_half_open_x_collar":
            f"[x_star-2^-{X_COLLAR_POWER},x_star)",
        "closed_branch_continuation_enclosure":
            f"[x_star-2^-{X_COLLAR_POWER},x_star]",
        "coordinate_outer_bits": COORDINATE_OUTER_BITS,
        "r_star_outer": [qstr(value) for value in root_r],
        "delta_r_outer": [qstr(value) for value in delta_r],
        "far_r_outer": [qstr(value) for value in endpoint_r],
        "r_collar_hull": [qstr(value) for value in r_hull],
        "t_image_outer": [qstr(t0), qstr(t1)],
        "p_image_outer": [qstr(p0), qstr(p1)],
        "exact_leaf_graph_contained_in_replayed_rectangle": True,
        "rectangle_enclosure_inside_selected_Round116_strip": True,
        "rectangle_enclosure_inside_source_core": True,
        "far_endpoint": {
            "t_outer": [qstr(value) for value in far_t],
            "p_outer": [qstr(value) for value in far_p],
            "strict_D3_negative": True,
            "negative_D3_margin_dyadic_depth":
                base.strict_dyadic_depth(-far_D),
        },
        "D3_strictly_increasing_along_whole_leaf_collar": True,
        "D3_along_leaf_margin_dyadic_depth":
            base.strict_dyadic_depth(along),
        "D3_negative_on_exact_half_open_collar": True,
        "only_D3_zero_endpoint": "x_star",
        "positive_H1_one_sided_width": True,
    })
    return atom, row


def positive_area_cylinder(
    source: Any,
    collar_atom: Any,
    b_enclosure: tuple[Q, Q],
    parent_id: str,
    strip: tuple[Q, Q, Q, Q],
) -> tuple[Any, dict[str, Any]]:
    t0, t1 = collar_atom.t0, (collar_atom.t0 + collar_atom.t1) / 2
    p0, p1 = fixed_outer(leaf_p_ball(t0, t1, b_enclosure))
    require(
        collar_atom.t0 <= t0 < t1 < collar_atom.t1
        and collar_atom.p0 <= p0 < p1 <= collar_atom.p1,
        "cylinder inside collar enclosure",
    )
    require(
        strip[0] < t0 < t1 < strip[1]
        and strip[2] < p0 < p1 < strip[3]
        and source.t0 < t0 < t1 < source.t1
        and source.p0 < p0 < p1 < source.p1,
        "cylinder inside selected strip",
    )
    anchor_D = base.third_tangency_jet(
        source, base.SECOND_OWNER, ANCHOR, t0, t1, p0, p1
    ).value
    require(bool(anchor_D < 0), "cylinder anchor miss")
    atom = base.step1.Atom(
        base.SOURCE_CORE_INDEX,
        source,
        t0,
        t1,
        p0,
        p1,
        Q(0),
        Q(0),
        "round139-positive-area-r1648-cylinder",
    )
    area = (t1 - t0) * (p1 - p0)
    row = with_hash({
        "same_Round138_local_parent_W_id": parent_id,
        "object_kind": "LOCAL_POSITIVE_AREA_FIXED_S_R1648_CYLINDER",
        "construction":
            "first t-half of the graph-collar rectangle, with a fresh leaf p-hull",
        "t_box": [qstr(t0), qstr(t1)],
        "p_box": [qstr(p0), qstr(p1)],
        "s_box": ["0", "0"],
        "t_width": qstr(t1 - t0),
        "p_width": qstr(p1 - p0),
        "area": qstr(area),
        "t_width_floor_log2": base.floor_log2_fraction(t1 - t0),
        "p_width_floor_log2": base.floor_log2_fraction(p1 - p0),
        "contained_in_graph_collar_rectangle_enclosure": True,
        "strictly_inside_selected_Round116_strip": True,
        "strictly_inside_source_core": True,
        "contains_a_positive_width_exact_leaf_subgraph": True,
        "is_not_the_one_dimensional_graph_collar": True,
        "whole_box_D3_anchor_discriminant_strictly_negative": True,
        "whole_box_D3_anchor_miss_margin_dyadic_depth":
            base.strict_dyadic_depth(-anchor_D),
        "ordinary_anchor_inclusive_collision_replay_required": True,
        "positive_area": True,
    })
    return atom, row


def owner_excluding_anchor(
    state: dict[str, Any],
    current_target: str,
    candidates: Iterable[str],
    ledger: Any,
    collision_index: int,
    full_radius4: bool,
) -> tuple[dict[str, Any], dict[str, Any]]:
    require(collision_index == 3, "anchor exclusion stage")
    candidate_ids = tuple(candidates)
    require(ANCHOR in candidate_ids, "anchor candidate present")
    prefix = "full_radius4_" if full_radius4 else ""
    qx, qy, ux, uy, s = (
        state["contact_x"],
        state["contact_y"],
        state["outgoing_x"],
        state["outgoing_y"],
        state["s"],
    )
    future: list[tuple[str, dict[str, arb]]] = []
    histogram: Counter[str] = Counter()
    depths: list[int] = []
    anchor_audit: dict[str, Any] | None = None
    ambiguous: list[str] = []
    for candidate_id in candidate_ids:
        center_x, center_y = base.time3.time2_cert.target_center(candidate_id, s)
        dx, dy = center_x - qx, center_y - qy
        ell = ux * dx + uy * dy
        transverse = -uy * dx + ux * dy
        radius = base.aq(
            base.time3.time2_cert.first_hit.RADIUS[candidate_id[0]]
        )
        discriminant = radius * radius - transverse * transverse
        witness = {"collision_index": collision_index, "candidate_id": candidate_id}
        if candidate_id == ANCHOR:
            low, high = base.arb_pair(discriminant)
            tau_margin = base.aq(base.time3.time2_cert.first_hit.TAU_MAX) - ell
            require(
                low <= 0 <= high and bool(ell > 0) and bool(tau_margin > 0),
                "anchor double root",
            )
            anchor_audit = {
                "candidate_id": ANCHOR,
                "discriminant_is_the_D3_function": True,
                "closed_collar_discriminant_contains_zero": True,
                "exact_zero_occurs_only_at_x_star": True,
                "interior_exact_leaf_discriminant_strictly_negative": True,
                "double_root_flight_strictly_positive_dyadic_depth":
                    base.strict_dyadic_depth(ell),
                "double_root_below_tau_dyadic_depth":
                    base.strict_dyadic_depth(tau_margin),
                "excluded_only_from_collision3_branch_continuation": True,
            }
            continue
        if bool(discriminant < 0):
            histogram["no_real_intersection"] += 1
            depths.append(ledger.observe(
                prefix + "candidate_miss_discriminant",
                -discriminant,
                witness,
            ))
            continue
        if not bool(discriminant > 0):
            ambiguous.append(candidate_id)
            continue
        if not full_radius4:
            depths.append(ledger.observe(
                "candidate_positive_discriminant", discriminant, witness
            ))
        radical = discriminant.sqrt()
        near, far = ell - radical, ell + radical
        if bool(far < 0):
            histogram["intersection_strictly_behind"] += 1
            depths.append(ledger.observe(
                prefix + "candidate_behind_far_root", -far, witness
            ))
            continue
        require(bool(near > 0), "nonanchor future root")
        histogram["strict_future_near_root"] += 1
        depths.append(ledger.observe(
            prefix + "candidate_future_root_positive", near, witness
        ))
        future.append((
            candidate_id,
            {
                "near": near,
                "radical": radical,
                "transverse": transverse,
                "radius": radius,
                "discriminant": discriminant,
            },
        ))
    require(anchor_audit is not None and not ambiguous, "only anchor ambiguous")
    winners = [
        (candidate_id, row)
        for candidate_id, row in future
        if all(
            candidate_id == other_id or bool(row["near"] < other["near"])
            for other_id, other in future
        )
    ]
    require(
        len(winners) == 1 and winners[0][0] == EXPECTED_MINUS_OWNER,
        "minus branch winner",
    )
    selected_id, selected = winners[0]
    gap_depths = [
        ledger.observe(
            prefix + "winner_pairwise_root_gap",
            row["near"] - selected["near"],
            {
                "collision_index": collision_index,
                "winner_id": selected_id,
                "competitor_id": candidate_id,
            },
        )
        for candidate_id, row in future
        if candidate_id != selected_id
    ]
    root = selected["near"]
    if not full_radius4:
        tau_margin = base.aq(base.time3.time2_cert.first_hit.TAU_MAX) - root
        require(bool(tau_margin > 0), "winner tau")
        ledger.observe("selected_root_positive", root, {"collision_index": 3})
        ledger.observe(
            "selected_discriminant_positive",
            selected["discriminant"],
            {"collision_index": 3, "candidate_id": selected_id},
        )
        ledger.observe(
            "selected_root_below_tau_max", tau_margin, {"collision_index": 3}
        )
    radical, transverse, radius = (
        selected["radical"],
        selected["transverse"],
        selected["radius"],
    )
    owner = {
        "selected_target_id": selected_id,
        "selected_root": root,
        "normal_x": (-radical * ux + transverse * uy) / radius,
        "normal_y": (-radical * uy - transverse * ux) / radius,
        "p": transverse / radius,
        "cosine": radical / radius,
    }
    require(sum(histogram.values()) == len(candidate_ids) - 1, "anchor census")
    audit = {
        "candidate_universe":
            "full-radius-four" if full_radius4 else "retained-chart",
        "candidate_count": len(candidate_ids),
        "nonanchor_candidate_count": len(candidate_ids) - 1,
        "anchor_candidate_count": 1,
        "ambiguous_nonanchor_candidate_count": 0,
        "candidate_classification_histogram": dict(sorted(histogram.items())),
        "minimum_candidate_decision_margin_dyadic_depth": max(depths),
        "minimum_winner_gap_dyadic_depth":
            max(gap_depths) if gap_depths else None,
        "selected_target_id": selected_id,
        "selected_target_matches_minus_branch": True,
        "anchor": anchor_audit,
    }
    return owner, audit


def official_wall_margin_audit(
    state: dict[str, Any],
    current_target: str,
    owner: dict[str, Any],
    ledger: Any,
    collision_index: int,
) -> dict[str, Any]:
    qx, qy, ux, uy = (
        state["contact_x"],
        state["contact_y"],
        state["outgoing_x"],
        state["outgoing_y"],
    )
    root = owner["selected_root"]
    hit_x, hit_y = qx + root * ux, qy + root * uy
    _obstacle, shift_x, shift_y = base.component_cert.parse_target(
        current_target
    )
    coordinates = (
        ("X", qx - arb(shift_x), hit_x - arb(shift_x)),
        ("Y", qy - arb(shift_y), hit_y - arb(shift_y)),
    )
    endpoint_depths: list[int] = []
    crossing_depths: list[int] = []
    events: list[tuple[arb, str, int]] = []
    for axis, q_value, h_value in coordinates:
        for endpoint_role, endpoint in (
            ("source", q_value),
            ("target", h_value),
        ):
            adjacent = [
                wall
                for wall in range(-7, 7)
                if bool(endpoint > arb(wall))
                and bool(endpoint < arb(wall + 1))
            ]
            require(len(adjacent) == 1, "endpoint strict integer cell")
            lower_wall = adjacent[0]
            for wall, margin in (
                (lower_wall, endpoint - arb(lower_wall)),
                (lower_wall + 1, arb(lower_wall + 1) - endpoint),
            ):
                endpoint_depths.append(ledger.observe(
                    "official_wall_endpoint_integer_margin",
                    margin,
                    {
                        "collision_index": collision_index,
                        "axis": axis,
                        "endpoint_role": endpoint_role,
                        "wall": wall,
                    },
                ))
        axis_events, reason = base.component_cert.ordered_axis_events(
            q_value, h_value, axis
        )
        require(axis_events is not None and reason is None, "axis events")
        for alpha, token, wall in axis_events:
            crossing_depths.append(ledger.observe(
                "official_wall_crossing_time_from_zero",
                alpha,
                {
                    "collision_index": collision_index,
                    "token": token,
                    "wall": wall,
                },
            ))
            crossing_depths.append(ledger.observe(
                "official_wall_crossing_time_from_one",
                arb(1) - alpha,
                {
                    "collision_index": collision_index,
                    "token": token,
                    "wall": wall,
                },
            ))
        events.extend(axis_events)
    order_depths: list[int] = []
    for first_index, (first_alpha, first_token, first_wall) in enumerate(events):
        for second_alpha, second_token, second_wall in events[first_index + 1:]:
            if bool(first_alpha < second_alpha):
                gap = second_alpha - first_alpha
            else:
                require(
                    bool(second_alpha < first_alpha),
                    "official strict event order",
                )
                gap = first_alpha - second_alpha
            order_depths.append(ledger.observe(
                "official_wall_event_order_gap",
                gap,
                {
                    "collision_index": collision_index,
                    "first_token": first_token,
                    "first_wall": first_wall,
                    "second_token": second_token,
                    "second_wall": second_wall,
                },
            ))
    crossings, reason = base.component_cert.strict_event_order(events)
    require(crossings is not None and reason is None, "wall total order")
    return {
        "endpoint_integer_margin_minimum_dyadic_depth": max(endpoint_depths),
        "crossing_time_endpoint_margin_minimum_dyadic_depth":
            max(crossing_depths) if crossing_depths else None,
        "event_order_gap_minimum_dyadic_depth":
            max(order_depths) if order_depths else None,
        "ordered_crossing_count": len(events),
    }


def replay(
    atom: Any,
    parent_id: str,
    object_kind: str,
    analytic_anchor_exclusion: bool,
) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    cores = tuple(base.core_cert.physical_cores())
    pair_index, pattern_index, registry_sha = base.component_cert.key_index_tables()
    require(registry_sha == OFFICIAL_REGISTRY_SHA256, "registry digest")
    state = base.initial_state(atom)
    current_target = base.SOURCE_ABSOLUTE_OWNER
    previous_cosine = (1 - state["p"] * state["p"]).sqrt()
    ledger = FastMarginLedger()
    rows: list[dict[str, Any]] = []
    compact_rows: list[list[Any]] = []
    owners: list[str] = []
    official_ids: list[str] = []
    homogeneity_labels: list[str] = []
    incidence_ranks: list[int] = []
    retained_histogram: Counter[int] = Counter()
    full_histogram: Counter[int] = Counter()
    retained_totals: Counter[str] = Counter()
    full_totals: Counter[str] = Counter()
    collision3_audits: dict[str, Any] = {}
    for collision_index in range(1, RETURN_DEPTH + 1):
        if analytic_anchor_exclusion and collision_index == 3:
            owner, retained_audit = owner_excluding_anchor(
                state,
                current_target,
                base.time3.time2_cert.translated_candidate_ids(
                    current_target, state["chart"]
                ),
                ledger,
                collision_index,
                False,
            )
            full_owner, full_audit = owner_excluding_anchor(
                state,
                current_target,
                base.charge.candidate_ids_around(current_target),
                ledger,
                collision_index,
                True,
            )
            require(
                owner["selected_target_id"] == full_owner["selected_target_id"],
                "special retained/full winner",
            )
            collision3_audits = {
                "retained": with_hash(retained_audit),
                "full_radius4": with_hash(full_audit),
            }
            retained_count = retained_audit["candidate_count"]
            full_count = full_audit["candidate_count"]
        else:
            owner, retained_audit = base.complete_owner(
                state, current_target, ledger, collision_index
            )
            full_audit = base.full_radius4_candidate_audit(
                state, current_target, owner, ledger, collision_index
            )
            retained_count = retained_audit["retained_candidate_count"]
            full_count = full_audit["full_candidate_count"]
        require(
            full_count == 161
            and (
                analytic_anchor_exclusion and collision_index == 3
                or full_audit["selected_target_matches_retained_search"]
            ),
            "full radius4 equality",
        )
        word, error = base.translation_normalized_official_word(
            state, current_target, owner, pair_index, pattern_index
        )
        require(word is not None and error is None, f"official word:{collision_index}")
        official_margin_audit = official_wall_margin_audit(
            state, current_target, owner, ledger, collision_index
        )
        classification, destination, witnesses = base.time3.core_classification(
            owner, cores
        )
        if collision_index < RETURN_DEPTH:
            require(
                classification == "SURVIVE_THROUGH_3_INNER"
                and destination is None,
                f"preterminal:{collision_index}",
            )
        else:
            require(
                classification == "RETURN_AT_3_INNER"
                and destination == EXPECTED_DESTINATION_CORE_ID
                and owner["selected_target_id"] == EXPECTED_TERMINAL_OWNER,
                "terminal return",
            )
        core_depth = base.core_margin(
            owner, classification, destination, cores, ledger
        )
        homogeneity_label, homogeneity_audit = base.generic_homogeneity_label(
            collision_index, owner["cosine"], ledger
        )
        source_rank = base.capped_reciprocal_cosine_rank(
            previous_cosine, ledger, collision_index, "source"
        )
        target_rank = base.capped_reciprocal_cosine_rank(
            owner["cosine"], ledger, collision_index, "target"
        )
        incidence_rank = max(14, source_rank, target_rank)
        next_state = base.time3.second_outgoing_state(atom, state, owner)
        require(next_state is not None, f"outgoing:{collision_index}")
        chart_depth = base.chart_margin(next_state, ledger)
        compact_key = base.compact_key(word["key"])
        row = with_hash({
            "collision_index": collision_index,
            "incoming_absolute_owner_id": current_target,
            "selected_absolute_owner_id": owner["selected_target_id"],
            "retained_candidate_count": retained_count,
            "retained_candidate_minimum_decision_margin_dyadic_depth":
                retained_audit["minimum_candidate_decision_margin_dyadic_depth"],
            "retained_candidate_minimum_winner_gap_dyadic_depth":
                retained_audit["minimum_winner_gap_dyadic_depth"],
            "full_radius4_candidate_count": full_count,
            "full_radius4_candidate_minimum_decision_margin_dyadic_depth":
                full_audit["minimum_candidate_decision_margin_dyadic_depth"],
            "full_radius4_candidate_minimum_winner_gap_dyadic_depth":
                full_audit["minimum_winner_gap_dyadic_depth"],
            "retained_and_full_radius4_selected_owner_equal": True,
            "official_word_key": compact_key,
            "ordered_clean_wall_record": word["ordered_clean_wall_record"],
            "relative_frozen_target_id": word["relative_frozen_target_id"],
            "absolute_lattice_translation_removed":
                word["absolute_lattice_translation_removed"],
            "official_wall_endpoint_integer_margin_dyadic_depth":
                official_margin_audit[
                    "endpoint_integer_margin_minimum_dyadic_depth"
                ],
            "official_wall_crossing_time_endpoint_margin_dyadic_depth":
                official_margin_audit[
                    "crossing_time_endpoint_margin_minimum_dyadic_depth"
                ],
            "official_wall_event_order_gap_dyadic_depth":
                official_margin_audit[
                    "event_order_gap_minimum_dyadic_depth"
                ],
            "official_wall_ordered_crossing_count":
                official_margin_audit["ordered_crossing_count"],
            "homogeneity_label": homogeneity_label,
            "homogeneity_lower_margin_dyadic_depth":
                homogeneity_audit["lower_boundary_margin_dyadic_depth"],
            "homogeneity_upper_margin_dyadic_depth":
                homogeneity_audit["upper_boundary_margin_dyadic_depth"],
            "source_capped_reciprocal_cosine_rank": source_rank,
            "target_capped_reciprocal_cosine_rank": target_rank,
            "incidence_rank_B": incidence_rank,
            "C24_classification": classification,
            "destination_core_id": destination,
            "C24_core_witness_count": len(witnesses),
            "C24_minimum_inside_or_exclusion_margin_dyadic_depth": core_depth,
            "outgoing_chart": next_state["chart"],
            "outgoing_chart_margin_dyadic_depth": chart_depth,
        })
        rows.append(row)
        owners.append(owner["selected_target_id"])
        official_ids.append(compact_key["official_word_key_id"])
        homogeneity_labels.append(homogeneity_label)
        incidence_ranks.append(incidence_rank)
        compact_rows.append([
            collision_index,
            current_target,
            owner["selected_target_id"],
            compact_key["official_word_key_id"],
            homogeneity_label,
            incidence_rank,
            classification,
            destination,
        ])
        retained_histogram[retained_count] += 1
        full_histogram[full_count] += 1
        for name, count in retained_audit[
            "candidate_classification_histogram"
        ].items():
            retained_totals[name] += count
        for name, count in full_audit[
            "candidate_classification_histogram"
        ].items():
            full_totals[name] += count
        state, current_target, previous_cosine = (
            next_state,
            owner["selected_target_id"],
            owner["cosine"],
        )
    require(
        owners[:3]
        == [base.EXPECTED_SOURCE_TARGET, base.SECOND_OWNER, EXPECTED_MINUS_OWNER],
        "path prefix",
    )
    require(
        digest(official_ids) == EXPECTED_OFFICIAL_SEQUENCE_SHA256
        and digest(owners) == EXPECTED_OWNER_SEQUENCE_SHA256
        and digest(compact_rows) == EXPECTED_COMPACT_PATH_SHA256,
        "path hashes",
    )
    require(
        Counter(homogeneity_labels) == Counter({"H0_CENTRAL": RETURN_DEPTH})
        and Counter(incidence_ranks) == Counter({14: RETURN_DEPTH}),
        "central rank14",
    )
    excluded_anchor_count = 1 if analytic_anchor_exclusion else 0
    require(
        set(full_histogram) == {161}
        and sum(full_histogram.values()) == RETURN_DEPTH
        and sum(full_totals.values()) + excluded_anchor_count
        == 161 * RETURN_DEPTH,
        "full census",
    )
    path_id = "round139-local-d0-adjacent-return-word-cell:" + digest([
        "round139-local-d0-adjacent-return-word-cell-v1",
        parent_id,
        object_kind,
        X_COLLAR_POWER,
        RETURN_DEPTH,
        digest(rows),
        EXPECTED_DESTINATION_CORE_ID,
    ])
    summary = {
        "object_kind": object_kind,
        "local_D0_adjacent_return_word_cell_id": path_id,
        "same_Round138_local_parent_W_id": parent_id,
        "exact_half_open_H1_collar": (
            f"[x_star-2^-{X_COLLAR_POWER},x_star)"
            if analytic_anchor_exclusion else None
        ),
        "ordinary_positive_area_rectangle": not analytic_anchor_exclusion,
        "collision3_analytic_anchor_exclusion_used": analytic_anchor_exclusion,
        "first_return_depth": RETURN_DEPTH,
        "preterminal_strict_nonreturn_collision_count": RETURN_DEPTH - 1,
        "terminal_strict_return_collision_count": 1,
        "terminal_absolute_owner_id": EXPECTED_TERMINAL_OWNER,
        "destination_core_id": EXPECTED_DESTINATION_CORE_ID,
        "collision_row_count": len(rows),
        "collision_rows_sha256": digest(rows),
        "owner_sequence_sha256": digest(owners),
        "official_word_key_sequence_sha256": digest(official_ids),
        "combined_compact_path_rows_sha256": digest(compact_rows),
        "unique_official_word_key_count": len(set(official_ids)),
        "retained_candidate_count_histogram": {
            str(key): value for key, value in sorted(retained_histogram.items())
        },
        "retained_candidate_classification_totals":
            dict(sorted(retained_totals.items())),
        "full_radius4_candidate_count_histogram": {
            str(key): value for key, value in sorted(full_histogram.items())
        },
        "full_radius4_candidate_classification_totals":
            dict(sorted(full_totals.items())),
        "full_radius4_classification_totals_exclude_primary_D0_anchor_count":
            excluded_anchor_count,
        "full_radius4_candidate_test_count": 161 * RETURN_DEPTH,
        "collision3_D0_anchor_analytic_boundary_count": excluded_anchor_count,
        "collision3_nonanchor_full_radius4_test_count":
            160 if analytic_anchor_exclusion else 161,
        "homogeneity_label_histogram": {"H0_CENTRAL": RETURN_DEPTH},
        "incidence_rank_histogram": {"14": RETURN_DEPTH},
        "all_official_words_whole_collar_strict": True,
        "all_other_owner_decisions_whole_collar_strict": True,
        "all_homogeneity_and_incidence_decisions_whole_collar_strict": True,
        "strict_first_return_whole_exact_half_open_collar":
            analytic_anchor_exclusion,
        "strict_first_return_whole_positive_area_rectangle":
            not analytic_anchor_exclusion,
    }
    return rows, summary, {
        "collision3_anchor_audits": collision3_audits,
        "strict_margin_ledger": ledger.public(),
        "compact_path_rows_sha256": digest(compact_rows),
    }


def reconstruct(precision_bits: int) -> dict[str, Any]:
    require(precision_bits >= MINIMUM_PRECISION_BITS, "precision minimum")
    ctx.prec = precision_bits
    closed = validate_dependencies()
    base.round116.init_worker(precision_bits)
    nested = base.round136.validate_dependencies()
    source, face, selected_link, strip = base.round136.selected_corrected_objects(
        nested
    )
    r138 = closed[R138_CERTIFICATE.name]
    parent_id = r138["common_same_slope4_parent_leaf"]["local_parent_W_id"]
    root, b_enclosure, root_row = deep_root_and_b(source, r138)
    collar_atom, collar_row = x_collar(
        source, root, b_enclosure, parent_id, strip
    )
    cylinder_atom, cylinder_row = positive_area_cylinder(
        source, collar_atom, b_enclosure, parent_id, strip
    )
    graph_rows, graph_summary, graph_audit = replay(
        collar_atom,
        parent_id,
        "ONE_DIMENSIONAL_EXACT_HALF_OPEN_H1_GRAPH_COLLAR",
        True,
    )
    cylinder_rows, cylinder_summary, cylinder_audit = replay(
        cylinder_atom,
        parent_id,
        "POSITIVE_AREA_FIXED_S_RECTANGLE_CYLINDER",
        False,
    )
    return {
        "closed": closed,
        "source_contract": {
            "source_core_index": base.SOURCE_CORE_INDEX,
            "source_core_id": base.step1.core_id(source),
            "source_chart": source.chart_id,
            "source_target": source.target_id,
            "selected_Round116_face_id": base.round136.SELECTED_FACE_ID,
            "selected_face_branch": [
                face["source_core_index"],
                face["second_selected_target_id"],
                face["third_candidate_id"],
                face["signed_transverse_tangency_factor_sign"],
            ],
            "selected_link_rank": base.round136.SELECTED_LINK_RANK,
            "selected_link_type": selected_link["link_type"],
        },
        "parent_id": parent_id,
        "root_row": root_row,
        "collar_row": collar_row,
        "cylinder_row": cylinder_row,
        "graph_rows": graph_rows,
        "graph_summary": graph_summary,
        "graph_audit": graph_audit,
        "cylinder_rows": cylinder_rows,
        "cylinder_summary": cylinder_summary,
        "cylinder_audit": cylinder_audit,
    }


STRICT_NONPROMOTION = {
    "local_minus_D0_adjacent_finite_return_word_cell_materialized": True,
    "local_positive_area_R1648_return_cylinder_materialized": True,
    "local_H1_d_other_strictly_positive": True,
    "local_H1_d_other_lower_bound": qstr(Q(1, 2**X_COLLAR_POWER)),
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
    "Round50_owner_key_count": 0,
    "Round54_t54_token_count": 0,
    "Round54_pi54_to_Round50_map_count": 0,
    "Round67_owned_Omega_j_record_count": 0,
    "Round67_q_j_output_count": 0,
    "N_cut_at_D0": "UNKNOWN_NOT_CERTIFIED",
    "N_acc_at_D0": "UNKNOWN_NOT_CERTIFIED",
    "A_col_at_D0": "UNKNOWN_NOT_CERTIFIED",
    "owner_law_positive_mass": "NOT_CERTIFIED",
    "global_gate5_maturity": "10/18",
    "global_complete_18_field_block_count": 0,
    "complete_18_field_block_count": 0,
    "Gate5": "NOT_CERTIFIED",
    "CM2": "NO-GO_FOR_CLAIM",
}

COUNT_LEDGER = {
    "deep_D0_root_count": 1,
    "deep_b_star_enclosure_count": 1,
    "one_sided_H1_collar_count": 1,
    "positive_area_fixed_s_rectangle_cylinder_count": 1,
    "local_D0_adjacent_return_word_cell_count": 1,
    "local_positive_area_return_cylinder_count": 1,
    "collision_row_count": 2 * RETURN_DEPTH,
    "graph_collar_collision_row_count": RETURN_DEPTH,
    "positive_area_cylinder_collision_row_count": RETURN_DEPTH,
    "preterminal_strict_nonreturn_collision_count": 2 * (RETURN_DEPTH - 1),
    "terminal_strict_return_collision_count": 2,
    "official_word_key_occurrence_count": 2 * RETURN_DEPTH,
    "retained_candidate_stage_count": 2 * RETURN_DEPTH,
    "full_radius4_candidate_stage_count": 2 * RETURN_DEPTH,
    "full_radius4_candidate_test_count": 2 * 161 * RETURN_DEPTH,
    "collision3_primary_D0_anchor_exclusion_count": 1,
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
}

STRICT_NONCLAIMS = [
    "the closed-endpoint replay is an analytic continuation of the minus branch; the tangent endpoint itself is not claimed to be a regular billiard trajectory",
    "the local d_other lower bound is intrinsic H1 arclength on one exact implicit leaf, not a global component separation",
    "the dyadic decision-value margins are not identified with H1 distance",
    "the local adjacent finite word is not a global Round35 restriction, component, rank, short cell, or image recut",
    "no Round50 owner, Round54 t54 token or pi54 map, Round67 Omega_j or q_j is materialized",
    "N_cut, N_acc, and A_col at D0 are not promoted by this local one-sided certificate",
    "Gate5 remains 10/18 with zero complete blocks and CM2 remains NO-GO_FOR_CLAIM",
]


def validate_hashed_row(row: dict[str, Any], label: str) -> None:
    body = dict(row)
    row_hash = body.pop("row_sha256", None)
    require(row_hash == digest(body), f"row closure:{label}")


def expected_clearance(dynamic: dict[str, Any]) -> dict[str, Any]:
    ledger = dynamic["graph_audit"]["strict_margin_ledger"]
    depths = {name: row["dyadic_depth"] for name, row in ledger.items()}
    worst = max(depths.values())
    ell = Q(1, 2**X_COLLAR_POWER)
    return {
        "coordinate": "intrinsic H1 arclength x",
        "one_sided_from": "minus/BYPASS side",
        "excluded_primary_boundary": {
            "boundary": "D3=0 tangency candidate W[0,0]",
            "collision_index": 3,
            "location": "x_star only",
        },
        "entire_closed_branch_continuation_replayed": True,
        "all_other_boundary_families_strict_on_closed_collar": True,
        "all_other_boundary_family_margin_depths": dict(sorted(depths.items())),
        "worst_other_decision_value_dyadic_depth": worst,
        "worst_other_decision_value_strict_lower_bound":
            qstr(base.power_of_two(-worst)),
        "decision_value_margin_is_not_an_H1_distance": True,
        "local_H1_d_other_strictly_greater_than_ell": True,
        "local_H1_d_other_lower_bound": qstr(ell),
        "local_H1_d_other_statement":
            "d_other(x_star, minus branch) > 2^-5888",
        "compactness_continuity_reason":
            "all nonanchor tests are strict on the closed length-2^-5888 collar, including its far endpoint",
        "scope": "one exact local implicit leaf and one side only",
    }


def validate_document(document: dict[str, Any], dynamic: dict[str, Any]) -> None:
    require(
        set(document) == {"schema", "result", "result_sha256"},
        "closed certificate envelope",
    )
    require(document["schema"] == CERTIFICATE_SCHEMA, "certificate schema")
    result = document["result"]
    require(type(result) is dict, "result object")
    require(document["result_sha256"] == digest(result), "result digest")
    require(
        CERTIFICATE_RESULT_SHA256 is not None
        and document["result_sha256"] == CERTIFICATE_RESULT_SHA256,
        "frozen result pin",
    )
    expected_keys = {
        "status",
        "minimum_certified_precision_bits",
        "precision_invariance_contract",
        "provenance",
        "corrected_rank3_source_contract",
        "deep_same_D0_root_and_b_star",
        "minus_D0_adjacent_H1_collar",
        "nested_positive_area_R1648_cylinder",
        "collision3_analytic_anchor_exclusion",
        "local_first_return_summary",
        "collision_rows",
        "collision_rows_sha256",
        "strict_other_boundary_margin_ledger",
        "positive_area_first_return_summary",
        "positive_area_collision_rows",
        "positive_area_collision_rows_sha256",
        "positive_area_strict_margin_ledger",
        "local_H1_one_sided_other_cut_clearance",
        "strict_local_scope",
        "strict_nonpromotion",
        "historical_global_status_preserved",
        "count_ledger",
        "strict_nonclaims",
    }
    require(set(result) == expected_keys, "closed result keys")
    require(
        result["status"]
        == "CERTIFIED_MINUS_D0_ADJACENT_H1_COLLAR_STRICT_FIRST_RETURN"
        and result["minimum_certified_precision_bits"] == MINIMUM_PRECISION_BITS,
        "status and precision",
    )
    require(
        result["precision_invariance_contract"] == {
            "runtime_precision_is_not_serialized": True,
            "primary_precision_bits": MINIMUM_PRECISION_BITS,
            "secondary_precision_bits": SECONDARY_PRECISION_BITS,
            "newton_rounding_bits_fixed": NEWTON_ROUND_BITS,
            "root_bracket_fixed_after_rounding": True,
            "b_star_and_coordinate_outers_use_fixed_dyadic_grids": True,
            "expected_identical_result_at_primary_and_secondary_precision": True,
        },
        "precision contract",
    )
    require(
        PRODUCER_SHA256 is not None
        and result["provenance"] == {
            "producer_sha256": PRODUCER_SHA256,
            "direct_Round137_Round138_sha256": dict(sorted(PINS.items())),
            "nested_Round138_dependency_sha256":
                dict(sorted(base.PINS.items())),
            "nested_Round136_dependency_sha256":
                dict(sorted(base.round136.PINS.items())),
            "temporary_spike_read": False,
            "temporary_spike_imported": False,
            "append_only": True,
            "old_artifacts_modified": False,
        },
        "provenance",
    )
    require(
        result["corrected_rank3_source_contract"] == dynamic["source_contract"],
        "source contract",
    )
    for key, expected in (
        ("deep_same_D0_root_and_b_star", dynamic["root_row"]),
        ("minus_D0_adjacent_H1_collar", dynamic["collar_row"]),
        ("nested_positive_area_R1648_cylinder", dynamic["cylinder_row"]),
    ):
        validate_hashed_row(result[key], key)
        require(result[key] == expected, f"dynamic row:{key}")
    require(
        result["collision_rows"] == dynamic["graph_rows"]
        and result["collision_rows_sha256"] == digest(dynamic["graph_rows"])
        and result["positive_area_collision_rows"] == dynamic["cylinder_rows"]
        and result["positive_area_collision_rows_sha256"]
        == digest(dynamic["cylinder_rows"]),
        "collision groups",
    )
    for group in ("collision_rows", "positive_area_collision_rows"):
        rows = result[group]
        require(
            len(rows) == RETURN_DEPTH
            and [row["collision_index"] for row in rows]
            == list(range(1, RETURN_DEPTH + 1)),
            f"collision sequence:{group}",
        )
        for row in rows:
            validate_hashed_row(row, group)
            key = row["official_word_key"]
            require(
                key["registry_row_sha256"] == digest(key["registry_row"])
                and key["official_word_key_id"]
                == f"gate5-word:{key['ordinal_zero_based']:06d}:"
                f"{key['registry_row_sha256']}",
                f"official key closure:{group}",
            )
    require(
        result["local_first_return_summary"] == dynamic["graph_summary"]
        and result["positive_area_first_return_summary"]
        == dynamic["cylinder_summary"]
        and result["strict_other_boundary_margin_ledger"]
        == dynamic["graph_audit"]["strict_margin_ledger"]
        and result["positive_area_strict_margin_ledger"]
        == dynamic["cylinder_audit"]["strict_margin_ledger"],
        "summaries and ledgers",
    )
    graph_audits = dynamic["graph_audit"]["collision3_anchor_audits"]
    require(
        result["collision3_analytic_anchor_exclusion"] == {
            "collision_index": 3,
            "anchor_candidate": ANCHOR,
            "anchor_is_D3_discriminant": True,
            "exact_D3_zero_only_at_excluded_endpoint_x_star": True,
            "exact_half_open_minus_collar_has_anchor_discriminant_negative": True,
            "anchor_excluded_only_from_closed_branch_continuation_at_collision3":
                True,
            "anchor_not_deleted_from_any_other_stage_or_global_registry": True,
            "actual_regular_trajectory_at_x_star_claimed": False,
            "minus_branch_owner": EXPECTED_MINUS_OWNER,
            "retained_audit": graph_audits["retained"],
            "full_radius4_audit": graph_audits["full_radius4"],
        },
        "anchor exclusion contract",
    )
    require(
        result["local_H1_one_sided_other_cut_clearance"]
        == expected_clearance(dynamic),
        "local d_other clearance",
    )
    ell = qstr(Q(1, 2**X_COLLAR_POWER))
    require(
        result["strict_local_scope"] == {
            "same_Round138_local_parent_W_id": dynamic["parent_id"],
            "same_exact_D0_root": True,
            "same_exact_implicit_b_star": True,
            "one_sided_exact_leaf_graph_collar_count": 1,
            "positive_area_fixed_s_rectangle_cylinder_count": 1,
            "H1_collar_length": ell,
            "fixed_finite_return_word_cell_count": 2,
            "first_return_depth": RETURN_DEPTH,
            "radius4_candidate_universe_size_per_stage": 161,
            "radius4_stage_count": RETURN_DEPTH,
            "local_d_other_positive": True,
        },
        "local scope",
    )
    require(result["strict_nonpromotion"] == STRICT_NONPROMOTION, "nonpromotion")
    require(result["count_ledger"] == COUNT_LEDGER, "count ledger")
    require(result["strict_nonclaims"] == STRICT_NONCLAIMS, "strict nonclaims")
    r137 = dynamic["closed"][R137_CERTIFICATE.name]
    r138 = dynamic["closed"][R138_CERTIFICATE.name]
    require(
        result["historical_global_status_preserved"] == {
            "Round137_gate5_global_maturity":
                r137["strict_nonpromotion"]["gate5_global_maturity"],
            "Round138_gate5_global_maturity":
                r138["strict_nonpromotion"]["global_gate5_maturity"],
            "Round138_global_complete_18_field_block_count":
                r138["strict_nonpromotion"][
                    "global_complete_18_field_block_count"
                ],
            "Round138_CM2": r138["strict_nonpromotion"]["CM2"],
            "no_historical_or_global_status_upgraded": True,
        },
        "historical status",
    )


def resign(document: dict[str, Any]) -> None:
    document["result_sha256"] = digest(document["result"])


def set_path(document: dict[str, Any], path: tuple[Any, ...], value: Any) -> None:
    target: Any = document
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    resign(document)


def semantic_mutations(
    certificate: dict[str, Any],
    dynamic: dict[str, Any],
) -> list[str]:
    attacks = [
        ("status promotion", ("result", "status"), "CERTIFIED_CM2"),
        ("precision lowered", ("result", "minimum_certified_precision_bits"), 1),
        ("root uniqueness removed", ("result", "deep_same_D0_root_and_b_star", "deep_D0_unique"), False),
        ("collar power altered", ("result", "minus_D0_adjacent_H1_collar", "x_collar_power"), 1),
        ("positive area removed", ("result", "nested_positive_area_R1648_cylinder", "positive_area"), False),
        ("anchor made regular", ("result", "collision3_analytic_anchor_exclusion", "actual_regular_trajectory_at_x_star_claimed"), True),
        ("graph return depth altered", ("result", "local_first_return_summary", "first_return_depth"), 1647),
        ("2d return depth altered", ("result", "positive_area_first_return_summary", "first_return_depth"), 1647),
        ("graph owner altered", ("result", "collision_rows", 0, "selected_absolute_owner_id"), "G[9,9]"),
        ("2d owner altered", ("result", "positive_area_collision_rows", 2, "selected_absolute_owner_id"), ANCHOR),
        ("full count altered", ("result", "collision_rows", 100, "full_radius4_candidate_count"), 160),
        ("official ordinal altered", ("result", "collision_rows", 51, "official_word_key", "ordinal_zero_based"), 18715),
        ("d_other promoted globally", ("result", "local_H1_one_sided_other_cut_clearance", "scope"), "global"),
        ("Round35 restriction promoted", ("result", "strict_nonpromotion", "global_Round35_restriction_materialized"), True),
        ("owner promoted", ("result", "strict_nonpromotion", "Round50_owner_key_count"), 1),
        ("t54 promoted", ("result", "strict_nonpromotion", "Round54_t54_token_count"), 1),
        ("Omega promoted", ("result", "strict_nonpromotion", "Round67_owned_Omega_j_record_count"), 1),
        ("qj promoted", ("result", "strict_nonpromotion", "Round67_q_j_output_count"), 1),
        ("N_cut promoted", ("result", "strict_nonpromotion", "N_cut_at_D0"), True),
        ("A_col promoted", ("result", "strict_nonpromotion", "A_col_at_D0"), False),
        ("Gate5 promoted", ("result", "strict_nonpromotion", "global_gate5_maturity"), "18/18"),
        ("block promoted", ("result", "strict_nonpromotion", "global_complete_18_field_block_count"), 1),
        ("CM2 promoted", ("result", "strict_nonpromotion", "CM2"), "GO_FOR_CLAIM"),
        ("test count altered", ("result", "count_ledger", "full_radius4_candidate_test_count"), 1),
    ]
    rejected: list[str] = []
    for label, path, value in attacks:
        mutated = copy.deepcopy(certificate)
        set_path(mutated, path, value)
        try:
            validate_document(mutated, dynamic)
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
    require(len(rejected) == len(attacks) == 24, "24 semantic attacks")
    return rejected


def strict_json_attacks(
    certificate: dict[str, Any],
    dynamic: dict[str, Any],
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
    ).encode()
    attacks: list[tuple[str, bytes]] = []

    def add(label: str, payload: bytes) -> None:
        require(payload != raw, f"attack construction:{label}")
        attacks.append((label, payload))

    add("duplicate top schema", raw.replace(b'{\n  "result":', b'{\n  "schema":"x",\n  "result":', 1))
    add("duplicate nested status", raw.replace(b'"status": "CERTIFIED_MINUS_D0_ADJACENT_H1_COLLAR_STRICT_FIRST_RETURN"', b'"status":"x","status": "CERTIFIED_MINUS_D0_ADJACENT_H1_COLLAR_STRICT_FIRST_RETURN"', 1))
    add("duplicate collision index", raw.replace(b'"collision_index": 1,', b'"collision_index":0,"collision_index": 1,', 1))
    add("floating count", raw.replace(b'"collision_row_count": 3296', b'"collision_row_count": 3296.0', 1))
    add("NaN", raw.replace(b'"collision_row_count": 3296', b'"collision_row_count": NaN', 1))
    add("Infinity", raw.replace(b'"collision_row_count": 3296', b'"collision_row_count": Infinity', 1))
    add("-Infinity", raw.replace(b'"collision_row_count": 3296', b'"collision_row_count": -Infinity', 1))
    add("UTF-8 BOM", b"\xef\xbb\xbf" + raw)
    add("invalid UTF-8", raw[:20] + b"\xff" + raw[20:])
    add("top array", b"[]")
    add("top null", b"null")
    add("trailing document", raw + b"{}")
    add("oversized integer", raw.replace(b'"collision_row_count": 3296', b'"collision_row_count": ' + b"9" * (MAX_INTEGER_DIGITS + 1), 1))
    add("negative zero", raw.replace(b'"collision_row_count": 3296', b'"collision_row_count": -0', 1))
    add("leading zero", raw.replace(b'"collision_row_count": 3296', b'"collision_row_count": 03296', 1))
    add("unpaired surrogate", raw.replace(b'"CERTIFIED_MINUS_D0_ADJACENT_H1_COLLAR_STRICT_FIRST_RETURN"', b'"\\ud800"', 1))
    extra = copy.deepcopy(certificate)
    extra["unknown"] = True
    add("extra envelope key", (json.dumps(extra, sort_keys=True) + "\n").encode())
    extra = copy.deepcopy(certificate)
    extra["result"]["unknown"] = True
    resign(extra)
    add("extra result key", (json.dumps(extra, sort_keys=True) + "\n").encode())
    stale = copy.deepcopy(certificate)
    stale["result"]["strict_nonpromotion"]["CM2"] = "GO_FOR_CLAIM"
    add("stale digest", (json.dumps(stale, sort_keys=True) + "\n").encode())
    rejected: list[str] = []
    for label, payload in attacks:
        try:
            document = strict_json_bytes(payload, label)
            validate_document(document, dynamic)
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
            raise VerificationError(f"strict attack accepted:{label}")
    require(len(rejected) == len(attacks) == 19, "19 strict attacks")
    return rejected


def regular_single_link(path: Path, label: str) -> None:
    require(path.is_file(), f"missing regular file:{label}")
    require(not path.is_symlink(), f"symlink file:{label}")
    metadata = path.lstat()
    require(
        stat.S_ISREG(metadata.st_mode) and metadata.st_nlink == 1,
        f"single-link regular file:{label}",
    )


def safe_input_path(path: Path) -> Path:
    require(CERTIFICATE_SHA256 is not None, "certificate pin frozen")
    expanded = path.expanduser()
    regular_single_link(expanded, "certificate")
    require(
        expanded.stat().st_size <= MAX_CERTIFICATE_BYTES,
        "certificate size limit",
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
        *((HERE / name).resolve() for name in base.PINS),
        *((HERE / name).resolve() for name in base.round136.PINS),
    }
    require(not expanded.is_symlink(), "output symlink")
    require(not expanded.parent.is_symlink(), "output parent symlink")
    if expanded.exists():
        metadata = expanded.lstat()
        require(
            stat.S_ISREG(metadata.st_mode) and metadata.st_nlink == 1,
            "existing output regular single-link",
        )
        for item in protected:
            try:
                require(
                    not os.path.samefile(expanded, item),
                    "output hardlinks protected input",
                )
            except FileNotFoundError:
                pass
    resolved = expanded.resolve()
    require(
        resolved not in protected
        and resolved.parent.is_dir()
        and not resolved.parent.is_symlink(),
        "safe output target",
    )
    return resolved


def path_safety_self_tests(certificate_path: Path) -> list[str]:
    labels: list[str] = []

    def reject(label: str, action: Callable[[], Any]) -> None:
        try:
            action()
        except (VerificationError, OSError):
            labels.append(label)
        else:
            raise VerificationError(f"path attack accepted:{label}")

    with tempfile.TemporaryDirectory(prefix="cm2-r139-path-") as name:
        root = Path(name)
        copied = root / "certificate.json"
        copied.write_bytes(certificate_path.read_bytes())
        require(safe_input_path(copied) == copied.resolve(), "valid copy")
        reject("missing certificate", lambda: safe_input_path(root / "missing"))
        symlink = root / "input-symlink"
        symlink.symlink_to(copied)
        reject("input symlink", lambda: safe_input_path(symlink))
        hardlink = root / "input-hardlink"
        os.link(copied, hardlink)
        reject("input hardlink", lambda: safe_input_path(copied))
        hardlink.unlink()
        tampered = root / "tampered"
        tampered.write_bytes(certificate_path.read_bytes() + b" ")
        reject("tampered input", lambda: safe_input_path(tampered))
        reject("output certificate", lambda: safe_output_path(CERTIFICATE, copied))
        reject("output selected input", lambda: safe_output_path(copied, copied))
        reject("output producer", lambda: safe_output_path(PRODUCER, copied))
        reject("output verifier", lambda: safe_output_path(VERIFIER, copied))
        reject(
            "output pinned upstream",
            lambda: safe_output_path(HERE / sorted(PINS)[0], copied),
        )
        output_symlink = root / "output-symlink"
        output_symlink.symlink_to(copied)
        reject("output symlink", lambda: safe_output_path(output_symlink, copied))
        output_hardlink = root / "output-hardlink"
        os.link(copied, output_hardlink)
        reject(
            "output hardlink", lambda: safe_output_path(output_hardlink, copied)
        )
        output_hardlink.unlink()
        directory = root / "directory"
        directory.mkdir()
        reject("output directory", lambda: safe_output_path(directory, copied))
        real_parent = root / "real"
        real_parent.mkdir()
        linked_parent = root / "linked"
        linked_parent.symlink_to(real_parent, target_is_directory=True)
        reject(
            "output parent symlink",
            lambda: safe_output_path(linked_parent / "out", copied),
        )
        fresh = root / "fresh"
        require(safe_output_path(fresh, copied) == fresh.resolve(), "fresh output")
    require(len(labels) == 13, "13 path attacks")
    return labels


def build_verification(
    dynamic: dict[str, Any],
    semantic_labels: list[str],
    strict_labels: list[str],
    path_labels: list[str],
) -> dict[str, Any]:
    return {
        "status": "PASS",
        "verifier_sha256": sha256(VERIFIER),
        "producer_sha256": PRODUCER_SHA256,
        "certificate_sha256": CERTIFICATE_SHA256,
        "certificate_schema": CERTIFICATE_SCHEMA,
        "certificate_result_sha256": CERTIFICATE_RESULT_SHA256,
        "independence_contract": {
            "Round139_producer_imported": False,
            "Round139_producer_executed": False,
            "temporary_spike_read": False,
            "deep_D0_root_and_b_star_independently_rebuilt": True,
            "H1_graph_collar_and_positive_area_rectangle_rebuilt": True,
            "all_3296_collision_rows_independently_rebuilt": True,
            "all_3296_retained_candidate_searches_rebuilt": True,
            "all_3296_full_radius4_161_candidate_searches_rebuilt": True,
            "collision3_half_open_anchor_semantics_independently_checked": True,
            "official_words_homogeneity_incidence_and_C24_rebuilt": True,
            "local_d_other_scope_and_nonpromotion_checked": True,
        },
        "replay_audit": {
            "graph_collar_first_return_depth":
                dynamic["graph_summary"]["first_return_depth"],
            "positive_area_first_return_depth":
                dynamic["cylinder_summary"]["first_return_depth"],
            "destination_core_id": EXPECTED_DESTINATION_CORE_ID,
            "graph_collision_rows_sha256":
                dynamic["graph_summary"]["collision_rows_sha256"],
            "positive_area_collision_rows_sha256":
                dynamic["cylinder_summary"]["collision_rows_sha256"],
            "owner_sequence_sha256": EXPECTED_OWNER_SEQUENCE_SHA256,
            "official_word_sequence_sha256":
                EXPECTED_OFFICIAL_SEQUENCE_SHA256,
            "full_radius4_stage_count": 2 * RETURN_DEPTH,
            "full_radius4_candidate_test_count": 2 * 161 * RETURN_DEPTH,
            "local_H1_d_other_lower_bound":
                qstr(Q(1, 2**X_COLLAR_POWER)),
        },
        "dual_precision_consistency": {
            "primary_precision_bits": MINIMUM_PRECISION_BITS,
            "secondary_precision_bits": SECONDARY_PRECISION_BITS,
            "complete_dynamic_reconstruction_equal": True,
        },
        "semantic_mutation_test_count": len(semantic_labels),
        "semantic_mutation_rejection_labels": semantic_labels,
        "strict_json_attack_count": len(strict_labels),
        "strict_json_attack_rejection_labels": strict_labels,
        "path_safety_self_test_count": len(path_labels),
        "path_safety_rejection_labels": path_labels,
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
        with os.fdopen(
            descriptor, "w", encoding="utf-8", newline="\n"
        ) as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    require(PRODUCER_SHA256 is not None, "producer pin frozen")
    require(CERTIFICATE_SHA256 is not None, "certificate pin frozen")
    require(CERTIFICATE_RESULT_SHA256 is not None, "result pin frozen")
    regular_single_link(PRODUCER, PRODUCER.name)
    require(sha256(PRODUCER) == PRODUCER_SHA256, "producer byte pin")
    regular_single_link(VERIFIER, VERIFIER.name)
    certificate_path = safe_input_path(args.certificate)
    output_path = safe_output_path(args.output, certificate_path)
    certificate = strict_json(certificate_path)
    primary = reconstruct(MINIMUM_PRECISION_BITS)
    validate_document(certificate, primary)
    secondary = reconstruct(SECONDARY_PRECISION_BITS)
    require(
        {
            key: value
            for key, value in primary.items()
            if key != "closed"
        }
        == {
            key: value
            for key, value in secondary.items()
            if key != "closed"
        },
        "primary/secondary dynamic invariance",
    )
    semantic_labels = semantic_mutations(certificate, primary)
    strict_labels = strict_json_attacks(certificate, primary)
    path_labels = path_safety_self_tests(certificate_path)
    result = build_verification(
        primary, semantic_labels, strict_labels, path_labels
    )
    document = {
        "schema": VERIFICATION_SCHEMA,
        "result": result,
        "result_sha256": digest(result),
    }
    write_document(output_path, document)
    print(canonical({
        "output": str(output_path),
        "result_sha256": document["result_sha256"],
        "semantic_mutations": len(semantic_labels),
        "strict_json_attacks": len(strict_labels),
        "path_safety_tests": len(path_labels),
        "status": "PASS",
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
