#!/usr/bin/env python3
"""Independent no-producer verifier for C75 exact first-tangency strata.

The C75 producer source is never opened, read, decoded, imported, compiled, or
executed.  Its frozen hash is treated only as a declaration binding.  Numeric
claims are rebuilt at 384 bits with the separately implemented two-variable
Jet kernel from the accepted C73 independent verifier.
"""

from __future__ import annotations

import argparse
import copy
from collections import Counter
from fractions import Fraction as Q
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any, Iterable, Iterator
import zlib

from flint import arb, ctx


sys.dont_write_bytecode = True
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

SELF = Path(__file__).absolute()
ROOT = SELF.parent.parent
OUT = ROOT / "deliverables"
sys.path.insert(0, str(OUT))

import cm2_round306c73_recentered_collision1_h1_strict_exclusion_oracle_independent_verifier_v2 as iv  # noqa: E402


SCHEMA = "cm2.round306c75.first-tangency-exact-strata-oracle.independent-verification.v1"
PREFIX = "cm2_round306c75_first_tangency_exact_strata_oracle_v1"
LEDGER = PREFIX + ".jsonl.gz"
ENDPOINTS = PREFIX + "_endpoint_incidence.jsonl.gz"
RESULT = PREFIX + "_result.json"
REPORT = PREFIX + "_report.md"
MANIFEST = PREFIX + "_manifest.sha256"
OUTER = PREFIX + "_outer_receipt.json"
VERIFICATION = PREFIX + "_independent_verification_v1.json"
MEMBERS = [LEDGER, ENDPOINTS, RESULT, REPORT, MANIFEST, OUTER]
PRECISION = 384
SCOPE = 5_884
SELECTOR = "unique monotone inherited-active-set first tangency"
SELECTED_SEQUENCE = "af501ff9b5666cc6f477a0db0a7cd58544a6363c00560774bc831363dbf8bf17"
PRODUCER_SOURCE_SHA = "5c30c655d2a15e8a2b42f9db5b8c41e2bb0774bea8afee9c26ab08ee61d8aad5"
SUPPORT_SOURCE_SHA = "3bcb9f09e428cd8c4b8859f681683c3044e1cd6e61a1ac9fbb2d87c561abdf23"
CANDIDATE_PINS = {
    LEDGER: ("e1e30a36f75c2ec71b0c4ec51da33e3c09fb5570426aa356f0c815406e251229", 8_697_163),
    ENDPOINTS: ("db50b71ff364a1f1e132ca0804bd5eb8b027d0c9138f93ee95cfe55e71afb0f2", 6_068_104),
    RESULT: ("1d9d4b2f8b7a4bfb6133ce7b23c22765ef9097c133cc47dc199dd0479f478366", 6_804),
    REPORT: ("a68727231ca9edd93b4198cef0c4160619c00665672a0542f0004268760c6f8a", 1_142),
    MANIFEST: ("eb1308b4c73bba2e4bc65e435af66e07d5b6d522e9e118bff668eca7fe6ec18d", 539),
    OUTER: ("6b402c7b2755581368f9b9202bcfe06256593b07e2ab46452e18c23b55fec6a5", 2_094),
}
CANDIDATE_RESULT_OBJECT = "695fb1bb410c45fedbe5eef5cfc104a7043d452b75f03b1baa811b6e7426d863"
CANDIDATE_OUTER_OBJECT = "1fdf98715b66716054e7f1cd09d68b6f483de78d8f45ceab55e6fb4ec144b85b"
CANDIDATE_ROW_SEQUENCE = "4bebfca77d7f42eb04696c41f694343b8e3c80b043c8a7ac1456ee2d6c508d6a"

C72_A = ROOT / ".cm2-runtime/c72-build-a.ZWGF2f/cm2_round306c72_structural_child_obligation_atlas_v1.jsonl.gz"
C72_B = ROOT / ".cm2-runtime/c72-build-b.6NX5S7/cm2_round306c72_structural_child_obligation_atlas_v1.jsonl.gz"
C37 = ROOT / ".cm2-runtime/candidates/c37-horizontal-reflection-20260810T154802Z-be0d65d5e1cc3c38/ordinary_cell_reflection_pairs.jsonl.gz"
C32 = ROOT / ".cm2-runtime/candidates/c32-four-chart-atlas-20260810T133217Z-3c4d0dff259783c9/compact_cells.jsonl.gz"
UPSTREAM = {
    "C72_A": (C72_A, "8234a391be6d499830b75ffb76b76a38e7d9751f108f51a0f18bbf8dc4fd6370", 23_266_147),
    "C72_B": (C72_B, "8234a391be6d499830b75ffb76b76a38e7d9751f108f51a0f18bbf8dc4fd6370", 23_266_147),
    "C37": (C37, "902ccd3a8744a3a4cf851b5f96e1bf9a8c351ace24ce36ae9cb40355079d7dc8", 216_067),
    "C32": (C32, "3e330d63cce3a2c9f43551ee882102bd10f706daab2edc00674432561a62f5d8", 11_222_049),
}
PAIR = {
    31: {"origin": "W:E:00.14.01010111", "cell": "c32-compact-cell:041f34144b44a873bb333fc801014d0b238faaf33d616f20e8cea534effb8a09", "c37": "8178ec54920466e8caf33b267a898e72f5c91b16c6f70cdee9734c7cdcc13b11", "c32": "00f0e2db93a2816b5b696cadd7646be1d22e8644f8880621d4d1a9beea528993", "active": ["G[2,1]", "W[1,0]"], "target": "W[1,0]", "other": "G[2,1]"},
    200: {"origin": "W:E:07.01.01101001", "cell": "c32-compact-cell:1d466d3e68922feaa50c3db01ba42cc16e1aa90e4ae2af0f8d7abbfff78b79a8", "c37": "74e97bf9b7346152eac77b3057b0c816eb24cda4c531194ef3f2e0e843d02f03", "c32": "e65303c5fd089c6bbec794f49d1c9fc35e041ad47ea70cce52813521ac221924", "active": ["G[2,0]", "W[1,0]"], "target": "W[1,0]", "other": "G[2,0]"},
    270: {"origin": "W:E:07.01.01101010", "cell": "c32-compact-cell:2c5fb436107089292c28f4ab2167a0b1423c0fb6d64a327c164ff42739ad071d", "c37": "8ec98ae61d743ec5f3f88b061acf19ede2a70a12b490aff88753f8fdfc903830", "c32": "4ae4a43c8e6b7a9769b85ccba42b473e3d86a878e00f78c87560a266c0b4508e", "active": ["G[2,0]", "W[1,0]"], "target": "W[1,0]", "other": "G[2,0]"},
    711: {"origin": "W:E:00.14.01011011", "cell": "c32-compact-cell:8ee1ada7008271e1806d517118a8c0f2b9932a97b190d7d84770c9925afd62d6", "c37": "e66037c00d654cae65bd3a6a6cf56ae8be2a85f29eabc615d7323517d92ea9d4", "c32": "367136ed6dac99757e78a92d5c53b26dbb09a83d8b4c5dcacaa437f129ab9025", "active": ["G[2,1]", "W[1,0]"], "target": "W[1,0]", "other": "G[2,1]"},
    787: {"origin": "W:N:06.00.01101111", "cell": "c32-compact-cell:adfd78145e4fb77661ca53a12f24379f50809e334accbf9d74264ce6dc42edc6", "c37": "00fc155d31bd540b05aed6b808cd5aa020272b5180233188ef9b357501358a5b", "c32": "d4799abbd72bfaf1cdb82fbd73bd1bc2c9eecb544ae4e4d13d37c8a01c409d43", "active": ["G[1,1]", "W[1,0]"], "target": "G[1,1]", "other": "W[1,0]"},
}


class Reject(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
                      allow_nan=False).encode("utf-8")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def obj(value: Any) -> str:
    return sha(canonical(value))


def closed(value: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(value)
    need("object_sha256" not in result, "object closure absent")
    result["object_sha256"] = obj(result)
    return result


def identity(item: os.stat_result) -> tuple[int, ...]:
    return (item.st_dev, item.st_ino, item.st_mode, item.st_nlink, item.st_uid,
            item.st_gid, item.st_size, item.st_mtime_ns, item.st_ctime_ns)


def secure(path: Path, expected_sha: str, expected_size: int) -> bytes:
    before = path.lstat()
    need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and
         before.st_uid == os.getuid() and before.st_size == expected_size and
         not before.st_mode & stat.S_IWOTH, "secure shape:" + str(path))
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) |
                 getattr(os, "O_NOFOLLOW", 0))
    try:
        opened = os.fstat(fd)
        need(identity(opened) == identity(before), "path/fd identity:" + str(path))
        blocks = []
        while True:
            block = os.read(fd, 1 << 20)
            if not block:
                break
            blocks.append(block)
        need(identity(os.fstat(fd)) == identity(opened), "fd drift:" + str(path))
    finally:
        os.close(fd)
    need(identity(path.lstat()) == identity(before), "path drift:" + str(path))
    raw = b"".join(blocks)
    need(len(raw) == expected_size and sha(raw) == expected_sha, "byte pin:" + str(path))
    return raw


def parse_json(raw: bytes, label: str) -> dict[str, Any]:
    need(raw.endswith(b"\n") and b"\x00" not in raw and
         not raw.startswith(b"\xef\xbb\xbf"), label + ":framing")
    value = json.loads(raw.decode("utf-8"))
    need(type(value) is dict and canonical(value) + b"\n" == raw, label + ":canonical")
    return value


def gzip_lines(raw: bytes, label: str) -> Iterator[bytes]:
    stream = zlib.decompressobj(16 + zlib.MAX_WBITS)
    plain = stream.decompress(raw) + stream.flush()
    need(stream.eof and not stream.unused_data and not stream.unconsumed_tail,
         label + ":single gzip member")
    need(plain.endswith(b"\n"), label + ":newline")
    yield from plain.splitlines()


def rows(raw: bytes, label: str) -> tuple[list[dict[str, Any]], str]:
    values, hashes = [], []
    for index, line in enumerate(gzip_lines(raw, label)):
        value = json.loads(line.decode("utf-8"))
        need(type(value) is dict and canonical(value) == line,
             f"{label}:{index}:canonical")
        body = copy.deepcopy(value)
        claim = body.pop("row_sha256", None)
        need(type(claim) is str and claim == obj(body), f"{label}:{index}:closure")
        values.append(value)
        hashes.append(claim)
    return values, sequence(hashes)


def sequence(values: Iterable[str]) -> str:
    digest = hashlib.sha256()
    for value in values:
        digest.update(value.encode("ascii") + b"\n")
    return digest.hexdigest()


def exact_dyadic(value: arb) -> Q:
    mantissa, exponent = value.man_exp()
    return Q(int(mantissa)) * (Q(2) ** int(exponent))


def target_data(identifier: str) -> tuple[Q, Q, Q]:
    values = {
        "W[1,0]": (Q(3, 2), Q(1, 2), Q(4, 25)),
        "G[2,1]": (Q(2), Q(1), Q(9, 25)),
        "G[2,0]": (Q(2), Q(0), Q(9, 25)),
        "G[1,1]": (Q(1), Q(1), Q(9, 25)),
    }
    need(identifier in values, "target")
    return values[identifier]


# Reuse only the independently implemented Jet arithmetic.  Parent-chart
# geometry is reimplemented here because C73's earlier scope used E charts
# only, while C75 also contains one N-chart lineage.
def frame(box: iv.Box, parent: str) -> tuple[iv.Jet, iv.Jet, iv.Jet, iv.Jet]:
    t0, t1, p0, p1 = box
    t = iv.Jet(iv.interval(t0, t1), (arb(1), arb(0)))
    p = iv.Jet(iv.interval(p0, p1), (arb(0), arb(1)))
    rn = (iv.jet(1) - t * t).sqrt()
    rp = (iv.jet(1) - p * p).sqrt()
    source, chart = parent.split(":")[:2]
    need(source == "W" and chart in {"E", "N"}, "C75 parent chart")
    nx, ny = (rn, t) if chart == "E" else (t, rn)
    ux = rp * nx - p * ny
    uy = rp * ny + p * nx
    radius = iv.jet(Q(4, 25))
    return (iv.jet(Q(1, 2)) + radius * nx,
            iv.jet(Q(1, 2)) + radius * ny, ux, uy)


def root_raw(box: iv.Box, parent: str, identifier: str) -> dict[str, iv.Jet]:
    qx, qy, ux, uy = frame(box, parent)
    ax, ay, radius_q = target_data(identifier)
    dx, dy = iv.jet(ax) - qx, iv.jet(ay) - qy
    ell = ux * dx + uy * dy
    eta = -uy * dx + ux * dy
    radius = iv.jet(radius_q)
    delta_value = radius * radius - eta * eta
    return {"ux": ux, "uy": uy, "ell": ell, "eta": eta,
            "radius": radius, "delta": delta_value}


def delta(box: iv.Box, parent: str,
          target: str) -> tuple[dict[str, iv.Jet], arb]:
    raw = root_raw(box, parent, target)
    centered = iv.mean_value(lambda item: root_raw(item, parent, target)["delta"],
                             box, raw["delta"])
    return raw, centered


def impact(box: iv.Box, parent: str) -> tuple[iv.Jet, iv.Jet, iv.Jet, dict[str, iv.Jet]]:
    raw, centered = delta(box, parent, "W[1,0]")
    conditioned = iv.Jet(centered, raw["delta"].d)
    radical = conditioned.sqrt()
    eta, radius = raw["eta"], raw["radius"]
    ux, uy = raw["ux"], raw["uy"]
    nx = (-radical * ux + eta * uy) / radius
    ny = (-radical * uy - eta * ux) / radius
    return nx * nx - ny * ny, nx, ny, raw


def sign(value: arb) -> str:
    if bool(value < 0):
        return "NEGATIVE"
    if bool(value > 0):
        return "POSITIVE"
    return "UNRESOLVED"


def independent_decision(source: dict[str, Any]) -> dict[str, Any]:
    lineage = PAIR[source["pair_index"]]
    box = iv.parse_box(source)
    t0, t1, p0, p1 = box
    target, other = lineage["target"], lineage["other"]
    parent = lineage["origin"]
    raw, centered = delta(box, parent, target)
    need(bool(centered.lower() < 0) and bool(centered.upper() > 0), "Delta crosses")
    need(sign(raw["delta"].d[1]) in {"NEGATIVE", "POSITIVE"}, "strict dp")
    lower = iv.mean_value(lambda item: root_raw(item, parent, target)["delta"],
                          (t0, t1, p0, p0), root_raw((t0, t1, p0, p0), parent, target)["delta"])
    upper = iv.mean_value(lambda item: root_raw(item, parent, target)["delta"],
                          (t0, t1, p1, p1), root_raw((t0, t1, p1, p1), parent, target)["delta"])
    need(sign(lower) in {"NEGATIVE", "POSITIVE"} and
         sign(upper) in {"NEGATIVE", "POSITIVE"} and sign(lower) != sign(upper),
         "opposite p faces")
    corners = []
    for t in (t0, t1):
        for p in (p0, p1):
            value = root_raw((t, t, p, p), parent, target)["delta"].v
            need(sign(value) in {"NEGATIVE", "POSITIVE"}, "strict corner")
            corners.append(sign(value))
    need(Counter(corners) == Counter({"NEGATIVE": 2, "POSITIVE": 2}), "corners")
    midpoint = (p0 + p1) / 2
    mid_box = (t0, t1, midpoint, midpoint)
    mid_value = root_raw(mid_box, parent, target)["delta"].v
    newton_image = iv.rat(midpoint) - mid_value / raw["delta"].d[1]
    need(bool(newton_image > iv.rat(p0)) and bool(newton_image < iv.rat(p1)),
         "strict p Newton self-map")
    radical_upper = centered.upper().sqrt().upper()
    near_lower = raw["ell"].v.lower() - radical_upper
    need(bool(near_lower > 0), "target positive side future")
    other_raw, other_delta = delta(box, parent, other)
    need(bool(other_delta > 0), "other real")
    other_near = other_raw["ell"].v - other_delta.sqrt()
    need(bool(other_near > 0), "other future")
    gap = other_near.lower() - raw["ell"].v.upper()
    need(bool(gap > 0), "target first")
    if target == "W[1,0]":
        radical = iv.interval(Q(0), exact_dyadic(radical_upper))
        ux, uy, eta, radius = raw["ux"].v, raw["uy"].v, raw["eta"].v, raw["radius"].v
        h1 = ((radius * radius - 2 * eta * eta) * (ux * ux - uy * uy)
              - 4 * radical * eta * ux * uy) / (radius * radius)
        need(bool(h1 < 0), "conditional H1 negative")
        negative_reason = "FROZEN_W_OWNER_ABSENT_ON_DELTA_W_NEGATIVE"
        positive_reason = "FIRST_W_ROOT_EXISTS_BUT_H1_NEGATIVE_STRICT_NOT_W"
    else:
        h1, _nx, ny, _owner = impact(box, parent)
        h1_centered = iv.mean_value(lambda item: impact(item, parent)[0], box, h1)
        need(bool(h1.v < 0) and bool(h1_centered < 0) and bool(ny.v > 0),
             "negative side W chart N")
        negative_reason = "G_TANGENCY_TARGET_ABSENT_AND_UNIQUE_W_OWNER_HAS_H1_N_NOT_W"
        positive_reason = "G_NEAR_ROOT_STRICTLY_PRECEDES_REQUIRED_W_OWNER"
    return {"target": target, "other": other, "lower_face_sign": sign(lower),
            "upper_face_sign": sign(upper), "near_lower": near_lower,
            "first_gap": gap, "negative_reason": negative_reason,
            "positive_reason": positive_reason, "newton_image": newton_image}


def validate_candidate(candidate: dict[str, Any], source: dict[str, Any],
                       proof: dict[str, Any]) -> None:
    lineage = PAIR[source["pair_index"]]
    need(candidate["schema"] == "cm2.round306c75.first-tangency-exact-strata-oracle.v1.strata-row" and
         candidate["C72_obligation_row_sha256"] == source["row_sha256"] and
         candidate["C65_aggregate_child_row_sha256"] == source["C65_aggregate_child_row_sha256"] and
         candidate["C61_aggregate_leaf_row_sha256"] == source["C61_aggregate_leaf_row_sha256"] and
         candidate["pair_index"] == source["pair_index"] and
         candidate["source_path"] == source["source_path"] and
         candidate["child_path"] == source["child_path"] and
         candidate["exact_representative_box"] == source["exact_representative_box"] and
         candidate["exact_reflected_box"] == source["exact_reflected_box"], "row lineage")
    need(candidate["representative_origin_key"] == lineage["origin"] and
         candidate["representative_cell_id"] == lineage["cell"] and
         candidate["C37_pair_row_sha256"] == lineage["c37"] and
         candidate["C32_cell_row_sha256"] == lineage["c32"] and
         candidate["active_candidates"] == lineage["active"] and
         candidate["active_candidate_count"] == 2 and
         candidate["tangency_target"] == proof["target"] and
         candidate["other_active_target"] == proof["other"], "row static math")
    graph = candidate["full_child_tangency_graph"]
    need(graph["precision_bits"] == 384 and graph["graph_axis"] == "p" and
         graph["base_axis"] == "t" and graph["strict_dp_bounds"]["contains_zero"] is False and
         graph["lower_p_face"]["sign"] == proof["lower_face_sign"] and
         graph["upper_p_face"]["sign"] == proof["upper_face_sign"] and
         graph["interval_Newton"]["strict_interior_self_map"] is True and
         graph["unique_regular_graph_over_complete_t_base"] is True and
         graph["graph_endpoints_on_both_t_faces"] is True and
         Counter(item["sign"] for item in graph["four_strict_corners"]) ==
         Counter({"NEGATIVE": 2, "POSITIVE": 2}), "graph claim")
    order = candidate["exact_root_order"]
    need(arb(order["positive_side_target_near_lower"]) > 0 and
         arb(order["first_tangency_order_gap_lower"]) > 0 and
         order["target_is_strict_first_on_graph_and_positive_side"] is True,
         "order claim")
    strata = candidate["three_strata"]
    need(strata["negative_open_side"]["exit_class"] == "STRICT_EXCLUSION" and
         strata["negative_open_side"]["reason"] == proof["negative_reason"] and
         strata["zero_graph"]["exit_class"] == "CEMETERY_OR_SOURCE_GRAZING_TERMINAL" and
         strata["zero_graph"]["terminal_kind"] == "CEMETERY_FIRST_TANGENCY" and
         strata["zero_graph"]["strict_exclusion"] is False and
         strata["positive_open_side"]["exit_class"] == "STRICT_EXCLUSION" and
         strata["positive_open_side"]["reason"] == proof["positive_reason"] and
         strata["pairwise_disjoint"] is True and strata["union_is_exact_complete_child"] is True,
         "three strata")
    glue = candidate["face_corner_source_glue_and_incidence"]
    owner = candidate["half_open_ownership_and_Kraft"]
    need(glue == {"four_corners_attach_by_strict_Delta_sign": True,
                  "p_faces_attach_to_corresponding_open_sign_sides": True,
                  "physical_s_slice": "s=0", "source_grazing": False,
                  "source_grazing_terminal_claimed": False,
                  "t_lower_graph_endpoint_incidence": 1,
                  "t_upper_graph_endpoint_incidence": 1} and
         owner["graph_owner"] == "CEMETERY_FIRST_TANGENCY_TERMINAL" and
         owner["graph_is_not_double_owned"] is True and
         owner["additional_dyadic_depth"] == 0 and
         owner["full_dimensional_normalized_Kraft"] == "1" and
         owner["typed_graph_Kraft"] == "0", "glue/owner")
    need(candidate["unresolved_strata"] == 0 and
         candidate["formal_credit"] == candidate["whole_parent_credit"] ==
         candidate["D02_gate_credit"] == candidate["CM2_credit"] == 0,
         "row zero boundary")


def normalized_interval(values: list[str]) -> tuple[str, str]:
    lower, upper = (Q(value) for value in values)
    need(lower < upper, "interval")
    return str(lower), str(upper)


def face_key(source: dict[str, Any], side: str) -> tuple[int, str, tuple[str, str]]:
    box = source["exact_representative_box"]
    return (source["pair_index"],
            str(Q(box["t"][0 if side == "LOWER_T" else 1])),
            normalized_interval(box["p"]))


def reflected_face(source: dict[str, Any], side: str, target: str) -> dict[str, Any]:
    t = Q(source["exact_representative_box"]["t"][0 if side == "LOWER_T" else 1])
    reflected = source["exact_reflected_box"]
    if source["pair_index"] == 787:
        rt, rside = t, side
        rtarget = "G[1,0]" if target == "G[1,1]" else target
        formula = "N_TO_S__t_FIXED__p_NEGATED__y_REFLECTED"
    else:
        rt = -t
        rside = "UPPER_T" if side == "LOWER_T" else "LOWER_T"
        rtarget = "W[1,1]" if target == "W[1,0]" else target
        formula = "E_FIXED__t_NEGATED__p_NEGATED__y_REFLECTED"
    need(Q(reflected["t"][0 if rside == "LOWER_T" else 1]) == rt,
         "reflected face t")
    return {"compact_chart": reflected["compact_chart"], "face_axis": "t",
            "face_side": rside, "exact_t": str(rt),
            "exact_p_interval": list(normalized_interval(reflected["p"])),
            "exact_s": "0", "reflected_tangency_target": rtarget,
            "horizontal_reflection_formula": formula}


def validate_endpoint(candidate: dict[str, Any], source: dict[str, Any],
                      strata: dict[str, Any], side: str,
                      adjacency: dict[tuple[int, str, tuple[str, str]],
                                      list[tuple[dict[str, Any], str]]],
                      strata_by_c72: dict[str, dict[str, Any]],
                      cells: dict[str, dict[str, Any]], all_cells: list[dict[str, Any]]) -> None:
    lineage = PAIR[source["pair_index"]]
    target = lineage["target"]
    parent = lineage["origin"]
    box = iv.parse_box(source)
    t0, t1, p0, p1 = box
    t = t0 if side == "LOWER_T" else t1
    face = (t, t, p0, p1)
    full = root_raw(face, parent, target)["delta"]
    need(sign(full.d[1]) in {"NEGATIVE", "POSITIVE"}, "endpoint strict dp")
    midpoint = (p0 + p1) / 2
    value = root_raw((t, t, midpoint, midpoint), parent, target)["delta"].v
    image = iv.rat(midpoint) - value / full.d[1]
    need(bool(image > iv.rat(p0)) and bool(image < iv.rat(p1)),
         "endpoint independent Newton")
    physical = {"representative_origin_key": lineage["origin"],
                "equation": "collision1_Delta_" + target + "=0",
                "tangency_target": target, "exact_t": str(t), "exact_s": "0"}
    root_id = "c75-first-tangency-root:" + obj(physical)
    face_value = {"compact_chart": lineage["origin"].split(":")[1],
                  "face_axis": "t", "face_side": side, "exact_t": str(t),
                  "exact_p_interval": [str(p0), str(p1)], "exact_s": "0"}
    reflected = reflected_face(source, side, target)
    glue = {"representative_face": face_value, "reflected_face": reflected,
            "C37_pair_row_sha256": lineage["c37"],
            "reflection_is_exact_bijective_involution": True}
    key = face_key(source, side)
    entries = adjacency[key]
    opposite = [(row, row_side) for row, row_side in entries
                if row["row_sha256"] != source["row_sha256"] and row_side != side]
    need(len(opposite) <= 1, "endpoint adjacency")
    if opposite:
        neighbor, neighbor_side = opposite[0]
        in_scope = neighbor["row_sha256"] in strata_by_c72
        owner = source if side == "LOWER_T" else neighbor
        expected_adjacency = {
            "incidence_kind": ("IN_SCOPE_MATCHED_TANGENCY_SEGMENT" if in_scope else
                               "OUT_OF_SCOPE_C72_DOWNSTREAM_OWNER"),
            "incidence_degree_including_downstream": 2,
            "neighbor_C72_obligation_row_sha256": neighbor["row_sha256"],
            "neighbor_face_side": neighbor_side,
            "neighbor_child_path": neighbor["child_path"],
            "neighbor_child_route_witness": neighbor["child_route_witness"],
            "neighbor_structural_category": neighbor["structural_category"],
            "neighbor_C75_strata_row_sha256":
                strata_by_c72[neighbor["row_sha256"]]["row_sha256"] if in_scope else None,
            "half_open_owner_C72_obligation_row_sha256": owner["row_sha256"],
            "half_open_rule": "LOWER_T_FACE_INCLUSIVE__UPPER_T_FACE_EXCLUSIVE",
            "current_occurrence_is_half_open_owner": owner is source,
            "classified_boundary_not_dangling": True,
        }
    else:
        current = cells[lineage["cell"]]
        adjacent_cells = [row for row in all_cells
                          if row.get("cell_id") != current["cell_id"] and
                          row.get("gate3_chart") == current["gate3_chart"] and
                          row.get("gate3_product_box", {}).get("p") ==
                          current["gate3_product_box"]["p"] and
                          str(t) in [str(Q(item)) for item in
                                     row.get("gate3_product_box", {}).get("t", [])]]
        need(len(adjacent_cells) <= 1, "C32 adjacency")
        if adjacent_cells:
            neighbor = adjacent_cells[0]
            expected_adjacency = {
                "incidence_kind": "C32_ATLAS_CELL_BOUNDARY_OWNER",
                "incidence_degree_including_downstream": 2,
                "neighbor_C32_cell_id": neighbor["cell_id"],
                "neighbor_C32_cell_row_sha256": neighbor["row_sha256"],
                "neighbor_exact_parent_t_interval": neighbor["gate3_product_box"]["t"],
                "half_open_owner_C72_obligation_row_sha256": source["row_sha256"],
                "half_open_rule": "LOWER_T_FACE_INCLUSIVE__UPPER_T_FACE_EXCLUSIVE",
                "current_occurrence_is_half_open_owner": True,
                "classified_boundary_not_dangling": True,
            }
        else:
            need(side == "UPPER_T" and source["pair_index"] == 711 and
                 str(t) == "-531/800", "outer guard boundary")
            expected_adjacency = {
                "incidence_kind": "C32_ATLAS_OUTER_GUARD_BOUNDARY_TERMINAL",
                "incidence_degree_including_boundary_terminal": 1,
                "boundary_terminal_owner_C32_cell_id": current["cell_id"],
                "boundary_terminal_owner_C32_cell_row_sha256": current["row_sha256"],
                "half_open_owner_C72_obligation_row_sha256": source["row_sha256"],
                "half_open_rule": "TERMINAL_UPPER_ATLAS_FACE_INCLUDED_BY_OUTER_GUARD_EXCEPTION",
                "current_occurrence_is_half_open_owner": True,
                "classified_boundary_not_dangling": True,
            }
    occurrence = {"root_id": root_id, "C72": source["row_sha256"], "side": side}
    need(candidate["schema"] ==
         "cm2.round306c75.first-tangency-exact-strata-oracle.v1.endpoint-incidence-row" and
         candidate["endpoint_occurrence_id"] ==
         "c75-endpoint-occurrence:" + obj(occurrence) and
         candidate["root_id"] == root_id and
         candidate["root_identity_preimage"] == physical and
         candidate["C72_obligation_row_sha256"] == source["row_sha256"] and
         candidate["C75_strata_row_sha256"] == strata["row_sha256"] and
         candidate["endpoint_side"] == side and
         candidate["exact_face_key"] == face_value and
         candidate["exact_face_key_sha256"] == obj(face_value) and
         candidate["representative_reflected_exact_glue"] == glue and
         candidate["representative_reflected_exact_glue_sha256"] == obj(glue) and
         candidate["adjacency_and_half_open_owner"] == expected_adjacency,
         "endpoint exact rebuild")
    root = candidate["endpoint_root_enclosure"]
    need(root["precision_bits"] == 384 and root["graph_axis"] == "p" and
         root["interval_Newton"]["strict_derivative"] is True and
         root["interval_Newton"]["strict_interior_self_map"] is True and
         root["unique_root_on_exact_t_face"] is True and
         candidate["source_grazing"] is False and candidate["dangling"] is False and
         candidate["duplicate_occurrence"] is False and
         candidate["formal_credit"] == candidate["whole_parent_credit"] ==
         candidate["D02_gate_credit"] == candidate["CM2_credit"] == 0,
         "endpoint numeric/credit")


def attacks(result: dict[str, Any], row: dict[str, Any], endpoint: dict[str, Any]) -> dict[str, Any]:
    checks = {
        "result_status": lambda x: x.__setitem__("status", "PASS_MUTANT"),
        "result_scope": lambda x: x["scope"].__setitem__("row_count", SCOPE + 1),
        "result_graphs": lambda x: x["decision_census"].__setitem__("exact_unique_regular_p_axis_Newton_graphs", SCOPE - 1),
        "result_sides": lambda x: x["decision_census"].__setitem__("strict_exclusion_open_side_instances", 1),
        "result_terminals": lambda x: x["decision_census"].__setitem__("cemetery_first_tangency_graph_terminals", 0),
        "result_unresolved": lambda x: x["decision_census"].__setitem__("unresolved_strata", 1),
        "result_credit": lambda x: x["strict_boundary"].__setitem__("formal_credit", 1),
        "row_target": lambda x: x.__setitem__("tangency_target", "W[9,9]"),
        "row_axis": lambda x: x["full_child_tangency_graph"].__setitem__("graph_axis", "t"),
        "row_Newton": lambda x: x["full_child_tangency_graph"]["interval_Newton"].__setitem__("strict_interior_self_map", False),
        "row_graph_exclusion": lambda x: x["three_strata"]["zero_graph"].__setitem__("strict_exclusion", True),
        "row_graph_exit": lambda x: x["three_strata"]["zero_graph"].__setitem__("exit_class", "STRICT_EXCLUSION"),
        "row_side_exit": lambda x: x["three_strata"]["positive_open_side"].__setitem__("exit_class", "SEALED_COLLISION3_HANDOFF"),
        "row_incidence": lambda x: x["face_corner_source_glue_and_incidence"].__setitem__("t_lower_graph_endpoint_incidence", 0),
        "row_source": lambda x: x["face_corner_source_glue_and_incidence"].__setitem__("source_grazing", True),
        "row_owner": lambda x: x["half_open_ownership_and_Kraft"].__setitem__("graph_is_not_double_owned", False),
        "row_depth": lambda x: x["half_open_ownership_and_Kraft"].__setitem__("additional_dyadic_depth", 1),
        "row_Kraft": lambda x: x["half_open_ownership_and_Kraft"].__setitem__("typed_graph_Kraft", "1"),
        "row_credit": lambda x: x.__setitem__("D02_gate_credit", 1),
        "endpoint_root": lambda x: x.__setitem__("root_id", "c75-first-tangency-root:bad"),
        "endpoint_face": lambda x: x["exact_face_key"].__setitem__("exact_t", "0"),
        "endpoint_newton": lambda x: x["endpoint_root_enclosure"]["interval_Newton"].__setitem__("strict_interior_self_map", False),
        "endpoint_neighbor": lambda x: x["adjacency_and_half_open_owner"].__setitem__("classified_boundary_not_dangling", False),
        "endpoint_dangling": lambda x: x.__setitem__("dangling", True),
        "endpoint_credit": lambda x: x.__setitem__("formal_credit", 1),
    }
    outcome = {}
    for name, mutate in checks.items():
        source = (result if name.startswith("result_") else
                  endpoint if name.startswith("endpoint_") else row)
        mutant = copy.deepcopy(source)
        mutate(mutant)
        try:
            need(mutant == source, "attack:" + name)
        except Reject:
            outcome[name] = "FAIL_CLOSED"
        else:
            raise Reject("escaped attack:" + name)
    framing = [b"", b"\xef\xbb\xbf{}\n", b'{"a":1,"a":2}\n', b'{"x":NaN}\n', b"{}\x00\n", b"{ }\n"]
    for index, raw in enumerate(framing):
        try:
            value = parse_json(raw, "attack")
            need(value == {}, "framing attack")
        except Exception:
            outcome[f"framing_{index}"] = "FAIL_CLOSED"
        else:
            raise Reject("escaped framing attack")
    return {"attack_count": len(outcome), "attacks": outcome,
            "status": f"PASS_{len(outcome)}_OF_{len(outcome)}_COHERENT_ATTACKS_FAIL_CLOSED"}


def emit(path: Path, raw: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL |
                 getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0), 0o644)
    try:
        view = memoryview(raw)
        while view:
            count = os.write(fd, view)
            need(count > 0, "short write")
            view = view[count:]
        os.fsync(fd)
    finally:
        os.close(fd)
    need(path.read_bytes() == raw and path.lstat().st_nlink == 1,
         "verification terminal replay")


def verify(a: Path, b: Path, do_emit: bool) -> dict[str, Any]:
    need(a.is_dir() and b.is_dir() and a != b, "candidate dirs")
    need(ctx.prec == PRECISION, "precision")
    # This is a declaration-only equality.  There is intentionally no producer
    # path in this verifier and no attempt to recapture its bytes.
    need(len(PRODUCER_SOURCE_SHA) == 64 and "_" not in PRODUCER_SOURCE_SHA,
         "frozen producer declaration")
    support = Path(iv.__file__).absolute().read_bytes()
    need(sha(support) == SUPPORT_SOURCE_SHA, "independent kernel source pin")
    candidate_raw: dict[str, bytes] = {}
    for name in MEMBERS:
        expected_sha, expected_size = CANDIDATE_PINS[name]
        left = secure(a / name, expected_sha, expected_size)
        right = secure(b / name, expected_sha, expected_size)
        need(left == right, "dual candidate bytes:" + name)
        candidate_raw[name] = left
    result = parse_json(candidate_raw[RESULT], "result")
    outer = parse_json(candidate_raw[OUTER], "outer")
    for value, expected, label in ((result, CANDIDATE_RESULT_OBJECT, "result"),
                                   (outer, CANDIDATE_OUTER_OBJECT, "outer")):
        body = copy.deepcopy(value)
        claim = body.pop("object_sha256", None)
        need(claim == expected == obj(body), label + ":object closure")
    need(result["producer_file_sha256"] == PRODUCER_SOURCE_SHA and
         outer["producer_file_sha256"] == PRODUCER_SOURCE_SHA and
         outer["result_object_sha256"] == CANDIDATE_RESULT_OBJECT,
         "producer declaration/result binding")
    ledger_rows, ledger_sequence = rows(candidate_raw[LEDGER], "candidate ledger")
    need(len(ledger_rows) == SCOPE and ledger_sequence == CANDIDATE_ROW_SEQUENCE and
         result["ledger"]["row_hash_line_sequence_sha256"] == CANDIDATE_ROW_SEQUENCE,
         "candidate ledger descriptor")
    endpoint_rows, endpoint_sequence = rows(candidate_raw[ENDPOINTS],
                                             "candidate endpoint ledger")
    need(len(endpoint_rows) == 11_768 and
         endpoint_sequence == result["endpoint_incidence_ledger"]
         ["row_hash_line_sequence_sha256"], "endpoint ledger descriptor")
    manifest = "".join(
        f"{sha(candidate_raw[name])}  {name}\n"
        for name in (LEDGER, ENDPOINTS, RESULT, REPORT)
    ).encode("ascii")
    need(candidate_raw[MANIFEST] == manifest, "manifest exact rebuild")
    upstream_raw = {key: secure(*value) for key, value in UPSTREAM.items()}
    need(upstream_raw["C72_A"] == upstream_raw["C72_B"], "dual C72")
    all72, seq72 = rows(upstream_raw["C72_A"], "C72")
    need(len(all72) == 134_155 and seq72 ==
         "2cd348f1821c5d2158008bc8fda4c500388902e385a31e87e281cd6a69be587b",
         "C72 descriptor")
    selected = [row for row in all72 if row["child_route_witness"] == SELECTOR]
    need(len(selected) == SCOPE and sequence(row["row_sha256"] for row in selected) ==
         SELECTED_SEQUENCE, "exact current selector")
    c37, _ = rows(upstream_raw["C37"], "C37")
    c32, _ = rows(upstream_raw["C32"], "C32")
    by_pair = {row["pair_index"]: row for row in c37 if row.get("pair_index") in PAIR}
    by_cell = {row.get("cell_id"): row for row in c32 if row.get("cell_id") in
               {item["cell"] for item in PAIR.values()}}
    need(set(by_pair) == set(PAIR) and len(by_cell) == len(PAIR), "lineage domain")
    for pair, item in PAIR.items():
        need(by_pair[pair]["row_sha256"] == item["c37"] and
             by_pair[pair]["representative_origin_key"] == item["origin"] and
             by_cell[item["cell"]]["row_sha256"] == item["c32"], "lineage")
    pair_census, target_census = Counter(), Counter()
    for index, (candidate, source) in enumerate(zip(ledger_rows, selected, strict=True)):
        proof = independent_decision(source)
        validate_candidate(candidate, source, proof)
        pair_census[source["pair_index"]] += 1
        target_census[proof["target"]] += 1
    need(pair_census == Counter({31: 2154, 200: 809, 270: 46, 711: 2644, 787: 231}) and
         target_census == Counter({"W[1,0]": 5653, "G[1,1]": 231}), "census")
    strata_by_c72 = {row["C72_obligation_row_sha256"]: row for row in ledger_rows}
    wanted = {face_key(source, side) for source in selected
              for side in ("LOWER_T", "UPPER_T")}
    adjacency = {key: [] for key in wanted}
    for source in all72:
        for side in ("LOWER_T", "UPPER_T"):
            key = face_key(source, side)
            if key in adjacency:
                adjacency[key].append((source, side))
    cells = {row.get("cell_id"): row for row in c32
             if row.get("cell_id") in {item["cell"] for item in PAIR.values()}}
    need(len(cells) == len(PAIR), "endpoint C32 cells")
    endpoint_kinds = Counter()
    endpoint_index = 0
    for source, strata in zip(selected, ledger_rows, strict=True):
        for side in ("LOWER_T", "UPPER_T"):
            endpoint = endpoint_rows[endpoint_index]
            endpoint_index += 1
            validate_endpoint(endpoint, source, strata, side, adjacency,
                              strata_by_c72, cells, c32)
            endpoint_kinds[endpoint["adjacency_and_half_open_owner"]
                           ["incidence_kind"]] += 1
    need(endpoint_index == 11_768 and endpoint_kinds == Counter({
        "OUT_OF_SCOPE_C72_DOWNSTREAM_OWNER": 11_750,
        "IN_SCOPE_MATCHED_TANGENCY_SEGMENT": 16,
        "C32_ATLAS_CELL_BOUNDARY_OWNER": 1,
        "C32_ATLAS_OUTER_GUARD_BOUNDARY_TERMINAL": 1,
    }), "endpoint incidence census")
    root_groups: dict[str, list[dict[str, Any]]] = {}
    for endpoint in endpoint_rows:
        root_groups.setdefault(endpoint["root_id"], []).append(endpoint)
    need(len(root_groups) == 11_760 and
         Counter(len(group) for group in root_groups.values()) ==
         Counter({1: 11_752, 2: 8}) and
         len({row["endpoint_occurrence_id"] for row in endpoint_rows}) == 11_768,
         "root degree/no duplicate census")
    for group in root_groups.values():
        if len(group) == 2:
            need({row["endpoint_side"] for row in group} == {"LOWER_T", "UPPER_T"} and
                 sum(bool(row["adjacency_and_half_open_owner"]
                          ["current_occurrence_is_half_open_owner"])
                     for row in group) == 1, "matched root unique owner")
    need(result["scope"]["row_count"] == SCOPE and
         result["decision_census"] == {
             "cemetery_first_tangency_graph_terminals": SCOPE,
             "exact_unique_regular_p_axis_Newton_graphs": SCOPE,
             "strict_exclusion_open_side_instances": 2 * SCOPE,
             "tangency_target_census": {"G[1,1]": 231, "W[1,0]": 5653},
             "unresolved_strata": 0,
             "whole_child_reported_as_strict_exclusion": 0,
         } and result["strict_boundary"]["formal_credit"] ==
         result["strict_boundary"]["whole_parent_credit"] ==
         result["strict_boundary"]["D02_gate_credit"] ==
         result["strict_boundary"]["CM2_credit"] == 0,
         "result semantics")
    endpoint_census = result["endpoint_incidence_census"]
    need(endpoint_census == {
        "C32_atlas_cell_boundary_occurrences": 1,
        "C32_atlas_outer_guard_terminal_occurrences": 1,
        "dangling": 0,
        "degree_one_with_explicit_downstream_or_boundary_owner": 11_752,
        "degree_two_in_scope_matched_root_ids": 8,
        "duplicate_occurrences": 0,
        "endpoint_occurrences": 11_768,
        "in_scope_matched_endpoint_occurrences": 16,
        "out_of_scope_C72_downstream_owner_occurrences": 11_750,
        "physical_root_ids": 11_760,
    }, "result endpoint census")
    attack_result = attacks(result, ledger_rows[0], endpoint_rows[0])
    verification = closed({
        "schema": SCHEMA,
        "status": "PASS_NO_C75_PRODUCER_READ_IMPORT_EXECUTION_OR_DECODE__5884_OF_5884_INDEPENDENT_EXACT_GRAPH_AND_TWO_SIDE_REBUILD__GRAPH_TERMINALS_NOT_EXCLUSIONS__UNRESOLVED_ZERO__ZERO_CREDIT",
        "verifier_file_sha256": sha(SELF.read_bytes()),
        "independent_kernel_file_sha256": SUPPORT_SOURCE_SHA,
        "producer_file_sha256_declaration_only": PRODUCER_SOURCE_SHA,
        "producer_source_policy": {"producer_path_in_runtime_input_set": False,
                                   "producer_source_opened": False,
                                   "producer_source_read_or_decoded": False,
                                   "producer_imported": False,
                                   "producer_compiled": False,
                                   "producer_executed": False,
                                   "producer_hash_consumed_as_declaration_only_binding": True},
        "candidate_file_sha256": {name: CANDIDATE_PINS[name][0] for name in MEMBERS},
        "candidate_result_object_sha256": CANDIDATE_RESULT_OBJECT,
        "candidate_outer_object_sha256": CANDIDATE_OUTER_OBJECT,
        "candidate_row_sequence_sha256": CANDIDATE_ROW_SEQUENCE,
        "dual_isolated_candidate_byte_identity": {name: True for name in MEMBERS},
        "recomputed_scope": {"row_count": SCOPE, "source_count": 2458,
                             "pair_census": {str(k): v for k, v in sorted(pair_census.items())},
                             "target_census": dict(sorted(target_census.items()))},
        "recomputed_decisions": {"unique_regular_full_p_graphs": SCOPE,
                                 "strict_open_side_exclusions": 2 * SCOPE,
                                 "cemetery_graph_terminals": SCOPE,
                                 "graph_terminals_reported_as_exclusions": 0,
                                 "unresolved_strata": 0,
                                 "additional_dyadic_depth": 0},
        "recomputed_endpoint_incidence": {
            "endpoint_occurrences": 11_768, "physical_root_ids": 11_760,
            "degree_two_in_scope_root_ids": 8,
            "out_of_scope_C72_owner_occurrences": 11_750,
            "C32_boundary_occurrences": 2,
            "dangling": 0, "duplicate_occurrences": 0,
            "all_exact_face_root_reflection_glue_rebuilt": True,
            "all_half_open_owners_unique": True,
        },
        "all_full_face_corner_root_order_glue_incidence_half_open_Kraft_closed": True,
        "coherent_attacks": attack_result,
        "post_scan_input_pin_recapture": True,
        "verification_O_EXCL_terminal_byte_replay": do_emit,
        "strict_boundary": {"candidate_is_authority": False,
                            "global_consumption_ready": False,
                            "runtime_canonical_pointer_or_seal_writes": False,
                            "formal_credit": 0, "whole_parent_credit": 0,
                            "D02_gate_credit": 0, "CM2_credit": 0,
                            "CM2": "NO-GO_FOR_CLAIM"},
    })
    # Recapture immutable candidates and upstream pins after the full scan.
    for name in MEMBERS:
        expected_sha, expected_size = CANDIDATE_PINS[name]
        need(secure(a / name, expected_sha, expected_size) == candidate_raw[name] and
             secure(b / name, expected_sha, expected_size) == candidate_raw[name],
             "postscan candidate recapture")
    for key, value in UPSTREAM.items():
        need(secure(*value) == upstream_raw[key], "postscan upstream recapture")
    raw_verification = canonical(verification) + b"\n"
    if do_emit:
        need(not (a / VERIFICATION).exists() and not (b / VERIFICATION).exists(),
             "fresh verification targets")
        emit(a / VERIFICATION, raw_verification)
        emit(b / VERIFICATION, raw_verification)
        need((a / VERIFICATION).read_bytes() == (b / VERIFICATION).read_bytes() ==
             raw_verification, "dual verification bytes")
    return verification


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-a", type=Path, required=True)
    parser.add_argument("--candidate-b", type=Path, required=True)
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()
    ctx.prec = PRECISION
    value = verify(args.candidate_a.resolve(), args.candidate_b.resolve(), args.emit)
    print(json.dumps({"status": value["status"],
                      "object_sha256": value["object_sha256"],
                      "attacks": value["coherent_attacks"]["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Reject, OSError, ValueError, KeyError, TypeError, IndexError,
            RuntimeError, json.JSONDecodeError) as error:
        print(f"FAIL_CLOSED:{type(error).__name__}:{error}", file=sys.stderr)
        raise SystemExit(2)
