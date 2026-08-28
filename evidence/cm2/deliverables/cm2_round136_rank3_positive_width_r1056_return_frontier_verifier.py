#!/usr/bin/env python3
"""Independent fail-closed verifier for the Round136 R1056 frontier.

The Round136 producer is byte pinned but is never imported or executed here.
This verifier independently rebuilds the rational source box, all 1056
complete-candidate collision decisions, translation-normalized official
registry words, C24 first-return classifications, countable homogeneity
labels, whole-box incidence ranks, strict margin ledger, typed occurrence
singleton, census, and every nonpromotion boundary.

The certified object remains one positive-area *local* R1056 cylinder.  No
canonical c24-component, Round35 restriction, Round50 owner, Round54 token,
Round67 q_j output, global Gate5 block, or CM2 claim is created.
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
import cm2_gate34_round28_nonempty_adaptive_component_registry_cert as component_cert
import cm2_gate34_round29_q2_time3_anchor_registry_cert as time3
import cm2_round89_rank3_projective_gap_closure_cert as round89
import cm2_round116_rank3_interior_two_sided_transverse_collar as round116
import cm2_round117_rank3_countable_homogeneity_operator_cells as round117
from cm2_round79_tangency_intersection_generator import aq, strict_sign
from cm2_round80_time3_tangency_curve_generator import third_tangency_jet


HERE = Path(__file__).resolve().parent
VERIFIER = Path(__file__).resolve()
PRODUCER = HERE / "cm2_round136_rank3_positive_width_r1056_return_frontier.py"
CERTIFICATE = (
    HERE
    / "cm2-round136-rank3-positive-width-r1056-return-frontier-2026-07-24.json"
)
OUTPUT = (
    HERE
    / "cm2-round136-rank3-positive-width-r1056-return-frontier-verification-2026-07-24.json"
)
CERTIFICATE_SCHEMA = "cm2.round136.rank3-positive-width-r1056-return-frontier.v1"
VERIFICATION_SCHEMA = (
    "cm2.round136.rank3-positive-width-r1056-return-frontier-verification.v1"
)
PRODUCER_SHA256 = (
    "4e78309d5275bf367e6df03509c40ebaaac6f344c7948446a25b3b508c8c2bc2"
)
CERTIFICATE_SHA256 = (
    "d9b7b7823dddce2dcbc16412294c8ecef42b304712d4bb968896d2221b8aa7f9"
)
CERTIFICATE_RESULT_SHA256 = (
    "407bc2dbecaacb2ed8527a3fe8a41f97ed523a43f428c37b76e14639425cf545"
)
PRECISION_BITS = 8192
SECONDARY_PRECISION_BITS = 12288
MAX_CERTIFICATE_BYTES = 4_000_000
MAX_INTEGER_DIGITS = 10_000

LOCATOR_BISECTIONS = 1500
SOURCE_BOX_HALF_WIDTH_BITS = 3815
RETURN_DEPTH = 1056
SELECTED_FACE_ID = (
    "physical-s0-rank3-corrected-face:"
    "02a116578e4b096df6c1575632590e5e6202442803da780fb13cdb6ff1026773"
)
SELECTED_LINK_RANK = 1
SELECTED_STRIP_INDEX = 128
SOURCE_CORE_INDEX = 14
SOURCE_ABSOLUTE_OWNER = "W[0,0]"
SECOND_OWNER = "G[0,1]"
DESIGNATED_THIRD_OWNER = "W[0,0]"
SOURCE_P_CENTER = Q(-1587, 1638400)
CONSTRUCTION_COSINE = Q(1, 2**64)
TARGET_RADIUS = Q(4, 25)
TARGET_RADIUS_SQUARED = Q(16, 625)
LOCATOR_INITIAL_T_INTERVAL = (Q(19, 1000), Q(1, 50))
EXPECTED_TAIL_LABEL_INDEX = 2**32 - 1
EXPECTED_DESTINATION_CORE_ID = (
    "core:d6e30c5e3160559018e3ed757ec6d3fc12eb97cbd9d9673c7907621b2fe97ee8"
)
EXPECTED_SOURCE_CORE_ID = (
    "core:90398e9ab632e57b027266bc7c34461a0a6a6d308c35fbeacc41432a3d7f48f7"
)
OFFICIAL_REGISTRY_STREAM_SHA256 = (
    "841cb96798c9bd41e1440c8b2cdd93af5d80f2f64d693f2aa00175a440045ab9"
)

ROUND99 = HERE / "cm2-round99-rank3-registered-port-candidate-audit-2026-07-22.json"
ROUND99V = (
    HERE
    / "cm2-round99-rank3-registered-port-candidate-verification-2026-07-22.json"
)
ROUND100 = HERE / "cm2-round100-rank3-immutable-interior-gap-closure-2026-07-22.json"
ROUND100V = (
    HERE / "cm2-round100-rank3-immutable-interior-gap-verification-2026-07-22.json"
)
ROUND102 = HERE / "cm2-round102-rank3-corrected-face-quotient-2026-07-22.json"
ROUND102V = (
    HERE
    / "cm2-round102-rank3-corrected-face-quotient-verification-2026-07-22.json"
)
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
ROUND132 = (
    HERE / "cm2-round132-round28-occurrence-record-materialization-2026-07-24.json"
)
ROUND132V = (
    HERE
    / "cm2-round132-round28-occurrence-record-materialization-verification-2026-07-24.json"
)
ROUND133 = (
    HERE / "cm2-round133-round132-owner-map-realizability-audit-2026-07-24.json"
)
ROUND133V = (
    HERE
    / "cm2-round133-round132-owner-map-realizability-audit-verification-2026-07-24.json"
)
ROUND27 = (
    HERE / "cm2-gate34-round27-arbitrary-n-path-schema-manifest-2026-07-18.json"
)
ROUND35 = (
    HERE / "cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json"
)
ROUND50 = (
    HERE / "cm2-gate5-round50-owner-boundary-zb-f17-frontier-manifest-2026-07-19.json"
)
ROUND54 = (
    HERE
    / "cm2-gate5-round54-collar-pairing-directional-bv-frontier-manifest-2026-07-20.json"
)
ROUND60 = (
    HERE
    / "cm2-gate5-round60-owner-trace-suffix-positive-anchor-frontier-manifest-2026-07-20.json"
)
ROUND67 = (
    HERE
    / "cm2-round67-fixed-j-occurrence-owner-root-time-potential-frontier-manifest-2026-07-21.json"
)

PINS = {
    "cm2_round79_tangency_intersection_generator.py":
        "971f918ca1ed23bd081adf3b233d578e750b61231b20113327f221b40b890ed7",
    "cm2_round80_time3_tangency_curve_generator.py":
        "68d17d088e94a8d5b0b97a6518691e19da2560be7df7fcff32eacdfd367aa659",
    "cm2_round89_rank3_projective_gap_closure_cert.py":
        "6b5706fe16bd9a9142e64fbd227b32b6a2cfdc13d90d362c76fd33eca6874daf",
    "cm2_round116_rank3_interior_two_sided_transverse_collar.py":
        "91ea057ad31517ce6b390561e9b894e219a837fa3a3be793fc96db082566f3f7",
    "cm2_round117_rank3_countable_homogeneity_operator_cells.py":
        "8112aeb2c5d67a914a651683c9a497def3c2ffed81b1c42b365bb257cf8f7e7c",
    "cm2_gate25_physical_return_core_registry_cert.py":
        "2da58e5fb5fe030023d6fade7252ec67d0e494708b32d1e32b3ce545e2052fdb",
    "cm2_gate34_full_core_return_adaptive_frontier_cert.py":
        "d18b234471b192282abf064684fa535cc99c205797399b268f052c0884063a24",
    "cm2_gate34_round28_nonempty_adaptive_component_registry_cert.py":
        "b489f498cac2650a6456da0540d035b2cc9654a69f5dc0110db85933eecd12f6",
    "cm2_gate34_round29_q2_time3_anchor_registry_cert.py":
        "399ea86401e97d2679fb3f3f7a0a9328266d8d583e73fd5c5ed2bc811c14475b",
    ROUND99.name:
        "e1f0ea00d48e9eae553d5bb24ce140d27f696fd071cb19270e023263aac32f5e",
    ROUND99V.name:
        "c084ff487f9f9e03ff2ca999243addb72cf3abd42772f4e18bd5258edb9d5c41",
    ROUND100.name:
        "097849bf3da9d34a83ce9693ca68093ed2de7460cc51dcb26ce484c589f278d6",
    ROUND100V.name:
        "d94232b61685256a118484a4e76c01dbf6d56a7ed98efcca1b84397c907b3982",
    ROUND102.name:
        "85069546fbc29f45af93eb65e2c2979bc83bfb5d744199771e234c2f7a1f0edb",
    ROUND102V.name:
        "74ed17140572d772743387d9518bc0cde25ed878673a3c5f8d4737e7401852d6",
    ROUND116.name:
        "504e070eea10fbab3b1968423ecedcda6fa8fc20549adb9ef3e9ed42bd2c45b3",
    ROUND116V.name:
        "6e12d118c7955bd0405c79dcf7b9de40df56f3eba6bc96ee6c1078898a038750",
    ROUND117.name:
        "31b6535e21886d825d5a4658f2c9d3ccc8c5525c2b9d2fb181f88baa7dcf9eb0",
    ROUND117V.name:
        "06647b5b6f81ad0e8098f5885e9aa2b2c926991faaa34102e0646c058da0764f",
    ROUND132.name:
        "b5d09c7398dae4b77a6f011430286f88539e0f13ca449e50eb84fc3712d67d31",
    ROUND132V.name:
        "26ef83ceb2aa484388e99a4f832670c7e13429452aec7a56945d2db4cb97f171",
    ROUND133.name:
        "a020ce376c1398384e5f304aff320aa214721f5f8d8bcc1e35bfa31eadd54c91",
    ROUND133V.name:
        "f41a45baf3cffab63a3429b66c2f3c9473394024a4ae4c9a234df13e3410794f",
    ROUND27.name:
        "988f364bd1e6943178238c072e725de01af36452ef25d179eae6aef4000f7916",
    ROUND35.name:
        "ece7c97beeeb0b527434dc430e247ad0af407dc58b82d634da9e34a2f9e9521c",
    ROUND50.name:
        "c848c67bb9f2c0793d793c2ab4dca754cad71c507b9f0a06b9c29be3eaafeb46",
    ROUND54.name:
        "87e052dbfc369195becc5f2d4ac641c8250d72266bb73f47281b8b923d584ab5",
    ROUND60.name:
        "d519ad15a870fe7820839828347140e4bae3b5752a95fab4c18263c67e2ab778",
    ROUND67.name:
        "97cb410b9e960d8331a37ef9203b040c9b1d86c3ed3d1ba6ba66a28c4e4ff400",
}

CLOSED_SCHEMAS = {
    ROUND99.name: "cm2.round99.rank3-registered-port-candidate-audit.v1",
    ROUND99V.name:
        "cm2.round99.rank3-registered-port-candidate-audit-verification.v1",
    ROUND100.name: "cm2.round100.rank3-immutable-interior-gap-closure.v1",
    ROUND100V.name:
        "cm2.round100.rank3-immutable-interior-gap-verification.v1",
    ROUND102.name: "cm2.round102.rank3-corrected-face-quotient.v1",
    ROUND102V.name:
        "cm2.round102.rank3-corrected-face-quotient-verification.v1",
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
    ROUND133.name:
        "cm2.round133.round132-owner-map-realizability-audit.v1",
    ROUND133V.name:
        "cm2.round133.round132-owner-map-realizability-audit-verification.v1",
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
        stat.S_ISREG(metadata.st_mode) and metadata.st_nlink == 1,
        f"unsafe input type:{path.name}",
    )
    require(not path.is_symlink(), f"input symlink:{path.name}")
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
            ROUND99,
            ROUND99V,
            ROUND100,
            ROUND100V,
            ROUND102,
            ROUND102V,
            ROUND116,
            ROUND116V,
            ROUND117,
            ROUND117V,
            ROUND132,
            ROUND132V,
            ROUND133,
            ROUND133V,
        )
    }
    for path in (
        ROUND99V,
        ROUND100V,
        ROUND102V,
        ROUND116V,
        ROUND117V,
        ROUND132V,
        ROUND133V,
    ):
        require(verification_passed(closed[path.name]), f"verification PASS:{path.name}")
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


class MarginLedger:
    def __init__(self) -> None:
        self.depths: dict[str, int] = {}
        self.counts: Counter[str] = Counter()
        self.minimum_lowers: dict[str, Q] = {}
        self.minimum_uppers: dict[str, Q] = {}
        self.minimum_witnesses: dict[str, dict[str, Any] | None] = {}

    def observe(
        self,
        name: str,
        value: arb,
        witness: dict[str, Any] | None = None,
    ) -> int:
        lower, upper = arb_pair(value)
        depth = strict_dyadic_depth(value, lower)
        self.depths[name] = max(self.depths.get(name, -100000), depth)
        self.counts[name] += 1
        if name not in self.minimum_lowers or lower < self.minimum_lowers[name]:
            self.minimum_lowers[name] = lower
            self.minimum_uppers[name] = upper
            self.minimum_witnesses[name] = witness
        return depth

    def public(self) -> dict[str, Any]:
        return {
            name: {
                "dyadic_depth": depth,
                "strict_lower_bound": qstr(power_of_two(-depth)),
                "observation_count": self.counts[name],
                "minimum_observed_interval_exact_dyadic": [
                    qstr(self.minimum_lowers[name]),
                    qstr(self.minimum_uppers[name]),
                ],
                "minimum_observed_witness": self.minimum_witnesses[name],
            }
            for name, depth in sorted(self.depths.items())
        }


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


def translation_normalized_official_word(
    state: dict[str, Any],
    current_target: str,
    owner: dict[str, Any],
    pair_index: dict[tuple[str, str], int],
    pattern_index: dict[tuple[str, ...], int],
) -> tuple[dict[str, Any] | None, str | None]:
    """Rebuild an official word after removing the current lattice shift."""

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
        "absolute_selected_target_id": owner["selected_target_id"],
        "relative_frozen_target_id": target,
        "ordered_clean_wall_record": list(crossings),
        "absolute_lattice_translation_removed": [shift_x, shift_y],
        "translation_normalization_preserves_wall_word": True,
    }, None


def selected_corrected_objects(
    closed: dict[str, dict[str, Any]],
) -> tuple[Any, dict[str, Any], dict[str, Any], tuple[Q, Q, Q, Q]]:
    r99 = closed[ROUND99.name]
    r100 = closed[ROUND100.name]
    r102 = closed[ROUND102.name]
    r116 = closed[ROUND116.name]
    require(
        r99["corrected_locally_physical_port_count"] == 120
        and len(set(r99["corrected_locally_physical_registered_port_ids"])) == 120,
        "Round99 corrected port census",
    )
    face_rows = [
        row for row in r102["face_rows"] if row["face_id"] == SELECTED_FACE_ID
    ]
    require(len(face_rows) == 1, "selected corrected face")
    face = face_rows[0]
    require(
        [
            face["source_core_index"],
            face["second_selected_target_id"],
            face["third_candidate_id"],
            face["signed_transverse_tangency_factor_sign"],
        ]
        == [SOURCE_CORE_INDEX, SECOND_OWNER, DESIGNATED_THIRD_OWNER, 1],
        "selected face branch",
    )
    links = [
        row
        for row in r102["interior_link_rows"]
        if row["face_id"] == SELECTED_FACE_ID
        and row["link_rank"] == SELECTED_LINK_RANK
    ]
    require(len(links) == 1, "selected corrected link")
    link = links[0]
    require(
        link["link_type"] == "IMMUTABLE_CERTIFIED_INTERIOR_GAP",
        "selected corrected gap type",
    )
    endpoint_pair = frozenset(
        (link["left_registered_port_id"], link["right_registered_port_id"])
    )
    gaps = [
        row
        for row in r100["gap_rows"]
        if frozenset(
            (row["left_registered_port_id"], row["right_registered_port_id"])
        )
        == endpoint_pair
    ]
    require(len(gaps) == 1, "selected Round100 gap")
    gap = gaps[0]
    require(
        gap["source_core_index"] == SOURCE_CORE_INDEX
        and gap["second_selected_target_id"] == SECOND_OWNER
        and gap["third_candidate_id"] == DESIGNATED_THIRD_OWNER
        and gap["signed_transverse_tangency_factor_sign"] == 1
        and gap["immutable_candidate_reaudit_method"] == "WHOLE_TUBE_IFT_CHAIN"
        and gap["strip_count"] == 256,
        "selected gap semantics",
    )
    collars = [
        row
        for row in r116["interior_link_rows"]
        if row["face_id"] == SELECTED_FACE_ID
        and row["link_rank"] == SELECTED_LINK_RANK
    ]
    require(len(collars) == 1, "selected Round116 collar")
    collar = collars[0]
    require(
        collar["relative_interior_full_two_sided_collar_certified"] is True
        and collar["complete_candidate_owner_constancy_certified"] is True
        and collar["residual_strip_count"] == 0
        and collar["tangent_strip_count"] == 256,
        "selected Round116 whole collar",
    )
    event_rows, _pairs = round89.load()
    by_id = {row["registered_port_id"]: row for row in event_rows}
    left = by_id[link["left_registered_port_id"]]
    right = by_id[link["right_registered_port_id"]]
    source = core_cert.physical_cores()[SOURCE_CORE_INDEX]
    boxes = round116.standard_boxes(
        left,
        right,
        source,
        gap["strip_count"],
        gap["dependent_collar_depth"],
    )
    require(len(boxes) == 256, "materialized Round116 strips")
    strip = boxes[SELECTED_STRIP_INDEX]
    require(
        strip[2] < SOURCE_P_CENTER < strip[3],
        "source p center strictly inside strip 128",
    )
    return source, face, {**link, "round100_gap": gap, "round116_collar": collar}, strip


def construction_and_source_box(
    source: Any,
    strip: tuple[Q, Q, Q, Q],
) -> tuple[step1.Atom, dict[str, Any]]:
    require(
        TARGET_RADIUS_SQUARED == TARGET_RADIUS * TARGET_RADIUS,
        "W target radius square identity",
    )
    target_shift = aq(TARGET_RADIUS_SQUARED * CONSTRUCTION_COSINE**2)

    def shifted_value(t_value: Q) -> arb:
        return (
            third_tangency_jet(
                source,
                SECOND_OWNER,
                DESIGNATED_THIRD_OWNER,
                t_value,
                t_value,
                SOURCE_P_CENTER,
                SOURCE_P_CENTER,
            ).value
            - target_shift
        )

    lower, upper = LOCATOR_INITIAL_T_INTERVAL
    require(
        strict_sign(shifted_value(lower)) == -1
        and strict_sign(shifted_value(upper)) == 1,
        "construction locator face signs",
    )
    for _index in range(LOCATOR_BISECTIONS):
        middle = (lower + upper) / 2
        sign = strict_sign(shifted_value(middle))
        require(sign in (-1, 1), "construction midpoint strict sign")
        if sign < 0:
            lower = middle
        else:
            upper = middle
    t_seed = lower
    half_width = Q(1, 2**SOURCE_BOX_HALF_WIDTH_BITS)
    t0, t1 = t_seed - half_width, t_seed + half_width
    p0, p1 = SOURCE_P_CENTER - half_width, SOURCE_P_CENTER + half_width
    require(strip[0] < t0 < t1 < strip[1], "source t box inside selected strip")
    require(strip[2] < p0 < p1 < strip[3], "source p box inside selected strip")
    require(t0 < lower < t1 < upper, "source t box around lower locator endpoint")
    atom = step1.Atom(
        SOURCE_CORE_INDEX,
        source,
        t0,
        t1,
        p0,
        p1,
        Q(0),
        Q(0),
        "round136-verifier-rational-r1056-source-box",
    )
    actual_jet = third_tangency_jet(
        source,
        SECOND_OWNER,
        DESIGNATED_THIRD_OWNER,
        t0,
        t1,
        p0,
        p1,
    )
    require(bool(actual_jet.value > 0), "actual rational source box is HIT-side")
    require(
        bool(actual_jet.value - target_shift < 0),
        "actual rational source box is strictly below c=2^-64",
    )
    require(bool(actual_jet.gradient[0] > 0), "actual source box transverse D_t")
    source_area = (t1 - t0) * (p1 - p0)
    require(source_area > 0, "positive rational source area")
    construction = {
        "construction_version": "round136-r1056-rational-source-box-v1",
        "construction_cosine_target": qstr(CONSTRUCTION_COSINE),
        "construction_shift_equation": (
            "Delta3(t,p_center)=R_W^2*construction_cosine_target^2"
        ),
        "construction_target_radius": qstr(TARGET_RADIUS),
        "construction_target_radius_squared": qstr(TARGET_RADIUS_SQUARED),
        "target_radius_square_identity_checked": True,
        "locator_initial_t_interval": [
            qstr(LOCATOR_INITIAL_T_INTERVAL[0]),
            qstr(LOCATOR_INITIAL_T_INTERVAL[1]),
        ],
        "locator_initial_p": qstr(SOURCE_P_CENTER),
        "locator_bisection_depth": LOCATOR_BISECTIONS,
        "locator_bisection_rule": (
            "opposite strict endpoint signs; negative midpoint replaces lower, "
            "positive midpoint replaces upper"
        ),
        "locator_final_bracket": [qstr(lower), qstr(upper)],
        "locator_selected_endpoint": "lower_strict_negative",
        "exact_rational_t_seed": qstr(t_seed),
        "source_box_half_width": qstr(half_width),
        "actual_rational_source_box": {
            "source_core_index": SOURCE_CORE_INDEX,
            "source_chart": source.chart_id,
            "t": [qstr(t0), qstr(t1)],
            "p": [qstr(p0), qstr(p1)],
            "s": ["0", "0"],
            "exact_area": qstr(source_area),
            "positive_area": True,
        },
        "actual_box_D3_positive": True,
        "actual_box_D3_minus_R_squared_c_squared_negative": True,
        "actual_box_D_t_positive": True,
        "construction_target_is_not_used_after_source_box_is_frozen": True,
    }
    return atom, construction


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
    ledger: MarginLedger,
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
        if bool(discriminant < 0):
            histogram["no_real_intersection"] += 1
            decision_depths.append(
                ledger.observe(
                    "candidate_miss_discriminant",
                    -discriminant,
                    {
                        "collision_index": collision_index,
                        "candidate_id": candidate_id,
                    },
                )
            )
            continue
        require(bool(discriminant > 0), "candidate discriminant strict")
        decision_depths.append(
            ledger.observe(
                "candidate_positive_discriminant",
                discriminant,
                {
                    "collision_index": collision_index,
                    "candidate_id": candidate_id,
                },
            )
        )
        radical = discriminant.sqrt()
        near, far = ell - radical, ell + radical
        if bool(far < 0):
            histogram["intersection_strictly_behind"] += 1
            decision_depths.append(
                ledger.observe("candidate_behind_far_root", -far)
            )
            continue
        require(bool(near > 0), "candidate future root strict")
        histogram["strict_future_near_root"] += 1
        decision_depths.append(
            ledger.observe("candidate_future_root_positive", near)
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
        ledger.observe("winner_pairwise_root_gap", row["near"] - selected["near"])
        for candidate_id, row in future
        if candidate_id != selected_id
    ]
    root = selected["near"]
    tau_margin = aq(time3.time2_cert.first_hit.TAU_MAX) - root
    require(bool(tau_margin > 0), "winner flight cap")
    root_depth = ledger.observe("selected_root_positive", root)
    selected_discriminant_depth = ledger.observe(
        "selected_discriminant_positive",
        selected["discriminant"],
        {
            "collision_index": collision_index,
            "candidate_id": selected_id,
        },
    )
    tau_depth = ledger.observe("selected_root_below_tau_max", tau_margin)
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
        "minimum_winner_gap_dyadic_depth": (
            max(gap_depths) if gap_depths else None
        ),
        "selected_root_positive_margin_dyadic_depth": root_depth,
        "selected_discriminant_positive_margin_dyadic_depth":
            selected_discriminant_depth,
        "selected_root_below_tau_margin_dyadic_depth": tau_depth,
    }
    return owner, audit


def chart_margin(state: dict[str, Any], ledger: MarginLedger) -> int:
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
    ledger: MarginLedger,
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


def homogeneity_label(
    collision_index: int,
    cosine: arb,
    ledger: MarginLedger,
) -> tuple[str, dict[str, Any]]:
    central_boundary = round117.boundary_ball(round117.N0)
    if bool(cosine > central_boundary):
        depth = ledger.observe(
            "central_homogeneity_margin", cosine - central_boundary
        )
        return "H0_CENTRAL", {
            "homogeneity_label": "H0_CENTRAL",
            "lower_boundary": "sin(128^-2)",
            "lower_boundary_margin_dyadic_depth": depth,
            "upper_boundary": None,
            "upper_boundary_margin_dyadic_depth": None,
        }
    require(collision_index == 3, "unexpected noncentral homogeneity collision")
    index = EXPECTED_TAIL_LABEL_INDEX
    lower_boundary = round117.boundary_ball(index + 1)
    upper_boundary = round117.boundary_ball(index)
    lower_margin = cosine - lower_boundary
    upper_margin = upper_boundary - cosine
    require(
        bool(lower_margin > 0) and bool(upper_margin > 0),
        "exact tail homogeneity strip isolation",
    )
    lower_depth = ledger.observe("tail_homogeneity_lower_margin", lower_margin)
    upper_depth = ledger.observe("tail_homogeneity_upper_margin", upper_margin)
    return f"H{index}", {
        "homogeneity_label": f"H{index}",
        "lower_boundary": f"sin({index + 1}^-2)",
        "lower_boundary_margin_dyadic_depth": lower_depth,
        "upper_boundary": f"sin({index}^-2)",
        "upper_boundary_margin_dyadic_depth": upper_depth,
    }


def capped_reciprocal_cosine_rank(
    cosine: arb,
    ledger: MarginLedger,
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


def replay_return(
    atom: step1.Atom,
) -> tuple[list[dict[str, Any]], dict[str, Any], MarginLedger]:
    cores = tuple(core_cert.physical_cores())
    pair_index, pattern_index, registry_sha = component_cert.key_index_tables()
    require(
        registry_sha == OFFICIAL_REGISTRY_STREAM_SHA256,
        "official registry replay digest",
    )
    state = initial_state(atom)
    current_target = SOURCE_ABSOLUTE_OWNER
    source_cosine = (1 - state["p"] * state["p"]).sqrt()
    previous_cosine = source_cosine
    ledger = MarginLedger()
    rows: list[dict[str, Any]] = []
    first_return_depth: int | None = None
    destination_core_id: str | None = None
    for collision_index in range(1, RETURN_DEPTH + 1):
        owner, candidate_audit = complete_owner(
            state, current_target, ledger, collision_index
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
            f"official word reconstruction at collision {collision_index}:{word_error}",
        )
        classification, destination, witnesses = time3.core_classification(owner, cores)
        require(
            classification in {"SURVIVE_THROUGH_3_INNER", "RETURN_AT_3_INNER"},
            "strict C24 classification",
        )
        if collision_index < RETURN_DEPTH:
            require(
                classification == "SURVIVE_THROUGH_3_INNER"
                and destination is None,
                "premature C24 return",
            )
        else:
            require(
                classification == "RETURN_AT_3_INNER"
                and destination == EXPECTED_DESTINATION_CORE_ID,
                "collision 1056 strict destination",
            )
            first_return_depth = collision_index
            destination_core_id = destination
        core_depth = core_margin(
            owner, classification, destination, cores, ledger
        )
        _label, label_audit = homogeneity_label(
            collision_index, owner["cosine"], ledger
        )
        source_rank = capped_reciprocal_cosine_rank(
            previous_cosine, ledger, collision_index, "source"
        )
        target_rank = capped_reciprocal_cosine_rank(
            owner["cosine"], ledger, collision_index, "target"
        )
        incidence_rank = max(14, source_rank, target_rank)
        row_base = {
            "collision_index": collision_index,
            "incoming_absolute_owner_id": current_target,
            "incoming_chart": state["chart"],
            "selected_absolute_owner_id": owner["selected_target_id"],
            "complete_candidate_audit": candidate_audit,
            "official_word_key": compact_key(word["key"]),
            "ordered_clean_wall_record": word["ordered_clean_wall_record"],
            "relative_frozen_target_id": word["relative_frozen_target_id"],
            "absolute_lattice_translation_removed":
                word["absolute_lattice_translation_removed"],
            "C24_classification": classification,
            "destination_core_id": destination,
            "C24_core_witness_count": len(witnesses),
            "C24_minimum_inside_or_exclusion_margin_dyadic_depth": core_depth,
            **label_audit,
            "source_capped_reciprocal_cosine_rank": source_rank,
            "target_capped_reciprocal_cosine_rank": target_rank,
            "incidence_rank_B": incidence_rank,
            "incidence_rank_rule": (
                "max(14,ceil_log2(1/c_source),ceil_log2(1/c_target)) "
                "with whole-box strict dyadic comparisons"
            ),
        }
        next_state = time3.second_outgoing_state(atom, state, owner)
        require(next_state is not None, "outgoing state reconstruction")
        row_base["outgoing_chart"] = next_state["chart"]
        row_base["outgoing_chart_margin_dyadic_depth"] = chart_margin(
            next_state, ledger
        )
        rows.append(with_hash(row_base))
        state = next_state
        current_target = owner["selected_target_id"]
        previous_cosine = owner["cosine"]
    require(
        first_return_depth == RETURN_DEPTH
        and destination_core_id == EXPECTED_DESTINATION_CORE_ID,
        "first return summary",
    )
    require(
        [row["official_word_key"]["ordinal_zero_based"] for row in rows[:3]]
        == [266945, 285659, 42355],
        "Round116 HIT three-key prefix",
    )
    require(
        rows[2]["homogeneity_label"] == f"H{EXPECTED_TAIL_LABEL_INDEX}"
        and rows[2]["target_capped_reciprocal_cosine_rank"] == 65,
        "third collision exact rank refinement",
    )
    path_key_ids = [
        row["official_word_key"]["official_word_key_id"] for row in rows
    ]
    unique_path_key_ids = sorted(set(path_key_ids))
    require(
        len(path_key_ids) == RETURN_DEPTH
        and len(unique_path_key_ids) == 125,
        "official word occurrence and unique-key census",
    )
    source_core_id = step1.core_id(atom.source_core)
    require(source_core_id == EXPECTED_SOURCE_CORE_ID, "source core identity")
    path_tuple_payload = [source_core_id, RETURN_DEPTH, path_key_ids]
    local_component_payload = [
        "round136-local-return-cylinder-v1",
        source_core_id,
        RETURN_DEPTH,
        digest(path_key_ids),
        [
            qstr(atom.t0),
            qstr(atom.t1),
            qstr(atom.p0),
            qstr(atom.p1),
            qstr(atom.s0),
            qstr(atom.s1),
        ],
    ]
    summary = {
        "source_core_id": source_core_id,
        "return_depth": RETURN_DEPTH,
        "first_return_depth": first_return_depth,
        "destination_core_id": destination_core_id,
        "Round27_compatible_complete_candidate_path_tuple_sha256":
            digest(path_tuple_payload),
        "official_word_key_occurrence_count": len(path_key_ids),
        "official_word_key_sequence_sha256": digest(path_key_ids),
        "unique_official_word_key_id_count": len(unique_path_key_ids),
        "sorted_unique_official_word_key_ids_sha256":
            digest(unique_path_key_ids),
        "local_return_cylinder_id":
            "round136-local-return-cylinder:" + digest(local_component_payload),
        "preterminal_strict_nonreturn_collision_count": RETURN_DEPTH - 1,
        "terminal_strict_return_collision_count": 1,
        "all_collision_candidate_searches_complete": True,
        "all_official_word_keys_rebuilt": True,
        "all_homogeneity_labels_whole_box_isolated": True,
        "all_incidence_ranks_whole_box_constant": True,
        "source_box_positive_area": True,
    }
    return rows, summary, ledger


def typed_occurrence_singleton(
    closed: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    rows = closed[ROUND132.name]["occurrence_face_record_rows"]
    label = ["G", "W[0,-1]", 1, "W[0,-2]", -1]
    matches = [row for row in rows if row["global_physical_label"] == label]
    require(len(rows) == 64 and len(matches) == 1, "Round132 typed singleton")
    row = matches[0]
    require(
        row["occurrence_record_id"]
        == "round132-occurrence-record:4fea21fa8bb8290b15f0f68650a02b373fb072bb520729107c344b4592ef01ab"
        and row["immutable_global_occurrence_face_seed_id"]
        == "physical-moving-occurrence-face-seed:"
        "bfe49bc96e1d102432553fec6f61761ed65c61726056b914c1a37c6777aa5ca0",
        "Round132 singleton IDs",
    )
    values = row["canonical_Round67_source_field_values"]
    require(
        values["return_component"] is None
        and values["owner_key"] is None
        and values["rank_zero_component"] is None
        and row["Round67_owner_map_q_j_materialized"] is False,
        "Round132 owner fields remain null",
    )
    return {
        "complete_Round132_global_label_row_count": len(rows),
        "filter_global_physical_label": label,
        "matching_row_count": len(matches),
        "occurrence_record_id": row["occurrence_record_id"],
        "occurrence_id": row["occurrence_id"],
        "immutable_global_occurrence_face_seed_id":
            row["immutable_global_occurrence_face_seed_id"],
        "occurrence_word_cell_id":
            values["word_cell"]["occurrence_word_cell_id"],
        "hit_trace_seed_id": row["hit_trace_seed_id"],
        "miss_trace_seed_id": row["miss_trace_seed_id"],
        "common_boundary_recovery_carrier_id":
            row["common_boundary_recovery_carrier_id"],
        "typed_singleton_is_not_a_Round50_complete_primitive_fibre": True,
        "Round67_owner_map_q_j_materialized": False,
    }


STRICT_NONPROMOTION = {
    "Round27_compatible_complete_candidate_path_tuple_materialized": True,
    "canonical_Round27_c24_path_id_materialized": False,
    "canonical_Round27_c24_path_id": None,
    "actual_positive_width_R1056_local_return_cylinder_materialized": True,
    "global_least_dyadic_basis_component_rank_materialized": False,
    "c24_component_id": None,
    "Round35_rn_restriction_id": None,
    "return_component_to_D0_face_crosswalk_materialized": False,
    "Round50_complete_primitive_fibre_materialized": False,
    "Round50_owner_key_count": 0,
    "Round54_t54_token_count": 0,
    "Round67_q_j_output_count": 0,
    "owner_law_positive_mass": "NOT_CERTIFIED",
    "plus_HIT_A_col_clearance": "NOT_CERTIFIED",
    "minus_BYPASS_return_continuation": "UNRESOLVED",
    "gate5_global_maturity": "10/18",
    "global_complete_18_field_block_count": 0,
    "complete_18_field_block_count": 0,
    "Gate5": "NOT_CERTIFIED",
    "CM2": "NO-GO_FOR_CLAIM",
}

STRICT_SCOPE = (
    "one exact positive-area rational source box at s=0 inside corrected "
    "Round102 face/link and Round116 strip 128; actual complete-candidate "
    "first return at depth 1056 with all official keys, homogeneity labels "
    "and dyadic incidence ranks rebuilt"
)

STRICT_NONCLAIMS = [
    "the Round116 three-key HIT prefix is not renamed an R_n return path",
    "the local return cylinder ID is not a c24-component ID",
    "no least global rational-dyadic basis component rank is claimed",
    "no Round35 rn-restriction is minted",
    "the R1056 cylinder is not proved to have the D=0 face in its closure",
    "the Round132 typed occurrence singleton is not renamed a Round50 owner fibre",
    "no owner key, t54 token, Omega_j record or q_j output is materialized",
    "owner-law positive mass and all-time owner sums remain unproved",
    "no Gate5 field, Gate5 block or CM2 claim is promoted",
]


def build_expected(
    precision_bits: int = PRECISION_BITS,
) -> tuple[dict[str, Any], step1.Atom]:
    require(precision_bits >= PRECISION_BITS, "verifier precision below 8192")
    ctx.prec = precision_bits
    closed = validate_dependencies()
    round116.init_worker(precision_bits)
    source, face, selected_link, strip = selected_corrected_objects(closed)
    atom, construction = construction_and_source_box(source, strip)
    collision_rows, return_summary, ledger = replay_return(atom)
    occurrence = typed_occurrence_singleton(closed)

    r27 = strict_json(ROUND27)["result"]
    r35 = strict_json(ROUND35)["result"]
    require(
        r27["canonical_regular_connected_component_schema"][
            "component_coordinates_and_nonempty_ranks_enumerated"
        ]
        is False,
        "Round27 component enumeration frontier",
    )
    require(
        r35["arbitrary_Rn_parent_W_Borel_registry"][
            "nonempty_component_coordinates_enumerated"
        ]
        is False,
        "Round35 component enumeration frontier",
    )
    r133 = closed[ROUND133.name]
    require(
        r133["count_ledger"]["owner_key_count"] == 0
        and r133["count_ledger"]["q_j_recordwise_output_count"] == 0,
        "Round133 owner frontier",
    )

    result = {
        "precision_bits": precision_bits,
        "status": "CERTIFIED_ACTUAL_POSITIVE_WIDTH_R1056_LOCAL_RETURN_CYLINDER_FRONTIER",
        "provenance": {
            "producer_sha256": PRODUCER_SHA256,
            "dependency_sha256": dict(sorted(PINS.items())),
            "append_only": True,
            "old_artifacts_modified": False,
            "historical_Round87_physicality_used": False,
            "corrected_port_membership_source": "Round99 corrected IDs only",
        },
        "corrected_rank3_source_contract": {
            "face_id": SELECTED_FACE_ID,
            "face_branch": [
                face["source_core_index"],
                face["second_selected_target_id"],
                face["third_candidate_id"],
                face["signed_transverse_tangency_factor_sign"],
            ],
            "link_rank": SELECTED_LINK_RANK,
            "link_type": selected_link["link_type"],
            "left_registered_port_id": selected_link["left_registered_port_id"],
            "right_registered_port_id": selected_link["right_registered_port_id"],
            "strip_index_zero_based": SELECTED_STRIP_INDEX,
            "strip_count": 256,
            "Round116_HIT_prefix_only_not_return_path": True,
            "Round116_HIT_prefix_ordinals": [266945, 285659, 42355],
        },
        "typed_occurrence_singleton": occurrence,
        "rational_source_box_construction": construction,
        "actual_R1056_return_summary": return_summary,
        "collision_rows": collision_rows,
        "collision_rows_sha256": digest(collision_rows),
        "strict_margin_ledger": ledger.public(),
        "strict_nonpromotion": dict(STRICT_NONPROMOTION),
        "count_ledger": {
            "typed_occurrence_singleton_count": 1,
            "positive_width_local_return_cylinder_count": 1,
            "collision_row_count": len(collision_rows),
            "official_word_key_occurrence_count":
                return_summary["official_word_key_occurrence_count"],
            "unique_official_word_key_id_count":
                return_summary["unique_official_word_key_id_count"],
            "preterminal_strict_nonreturn_collision_count": RETURN_DEPTH - 1,
            "terminal_strict_return_collision_count": 1,
            "tail_homogeneity_collision_count": sum(
                row["homogeneity_label"] != "H0_CENTRAL"
                for row in collision_rows
            ),
            "global_c24_component_id_count": 0,
            "Round35_rn_restriction_id_count": 0,
            "Round50_owner_key_count": 0,
            "Round67_q_j_output_count": 0,
            "global_complete_18_field_block_count": 0,
        },
        "strict_scope": STRICT_SCOPE,
        "strict_nonclaims": list(STRICT_NONCLAIMS),
    }
    require(len(collision_rows) == RETURN_DEPTH, "collision row census")
    require(
        result["count_ledger"]["tail_homogeneity_collision_count"] == 1,
        "tail homogeneity census",
    )
    result = json.loads(json.dumps(result, sort_keys=True))
    return result, atom


def collision_semantic_projection(rows: list[dict[str, Any]]) -> list[Any]:
    """Precision-stable discrete geometry, excluding enclosure-depth metadata."""

    return [
        [
            row["collision_index"],
            row["incoming_absolute_owner_id"],
            row["incoming_chart"],
            row["selected_absolute_owner_id"],
            row["complete_candidate_audit"]["retained_candidate_count"],
            row["complete_candidate_audit"]["candidate_classification_histogram"],
            row["official_word_key"],
            row["ordered_clean_wall_record"],
            row["relative_frozen_target_id"],
            row["absolute_lattice_translation_removed"],
            row["C24_classification"],
            row["destination_core_id"],
            row["C24_core_witness_count"],
            row["homogeneity_label"],
            row["source_capped_reciprocal_cosine_rank"],
            row["target_capped_reciprocal_cosine_rank"],
            row["incidence_rank_B"],
            row["outgoing_chart"],
        ]
        for row in rows
    ]


def secondary_precision_replay(
    atom: step1.Atom,
    primary: dict[str, Any],
    precision_bits: int,
) -> dict[str, Any]:
    require(precision_bits > PRECISION_BITS, "secondary precision must be higher")
    ctx.prec = precision_bits
    round116.init_worker(precision_bits)
    rows, summary, ledger = replay_return(atom)
    primary_projection = collision_semantic_projection(primary["collision_rows"])
    secondary_projection = collision_semantic_projection(rows)
    require(
        secondary_projection == primary_projection,
        "dual-precision collision semantic projection",
    )
    semantic_summary_keys = (
        "source_core_id",
        "return_depth",
        "first_return_depth",
        "destination_core_id",
        "Round27_compatible_complete_candidate_path_tuple_sha256",
        "official_word_key_occurrence_count",
        "official_word_key_sequence_sha256",
        "unique_official_word_key_id_count",
        "sorted_unique_official_word_key_ids_sha256",
        "local_return_cylinder_id",
        "preterminal_strict_nonreturn_collision_count",
        "terminal_strict_return_collision_count",
        "all_collision_candidate_searches_complete",
        "all_official_word_keys_rebuilt",
        "all_homogeneity_labels_whole_box_isolated",
        "all_incidence_ranks_whole_box_constant",
        "source_box_positive_area",
    )
    require(
        {key: summary[key] for key in semantic_summary_keys}
        == {
            key: primary["actual_R1056_return_summary"][key]
            for key in semantic_summary_keys
        },
        "dual-precision summary semantics",
    )
    primary_ledger = primary["strict_margin_ledger"]
    secondary_ledger = ledger.public()
    require(set(primary_ledger) == set(secondary_ledger), "dual-precision ledger names")
    for name in primary_ledger:
        require(
            primary_ledger[name]["dyadic_depth"]
            == secondary_ledger[name]["dyadic_depth"]
            and primary_ledger[name]["observation_count"]
            == secondary_ledger[name]["observation_count"]
            and primary_ledger[name]["minimum_observed_witness"]
            == secondary_ledger[name]["minimum_observed_witness"],
            f"dual-precision margin semantics:{name}",
        )
    return {
        "primary_precision_bits": PRECISION_BITS,
        "secondary_precision_bits": precision_bits,
        "collision_semantic_projection_sha256": digest(primary_projection),
        "collision_semantic_projection_match": True,
        "summary_semantics_match": True,
        "margin_name_depth_count_witness_projection_match": True,
        "exact_Arb_enclosure_endpoints_intentionally_not_compared": True,
    }


def regular_single_link(path: Path, label: str) -> None:
    require(path.is_file(), f"missing regular file:{label}")
    require(not path.is_symlink(), f"symlink file:{label}")
    metadata = path.lstat()
    require(stat.S_ISREG(metadata.st_mode), f"non-regular file:{label}")
    require(metadata.st_nlink == 1, f"hardlinked file:{label}")


def safe_input_path(path: Path) -> Path:
    expanded = path.expanduser()
    regular_single_link(expanded, "certificate")
    require(
        expanded.stat().st_size <= MAX_CERTIFICATE_BYTES,
        "certificate exceeds size limit",
    )
    resolved = expanded.resolve()
    require(sha256(resolved) == CERTIFICATE_SHA256, "certificate byte pin")
    return resolved


def validate_collision_closures(result: dict[str, Any]) -> None:
    rows = result["collision_rows"]
    require(type(rows) is list and len(rows) == RETURN_DEPTH, "1056 collision rows")
    require(
        result["collision_rows_sha256"] == digest(rows),
        "collision row group closure",
    )
    seen_indices: list[int] = []
    seen_row_hashes: list[str] = []
    for row in rows:
        require(type(row) is dict, "collision row object")
        body = dict(row)
        row_hash = body.pop("row_sha256", None)
        require(type(row_hash) is str and row_hash == digest(body), "collision row closure")
        seen_indices.append(body["collision_index"])
        seen_row_hashes.append(row_hash)
        key = body["official_word_key"]
        registry_body = key["registry_row"]
        require(
            key["registry_row_sha256"] == digest(registry_body),
            "registry row closure",
        )
        require(
            key["official_word_key_id"]
            == f"gate5-word:{key['ordinal_zero_based']:06d}:"
            f"{key['registry_row_sha256']}",
            "official word ID closure",
        )
    require(seen_indices == list(range(1, RETURN_DEPTH + 1)), "collision index sequence")
    require(len(seen_row_hashes) == len(set(seen_row_hashes)), "unique row closures")


def evaluate_document(document: dict[str, Any], expected: dict[str, Any]) -> None:
    require(
        set(document) == {"schema", "result", "result_sha256"},
        "closed certificate envelope",
    )
    require(document["schema"] == CERTIFICATE_SCHEMA, "certificate schema")
    result = document["result"]
    require(type(result) is dict, "certificate result object")
    require(document["result_sha256"] == digest(result), "certificate result digest")
    validate_collision_closures(result)
    require(result == expected, "independent complete result reconstruction equality")
    require(
        document["result_sha256"] == CERTIFICATE_RESULT_SHA256,
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


def reclose_collision(document: dict[str, Any], index: int) -> None:
    row = document["result"]["collision_rows"][index]
    body = {key: value for key, value in row.items() if key != "row_sha256"}
    row.clear()
    row.update(body)
    row["row_sha256"] = digest(body)
    document["result"]["collision_rows_sha256"] = digest(
        document["result"]["collision_rows"]
    )
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
    simple("precision weakened", ("result", "precision_bits"), 4096)
    simple(
        "producer pin altered",
        ("result", "provenance", "producer_sha256"),
        "0" * 64,
    )
    simple(
        "upstream pin altered",
        (
            "result",
            "provenance",
            "dependency_sha256",
            ROUND132.name,
        ),
        "0" * 64,
    )
    simple(
        "historical Round87 enabled",
        ("result", "provenance", "historical_Round87_physicality_used"),
        True,
    )
    simple(
        "face ID altered",
        ("result", "corrected_rank3_source_contract", "face_id"),
        "physical-s0-rank3-corrected-face:bad",
    )
    simple(
        "face branch altered",
        ("result", "corrected_rank3_source_contract", "face_branch"),
        [14, "G[0,1]", "W[0,0]", -1],
    )
    simple(
        "strip index altered",
        ("result", "corrected_rank3_source_contract", "strip_index_zero_based"),
        127,
    )
    simple(
        "HIT prefix promoted to return",
        (
            "result",
            "corrected_rank3_source_contract",
            "Round116_HIT_prefix_only_not_return_path",
        ),
        False,
    )
    simple(
        "HIT prefix ordinal altered",
        (
            "result",
            "corrected_rank3_source_contract",
            "Round116_HIT_prefix_ordinals",
        ),
        [266945, 285659, 42356],
    )
    simple(
        "typed singleton count altered",
        (
            "result",
            "typed_occurrence_singleton",
            "matching_row_count",
        ),
        2,
    )
    simple(
        "typed singleton promoted",
        (
            "result",
            "typed_occurrence_singleton",
            "typed_singleton_is_not_a_Round50_complete_primitive_fibre",
        ),
        False,
    )
    simple(
        "owner q_j invented",
        (
            "result",
            "typed_occurrence_singleton",
            "Round67_owner_map_q_j_materialized",
        ),
        True,
    )
    simple(
        "construction target altered",
        (
            "result",
            "rational_source_box_construction",
            "construction_cosine_target",
        ),
        "1/9223372036854775808",
    )
    simple(
        "locator depth altered",
        (
            "result",
            "rational_source_box_construction",
            "locator_bisection_depth",
        ),
        1499,
    )
    simple(
        "source half width altered",
        (
            "result",
            "rational_source_box_construction",
            "source_box_half_width",
        ),
        "1/2",
    )
    simple(
        "positive area erased",
        (
            "result",
            "rational_source_box_construction",
            "actual_rational_source_box",
            "positive_area",
        ),
        False,
    )
    simple(
        "HIT-side sign erased",
        (
            "result",
            "rational_source_box_construction",
            "actual_box_D3_positive",
        ),
        False,
    )
    simple(
        "construction target reused",
        (
            "result",
            "rational_source_box_construction",
            "construction_target_is_not_used_after_source_box_is_frozen",
        ),
        False,
    )
    simple(
        "return depth altered",
        ("result", "actual_R1056_return_summary", "return_depth"),
        1055,
    )
    simple(
        "first return altered",
        ("result", "actual_R1056_return_summary", "first_return_depth"),
        1055,
    )
    simple(
        "destination altered",
        ("result", "actual_R1056_return_summary", "destination_core_id"),
        EXPECTED_SOURCE_CORE_ID,
    )
    simple(
        "word occurrence count altered",
        (
            "result",
            "actual_R1056_return_summary",
            "official_word_key_occurrence_count",
        ),
        1055,
    )
    simple(
        "unique word count altered",
        (
            "result",
            "actual_R1056_return_summary",
            "unique_official_word_key_id_count",
        ),
        124,
    )
    simple(
        "candidate completeness erased",
        (
            "result",
            "actual_R1056_return_summary",
            "all_collision_candidate_searches_complete",
        ),
        False,
    )
    simple(
        "word rebuild erased",
        (
            "result",
            "actual_R1056_return_summary",
            "all_official_word_keys_rebuilt",
        ),
        False,
    )
    simple(
        "homogeneity isolation erased",
        (
            "result",
            "actual_R1056_return_summary",
            "all_homogeneity_labels_whole_box_isolated",
        ),
        False,
    )
    simple(
        "incidence constancy erased",
        (
            "result",
            "actual_R1056_return_summary",
            "all_incidence_ranks_whole_box_constant",
        ),
        False,
    )
    simple(
        "canonical component invented",
        ("result", "strict_nonpromotion", "c24_component_id"),
        "c24-component:invented",
    )
    simple(
        "Round35 restriction invented",
        ("result", "strict_nonpromotion", "Round35_rn_restriction_id"),
        "rn-restriction:invented",
    )
    simple(
        "Round50 fibre invented",
        (
            "result",
            "strict_nonpromotion",
            "Round50_complete_primitive_fibre_materialized",
        ),
        True,
    )
    simple(
        "owner count invented",
        ("result", "strict_nonpromotion", "Round50_owner_key_count"),
        1,
    )
    simple(
        "q_j invented",
        ("result", "strict_nonpromotion", "Round67_q_j_output_count"),
        1,
    )
    simple(
        "owner positive mass promoted",
        ("result", "strict_nonpromotion", "owner_law_positive_mass"),
        "CERTIFIED",
    )
    simple(
        "global maturity promoted",
        ("result", "strict_nonpromotion", "gate5_global_maturity"),
        "18/18",
    )
    simple(
        "global block invented",
        (
            "result",
            "strict_nonpromotion",
            "global_complete_18_field_block_count",
        ),
        1,
    )
    simple(
        "Gate5 promoted",
        ("result", "strict_nonpromotion", "Gate5"),
        "CERTIFIED",
    )
    simple(
        "CM2 promoted",
        ("result", "strict_nonpromotion", "CM2"),
        "GO_FOR_CLAIM",
    )
    simple(
        "collision census altered",
        ("result", "count_ledger", "collision_row_count"),
        1055,
    )
    simple(
        "preterminal census altered",
        (
            "result",
            "count_ledger",
            "preterminal_strict_nonreturn_collision_count",
        ),
        1054,
    )
    simple(
        "tail census altered",
        ("result", "count_ledger", "tail_homogeneity_collision_count"),
        0,
    )
    simple(
        "global component census invented",
        ("result", "count_ledger", "global_c24_component_id_count"),
        1,
    )
    simple(
        "ledger depth weakened",
        (
            "result",
            "strict_margin_ledger",
            "selected_discriminant_positive",
            "dyadic_depth",
        ),
        133,
    )
    simple(
        "ledger observation count altered",
        (
            "result",
            "strict_margin_ledger",
            "candidate_miss_discriminant",
            "observation_count",
        ),
        0,
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

    sample_indices = [
        0,
        1,
        2,
        3,
        7,
        15,
        31,
        63,
        127,
        255,
        383,
        511,
        639,
        767,
        895,
        1023,
        1054,
        1055,
    ]
    for index in sample_indices:
        def mutate_owner(
            document: dict[str, Any],
            selected: int = index,
        ) -> None:
            document["result"]["collision_rows"][selected][
                "selected_absolute_owner_id"
            ] += "-tampered"
            reclose_collision(document, selected)

        mutations.append((f"collision owner altered:{index + 1}", mutate_owner))

    for index in (0, 2, 127, 511, 1055):
        def mutate_word(
            document: dict[str, Any],
            selected: int = index,
        ) -> None:
            row = document["result"]["collision_rows"][selected]
            row["official_word_key"]["ordinal_zero_based"] += 1
            reclose_collision(document, selected)

        mutations.append((f"official ordinal altered:{index + 1}", mutate_word))

    for index in (2, 1055):
        def mutate_classification(
            document: dict[str, Any],
            selected: int = index,
        ) -> None:
            row = document["result"]["collision_rows"][selected]
            row["C24_classification"] = (
                "SURVIVE_THROUGH_3_INNER"
                if selected == RETURN_DEPTH - 1
                else "RETURN_AT_3_INNER"
            )
            reclose_collision(document, selected)

        mutations.append((f"C24 classification altered:{index + 1}", mutate_classification))

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
            b'"status": "CERTIFIED_ACTUAL_POSITIVE_WIDTH_R1056_LOCAL_RETURN_CYLINDER_FRONTIER"',
            b'"status": "bad", "status": "CERTIFIED_ACTUAL_POSITIVE_WIDTH_R1056_LOCAL_RETURN_CYLINDER_FRONTIER"',
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
        raw.replace(b'"collision_row_count": 1056', b'"collision_row_count": 1056.0', 1),
    )
    add(
        "NaN constant",
        raw.replace(b'"collision_row_count": 1056', b'"collision_row_count": NaN', 1),
    )
    add(
        "positive Infinity",
        raw.replace(
            b'"collision_row_count": 1056',
            b'"collision_row_count": Infinity',
            1,
        ),
    )
    add(
        "negative Infinity",
        raw.replace(
            b'"collision_row_count": 1056',
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
            b'"collision_row_count": 1056',
            b'"collision_row_count": ' + b"9" * (MAX_INTEGER_DIGITS + 1),
            1,
        ),
    )
    add(
        "negative zero",
        raw.replace(b'"collision_row_count": 1056', b'"collision_row_count": -0', 1),
    )
    add(
        "leading-zero integer",
        raw.replace(b'"collision_row_count": 1056', b'"collision_row_count": 01056', 1),
    )
    add(
        "unpaired surrogate",
        raw.replace(
            b'"CERTIFIED_ACTUAL_POSITIVE_WIDTH_R1056_LOCAL_RETURN_CYLINDER_FRONTIER"',
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


def safe_output_path(path: Path, certificate_path: Path) -> Path:
    expanded = path.expanduser()
    protected = {
        VERIFIER.resolve(),
        PRODUCER.resolve(),
        CERTIFICATE.resolve(),
        certificate_path.resolve(),
        *((HERE / name).resolve() for name in PINS),
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

    with tempfile.TemporaryDirectory(prefix="cm2-r136-path-tests-") as name:
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
    precision_contract: dict[str, Any],
    semantic_labels: list[str],
    strict_labels: list[str],
    path_labels: list[str],
) -> dict[str, Any]:
    summary = expected["actual_R1056_return_summary"]
    rows = expected["collision_rows"]
    return {
        "status": "PASS",
        "verifier_sha256": sha256(VERIFIER),
        "producer_sha256": PRODUCER_SHA256,
        "certificate_sha256": CERTIFICATE_SHA256,
        "certificate_schema": CERTIFICATE_SCHEMA,
        "certificate_result_sha256": CERTIFICATE_RESULT_SHA256,
        "independence_contract": {
            "Round136_producer_imported": False,
            "Round136_producer_executed": False,
            "rational_source_box_independently_reconstructed": True,
            "all_1056_collision_rows_independently_reconstructed": True,
            "all_row_and_group_hashes_independently_reclosed": True,
            "complete_candidate_search_replayed_at_every_collision": True,
            "official_registry_words_translation_normalized_and_rebuilt": True,
            "homogeneity_and_incidence_ranks_independently_rebuilt": True,
            "strict_margin_ledger_independently_rebuilt": True,
            "full_certificate_result_independently_reconstructed": True,
        },
        "replay_audit": {
            "source_core_id": summary["source_core_id"],
            "source_box_positive_area": summary["source_box_positive_area"],
            "return_depth": summary["return_depth"],
            "preterminal_strict_nonreturn_collision_count":
                summary["preterminal_strict_nonreturn_collision_count"],
            "terminal_strict_return_collision_count":
                summary["terminal_strict_return_collision_count"],
            "destination_core_id": summary["destination_core_id"],
            "collision_row_count": len(rows),
            "collision_rows_sha256": expected["collision_rows_sha256"],
            "official_word_key_occurrence_count":
                summary["official_word_key_occurrence_count"],
            "unique_official_word_key_id_count":
                summary["unique_official_word_key_id_count"],
            "official_word_key_sequence_sha256":
                summary["official_word_key_sequence_sha256"],
            "Round116_prefix_ordinals": [
                row["official_word_key"]["ordinal_zero_based"]
                for row in rows[:3]
            ],
            "tail_homogeneity_collision_index": 3,
            "tail_homogeneity_label": rows[2]["homogeneity_label"],
            "tail_incidence_rank_B": rows[2]["incidence_rank_B"],
            "terminal_collision_index": rows[-1]["collision_index"],
            "terminal_classification": rows[-1]["C24_classification"],
            "strict_margin_kind_count": len(expected["strict_margin_ledger"]),
            "local_return_cylinder_id": summary["local_return_cylinder_id"],
        },
        "dual_precision_consistency": precision_contract,
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
    parser.add_argument(
        "--secondary-precision-bits",
        type=int,
        default=SECONDARY_PRECISION_BITS,
    )
    args = parser.parse_args()
    try:
        regular_single_link(PRODUCER, PRODUCER.name)
        require(sha256(PRODUCER) == PRODUCER_SHA256, "producer byte pin")
        regular_single_link(VERIFIER, VERIFIER.name)
        certificate_path = safe_input_path(args.certificate)
        output = safe_output_path(args.output, certificate_path)
        certificate = strict_json(certificate_path)
        expected, atom = build_expected(PRECISION_BITS)
        require(
            digest(expected) == CERTIFICATE_RESULT_SHA256,
            "independent result reconstruction pin",
        )
        evaluate_document(certificate, expected)
        precision_contract = secondary_precision_replay(
            atom,
            expected,
            args.secondary_precision_bits,
        )
        semantic_labels = semantic_mutations(certificate, expected)
        strict_labels = strict_json_attacks(certificate, expected)
        path_labels = path_safety_self_tests(certificate_path)
        result = build_verification(
            expected,
            precision_contract,
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
