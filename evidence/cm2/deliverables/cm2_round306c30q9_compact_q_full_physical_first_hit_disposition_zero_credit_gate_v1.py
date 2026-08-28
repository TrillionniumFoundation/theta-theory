#!/usr/bin/env python3
"""Append-only Q9 complete physical first-hit research disposition gate.

This program closes the three Q8 research gaps with full finite-horizon target
completeness, whole-origin interval templates, and explicit strict LIVE and
EXCLUDED subboxes.  It is deliberately future-C30f-gated and mints no credit.
"""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
from typing import Any

from flint import arb, ctx


sys.dont_write_bytecode = True
HERE = Path(__file__).absolute().parent
ROOT = HERE.parent
SCHEMA = "cm2.round306c30q9.compact-q-full-physical-first-hit-disposition.zero-credit.v1"
K = Q(1023, 262144)
RW = Q(4, 25)
RG = Q(9, 25)
S_DOMAIN = (Q(-1, 400), Q(1, 400))
R_DOMAIN = (Q(0), Q(1))

INPUTS = {
    "q8_manifest": (
        ".cm2-runtime/audit/c30q8-full-54-global-template-zero-credit-v1-20260808T112500Z/manifest.sha256",
        "2105ce1e7e898a33a3beb05063f203799e10430a4d5498a47e1e4db744c60a73",
    ),
    "q8_receipt": (
        ".cm2-runtime/audit/c30q8-full-54-global-template-zero-credit-v1-20260808T112500Z/receipt.json",
        "760a21c62bc22820b1a03cd5b72aa61d776ff7d7860d0926c1bfc11305383a1c",
    ),
    "q8_candidate": (
        ".cm2-runtime/audit/c30q8-full-54-global-template-zero-credit-v1-20260808T112500Z/producer_seed30880079_stdout.json",
        "e15cbad0515af501d2d5be2d7c01b9f5d77bd97598b7c6f0efef7e513efcdb1c",
    ),
    "geometry_registry": (
        "deliverables/cm2_gate3_candidate_first_hit_cert.py",
        "6d224d74cda186a40ef9956d1dd6556d5a7b9f506d47c942427ceb66fd705bd2",
    ),
    "round176_verifier": (
        "deliverables/cm2_round176_dimension_safe_multi_origin_parent_exclusion_verifier.py",
        "f1297881f724cb0a2087ebbfa6961a95750dffa751c003879eb2e14714581796",
    ),
    "c30b_producer": (
        "deliverables/cm2_round306c30b_source_w_outgoing_h_whole_origin_disposition_producer.py",
        "003191131bff227453d07fa22ecd6e95b4f9d48e9ff74604ea4b7116f5818762",
    ),
}

BRIDGE_TOKENS = ("03.15.11110101",)
MISS_TOKENS = (
    "06.00.00101010",
    "06.00.10000000",
    "06.00.10000010",
)
ROUTE_TOKENS = (
    "04.00.00001010",
    "04.00.00100000",
    "04.00.00100010",
    "04.00.00101000",
    "04.00.00101010",
    "04.00.10000000",
)
MIXED_TOKENS = ROUTE_TOKENS[1:]
SWITCH = {
    "04.00.00001010": Q(1, 2),
    "04.00.00100000": Q(1, 2),
    "04.00.00100010": Q(1, 2),
    "04.00.00101000": Q(63, 64),
    "04.00.00101010": Q(63, 64),
    "04.00.10000000": Q(63, 64),
}
LIVE_T = {
    "04.00.00100000": Q(27789, 512000),
    "04.00.00100010": Q(28497, 512000),
    "04.00.00101000": Q(34161, 512000),
    "04.00.00101010": Q(1593, 20480),
    "04.00.10000000": Q(45489, 512000),
}
T1_TARGETS = (
    "G[0,0]", "G[0,1]", "G[1,0]", "G[1,1]",
    "W[-1,0]", "W[0,-1]", "W[0,0]", "W[0,1]", "W[1,0]",
)
T32_TARGETS = (
    "G[-1,0]", "G[-1,1]", "G[0,-1]", "G[0,0]", "G[0,1]", "G[0,2]",
    "G[1,-1]", "G[1,0]", "G[1,1]", "G[1,2]", "G[2,0]", "G[2,1]",
    "W[-1,-1]", "W[-1,0]", "W[-1,1]", "W[0,-1]", "W[0,0]",
    "W[0,1]", "W[1,-1]", "W[1,0]", "W[1,1]",
)


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def capture(path: Path) -> bytes:
    absolute = path.absolute()
    need(absolute.resolve(strict=True) == absolute, "canonical input:" + str(path))
    before = os.lstat(absolute)
    need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
         "regular single-link input:" + str(path))
    raw = absolute.read_bytes()
    after = os.lstat(absolute)
    fields = ("st_dev", "st_ino", "st_mode", "st_nlink", "st_size",
              "st_mtime_ns", "st_ctime_ns", "st_uid", "st_gid")
    need(all(getattr(before, field) == getattr(after, field) for field in fields),
         "stable input:" + str(path))
    return raw


def pinned(name: str) -> bytes:
    relative, expected = INPUTS[name]
    raw = capture(ROOT / relative)
    need(hashlib.sha256(raw).hexdigest() == expected, "input pin:" + name)
    return raw


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in result, "duplicate JSON key:" + label)
            result[key] = value
        return result
    try:
        value = json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=unique,
                           parse_float=lambda token: token,
                           parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)))
    except (UnicodeDecodeError, ValueError, json.JSONDecodeError) as error:
        raise Reject("strict JSON:" + label) from error
    need(type(value) is dict, "JSON object:" + label)
    return value


def verify_q8_manifest() -> int:
    manifest = ROOT / INPUTS["q8_manifest"][0]
    base = manifest.parent
    rows = pinned("q8_manifest").decode("ascii", "strict").splitlines()
    seen: set[str] = set()
    for row in rows:
        need(len(row) >= 67 and row[64:66] == "  ", "Q8 manifest syntax")
        expected, member = row[:64], row[66:]
        part = Path(member)
        need(all(char in "0123456789abcdef" for char in expected)
             and not part.is_absolute() and ".." not in part.parts and member not in seen,
             "Q8 manifest row")
        seen.add(member)
        workspace = ROOT / part
        target = workspace if workspace.exists() else base / part
        need(target.absolute().is_relative_to(ROOT), "Q8 manifest scope")
        need(hashlib.sha256(capture(target)).hexdigest() == expected,
             "Q8 manifest member:" + member)
    need(bool(rows), "nonempty Q8 manifest")
    return len(rows)


def origins(tokens: tuple[str, ...] | list[str]) -> list[str]:
    return sorted(origin for token in tokens
                  for origin in ("W:N:" + token, "W:S:H." + token))


def token_of(origin: str) -> str:
    return origin.split(":")[-1].removeprefix("H.")


def aq(value: Q) -> arb:
    return arb(value.numerator) / value.denominator


def interval(lower: Q, upper: Q) -> arb:
    need(lower <= upper, "interval order")
    middle, radius = (lower + upper) / 2, (upper - lower) / 2
    return aq(middle) + arb(0, aq(radius).upper())


def bound(value: arb) -> dict[str, str]:
    return {"lower": str(value.lower()), "upper": str(value.upper())}


def hydrate(row: dict[str, Any]) -> dict[str, Any]:
    result = dict(row)
    result["t_domain_q"] = tuple(Q(value) for value in row["t_domain"])
    result["s_domain_q"] = tuple(Q(value) for value in row["s_domain"])
    need(result["s_domain_q"] == S_DOMAIN and row["r_domain"] == ["0", "1"],
         "Q8 exact s/r domains:" + row["origin_key"])
    return result


def target(target_id: str, s: arb) -> tuple[arb, arb, Q]:
    match = re.fullmatch(r"([GW])\[(-?\d+),(-?\d+)\]", target_id)
    need(match is not None, "target id:" + target_id)
    kind, ix_text, iy_text = match.groups()
    ix, iy = int(ix_text), int(iy_text)
    if kind == "G":
        return arb(ix), arb(iy), RG
    return arb(ix) + aq(Q(1, 2)) + s, arb(iy) + aq(Q(1, 2)), RW


def flight(origin: dict[str, Any], r_domain: tuple[Q, Q], target_id: str,
           *, t_domain: tuple[Q, Q] | None = None,
           s_domain: tuple[Q, Q] | None = None) -> tuple[dict[str, Any], dict[str, arb]]:
    td = origin["t_domain_q"] if t_domain is None else t_domain
    sd = origin["s_domain_q"] if s_domain is None else s_domain
    t = interval(*td)
    s = interval(*sd)
    a = (arb(1) - t * t).sqrt()
    north = origin["source_chart"] == "W:N"
    nx, ny = t, a if north else -a
    b = aq(K).sqrt() * interval(*r_domain)
    p_abs = (arb(1) - b * b).sqrt()
    p = p_abs if origin["p_sign"] == 1 else -p_abs
    ux, uy = b * nx - p * ny, b * ny + p * nx
    qx, qy = aq(Q(1, 2)) + s + aq(RW) * nx, aq(Q(1, 2)) + aq(RW) * ny
    ax, ay, radius = target(target_id, s)
    dx, dy = ax - qx, ay - qy
    ell = ux * dx + uy * dy
    transverse = -uy * dx + ux * dy
    f0 = dx * dx + dy * dy - aq(radius * radius)
    delta = aq(radius * radius) - transverse * transverse
    values = {"ell": ell, "f0": f0, "delta": delta,
              "ell_plus_radius": ell + aq(radius)}
    if bool(delta > 0):
        radical = delta.sqrt()
        values["tau_minus"] = ell - radical
        values["tau_plus"] = ell + radical
    return ({
        "target": target_id,
        "t_domain": [str(td[0]), str(td[1])],
        "s_domain": [str(sd[0]), str(sd[1])],
        "r_domain": [str(r_domain[0]), str(r_domain[1])],
        "bounds": {key: bound(value) for key, value in values.items()},
    }, values)


def need_hit(values: dict[str, arb], horizon: Q, label: str) -> None:
    need("tau_minus" in values and bool(values["f0"] > 0)
         and bool(values["ell"] > 0) and bool(values["delta"] > 0)
         and bool(values["tau_minus"] > 0) and bool(values["tau_minus"] < aq(horizon)),
         "strict future hit:" + label)


def competitor_class(values: dict[str, arb], radius: Q, label: str) -> str:
    if bool(values["delta"] < 0):
        return "NO_REAL_CONTACT"
    if bool(values["ell"] + aq(radius) < 0):
        return "STRICTLY_BEHIND__TAU_PLUS_LT_0"
    raise Reject("unresolved competitor:" + label)


def completeness(horizon: Q) -> dict[str, Any]:
    possible: list[str] = []
    excluded_gaps: list[Q] = []
    for kind in ("G", "W"):
        radius = RG if kind == "G" else RW
        threshold = horizon + RW + radius
        for ix in range(-5, 6):
            for iy in range(-5, 6):
                if kind == "W":
                    distance_squared = Q(ix * ix + iy * iy)
                else:
                    xlo, xhi = Q(199, 400), Q(201, 400)
                    dx = xlo - ix if ix < xlo else (Q(ix) - xhi if ix > xhi else Q(0))
                    distance_squared = dx * dx + (Q(iy) - Q(1, 2)) ** 2
                gap = distance_squared - threshold * threshold
                name = f"{kind}[{ix},{iy}]"
                if gap <= 0:
                    possible.append(name)
                else:
                    excluded_gaps.append(gap)
    possible.sort()
    expected = sorted(T1_TARGETS if horizon == 1 else T32_TARGETS)
    expected_gap = Q(29137, 160000) if horizon == 1 else Q(65937, 160000)
    need(possible == expected and min(excluded_gaps) == expected_gap,
         "exact finite physical target family:" + str(horizon))
    return {
        "horizon": str(horizon),
        "possible_target_count_including_source_self": len(possible),
        "possible_targets": possible,
        "first_excluded_squared_distance_margin": str(min(excluded_gaps)),
        "infinite_lattice_tail_bound": (
            "W outside {-1,0,1}^2 has center distance >=2; "
            "G outside {-1,0,1,2}^2 has one coordinate distance >=999/400"
        ),
        "triangle_inequality_is_necessary_for_any_tau_le_horizon": True,
    }


def self_no_reentry() -> dict[str, Any]:
    return {
        "target": "W[0,0]",
        "identity": "distance_from_source_center_squared=(4/25)^2+2*(4/25)*sqrt(K)*r*tau+tau^2",
        "domain": "r>=0 and tau>0",
        "strictly_greater_than_source_radius_squared": True,
    }


def load_q8() -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    manifest_count = verify_q8_manifest()
    receipt = strict_json(pinned("q8_receipt"), "Q8 receipt")
    candidate = strict_json(pinned("q8_candidate"), "Q8 candidate")
    need(receipt["status"] == (
        "PASS_C30Q8_DUAL_SEED_FULL_54_GLOBAL_TEMPLATE_AUDIT__"
        "36_RESEARCH_EXCLUSION_CANDIDATES__18_BLOCKERS__ZERO_CREDIT"),
        "Q8 receipt status")
    boundary = receipt["formal_boundary"]
    need(boundary["formal_credit"] == 0 and boundary["ledger_unchanged"] is True
         and boundary["source_W_formal_remaining"] == 80
         and boundary["compact_q_formal_remaining_origins"] == 54
         and boundary["CM2"] == "NO-GO_FOR_CLAIM", "Q8 strict zero-credit boundary")
    need(candidate["schema"] == "cm2.round306c30q8.compact-q-54-global-template-audit.zero-credit.v1"
         and candidate["result_sha256"] == digest(candidate["result"]), "Q8 candidate closure")
    closure = candidate["result"]["classification_closure"]
    need(closure["total_origins"] == 54 and closure["research_EXCLUDED_candidates"] == 36
         and closure["undecided_global_miss_origins"] == 6
         and closure["RESOLVED_MIXED_route_candidates_not_exhaustively_proved"] == 12,
         "Q8 36+18 closure")
    rows = candidate["result"]["historic_full_census"]["origin_rows"]
    census = {row["origin_key"]: hydrate(row) for row in rows}
    need(len(census) == len(rows) == 54, "Q8 unique 54-origin census")
    q8_theorems = candidate["result"]["whole_origin_theorem_candidates"]
    q8_blockers = candidate["result"]["explicit_blockers"]
    need(len(q8_theorems) == 36 and len(q8_blockers) == 18
         and {row["origin_key"] for row in q8_theorems + q8_blockers} == set(census),
         "Q8 theorem/blocker partition")
    return census, {
        "manifest_sha256": INPUTS["q8_manifest"][1],
        "manifest_member_count": manifest_count,
        "receipt_sha256": INPUTS["q8_receipt"][1],
        "candidate_sha256": INPUTS["q8_candidate"][1],
        "candidate_result_sha256": candidate["result_sha256"],
        "inherited_research_EXCLUDED_origin_keys": sorted(
            row["origin_key"] for row in q8_theorems
        ),
        "inherited_native_research_EXCLUDED_count": 34,
        "bridge_pending_count_at_Q8": 2,
        "formal_predecessor": False,
    }


def physical_bridge(census: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for origin_key in origins(BRIDGE_TOKENS):
        origin = census[origin_key]
        reflected = "G[0,1]" if origin["source_chart"] == "W:N" else "G[0,0]"
        left_row, left = flight(origin, (Q(0), Q(1, 2)), "W[-1,0]")
        right_row, right = flight(origin, (Q(1, 2), Q(1)), reflected)
        seam_left_row, seam_left = flight(origin, (Q(1, 2), Q(1, 2)), "W[-1,0]")
        seam_right_row, seam_right = flight(origin, (Q(1, 2), Q(1, 2)), reflected)
        frozen_row, frozen = flight(origin, R_DOMAIN, "W[1,0]")
        for label, values in (("left", left), ("right", right),
                              ("seam-left", seam_left), ("seam-right", seam_right)):
            need_hit(values, Q(1), origin_key + ":" + label)
        need(bool(frozen["ell"] + aq(RW) < 0), "bridge frozen strictly behind")
        rows.append({
            "origin_key": origin_key,
            "research_disposition": "EXCLUDED",
            "reason": "COMPLETE_T1_PHYSICAL_FAMILY_HAS_A_HIT_BUT_FROZEN_W1_CANNOT_HIT",
            "left_witness": {**left_row, "assigned_half_open_r": "[0,1/2)"},
            "right_witness": {**right_row, "assigned_half_open_r": "[1/2,1]"},
            "switch_seam": {"r": "1/2", "owner": "right", "both_closed_proofs_strict": True,
                            "left": seam_left_row, "right": seam_right_row},
            "frozen_owner": frozen_row,
            "source_self_no_reentry": True,
            "formal_disposition_minted": False,
        })
    return rows


def miss_resolution(census: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for origin_key in origins(MISS_TOKENS):
        origin = census[origin_key]
        selected = "G[2,0]" if origin["source_chart"] == "W:N" else "G[2,1]"
        selected_row, selected_values = flight(origin, R_DOMAIN, selected)
        need_hit(selected_values, Q(3, 2), "06 unique first:" + origin_key)
        competitors: list[dict[str, Any]] = []
        for target_id in T32_TARGETS:
            if target_id == selected:
                continue
            if target_id == "W[0,0]":
                competitors.append({"target": target_id, "classification": "SOURCE_SELF_NO_REENTRY"})
                continue
            row, values = flight(origin, R_DOMAIN, target_id)
            radius = RG if target_id.startswith("G") else RW
            competitors.append({**row, "classification": competitor_class(
                values, radius, origin_key + ":" + target_id
            )})
        need(len(competitors) == 20, "complete T3/2 competitor count")
        rows.append({
            "origin_key": origin_key,
            "research_disposition": "EXCLUDED",
            "reason": "COMPLETE_T3_OVER_2_FAMILY_HAS_UNIQUE_NONFROZEN_FIRST_OWNER",
            "selected_unique_first_target": selected,
            "selected_hit": selected_row,
            "competitor_audit": competitors,
            "all_twenty_competitors_no_contact_or_behind_or_self": True,
            "formal_disposition_minted": False,
        })
    return rows


def seam_H(origin: dict[str, Any], r_domain: tuple[Q, Q]) -> tuple[dict[str, Any], arb]:
    t = interval(*origin["t_domain_q"])
    a = (arb(1) - t * t).sqrt()
    north = origin["source_chart"] == "W:N"
    nx, ny = t, a if north else -a
    b = aq(K).sqrt() * interval(*r_domain)
    p_abs = (arb(1) - b * b).sqrt()
    p = p_abs if origin["p_sign"] == 1 else -p_abs
    ux, uy = b * nx - p * ny, b * ny + p * nx
    h = aq(Q(1, 2)).sqrt()
    mx, my = -h, h if north else -h
    dx, dy = arb(1) + aq(RW) * mx - aq(RW) * nx, aq(RW) * my - aq(RW) * ny
    value = ux * dy - uy * dx
    return ({
        "seam": "NW" if north else "SW", "r_domain": [str(r_domain[0]), str(r_domain[1])],
        "H_bounds": bound(value), "half_open_rule": "E_OR_W_OWNS__N_OR_S_SHADOWS",
    }, value)


def contact_W_margins(origin: dict[str, Any], t_domain: tuple[Q, Q],
                      r_domain: tuple[Q, Q]) -> tuple[dict[str, Any], dict[str, arb]]:
    t = interval(*t_domain)
    a = (arb(1) - t * t).sqrt()
    north = origin["source_chart"] == "W:N"
    nx, ny = t, a if north else -a
    b = aq(K).sqrt() * interval(*r_domain)
    p_abs = (arb(1) - b * b).sqrt()
    p = p_abs if origin["p_sign"] == 1 else -p_abs
    ux, uy = b * nx - p * ny, b * ny + p * nx
    dx, dy = arb(1) - aq(RW) * nx, -aq(RW) * ny
    ell = ux * dx + uy * dy
    transverse = -uy * dx + ux * dy
    delta = aq(RW * RW) - transverse * transverse
    need(bool(delta > 0), "contact normal delta")
    radical = delta.sqrt()
    normal_x = (-radical * ux + transverse * uy) / aq(RW)
    normal_y = (-radical * uy - transverse * ux) / aq(RW)
    margins = {"W.first": -normal_x - normal_y, "W.second": -normal_x + normal_y}
    return ({"outgoing_chart": "W", "margins": {key: bound(value)
             for key, value in margins.items()}}, margins)


def route_resolution(census: dict[str, dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    epsilon = Q(1, 2000000)
    for origin_key in origins(ROUTE_TOKENS):
        origin = census[origin_key]
        token = token_of(origin_key)
        switch = SWITCH[token]
        g_target = "G[1,1]" if origin["source_chart"] == "W:N" else "G[1,0]"
        left_row, left = flight(origin, (Q(0), switch), "W[1,0]")
        right_row, right = flight(origin, (switch, Q(1)), g_target)
        seam_w_row, seam_w = flight(origin, (switch, switch), "W[1,0]")
        seam_g_row, seam_g = flight(origin, (switch, switch), g_target)
        for label, values in (("left", left), ("right", right),
                              ("seam-W", seam_w), ("seam-G", seam_g)):
            need_hit(values, Q(1), origin_key + ":" + label)
        eliminated: list[dict[str, Any]] = []
        for target_id in T1_TARGETS:
            if target_id in {"W[1,0]", g_target}:
                continue
            if target_id == "W[0,0]":
                eliminated.append({"target": target_id, "classification": "SOURCE_SELF_NO_REENTRY"})
                continue
            proof_row, values = flight(origin, R_DOMAIN, target_id)
            radius = RG if target_id.startswith("G") else RW
            eliminated.append({**proof_row, "classification": competitor_class(
                values, radius, origin_key + ":" + target_id
            )})
        need(len(eliminated) == 7, "seven eliminated T1 competitors")
        common = {
            "origin_key": origin_key,
            "two_surviving_targets": ["W[1,0]", g_target],
            "eliminated_target_audit": eliminated,
            "two_box_cover": [
                {**left_row, "assigned_half_open_r": "[0," + str(switch) + ")"},
                {**right_row, "assigned_half_open_r": "[" + str(switch) + ",1]"},
            ],
            "switch_seam": {"r": str(switch), "owner": "right_G_witness",
                            "W_closed_proof_strict": True, "G_closed_proof_strict": True,
                            "W": seam_w_row, "G": seam_g_row},
            "historic_root_subdivision_count": 0,
            "first_target_tie_impossible_by_strict_obstacle_disjointness": True,
            "outgoing_half_open_partition": {
                "E": "nx>=abs(ny)", "W": "-nx>=abs(ny)",
                "N": "ny>abs(nx)", "S": "-ny>abs(nx)",
                "rule": "E_OR_W_OWNS__N_OR_S_SHADOWS",
                "frozen_live_chart": "W",
            },
            "formal_disposition_minted": False,
        }
        if token == ROUTE_TOKENS[0]:
            h_row, h_value = seam_H(origin, R_DOMAIN)
            need(bool(h_value < 0) if origin["source_chart"] == "W:N" else bool(h_value > 0),
                 "whole first-token outgoing mismatch")
            rows.append({
                **common,
                "research_disposition": "EXCLUDED",
                "reason": "G_FIRST_IS_OWNER_MISMATCH__W_FIRST_IS_STRICT_N_OR_S_CHART_MISMATCH",
                "whole_W_contact_seam_sign": h_row,
            })
            continue

        live_t = LIVE_T[token]
        tlo, thi = live_t - epsilon, live_t + epsilon
        need(origin["t_domain_q"][0] < tlo < thi < origin["t_domain_q"][1],
             "live t subbox interior")
        live_s = (-epsilon, epsilon)
        live_r = (Q(15, 1024), Q(17, 1024))
        live_w_row, live_w = flight(origin, live_r, "W[1,0]",
                                    t_domain=(tlo, thi), s_domain=live_s)
        live_g_row, live_g = flight(origin, live_r, g_target,
                                    t_domain=(tlo, thi), s_domain=live_s)
        need_hit(live_w, Q(1), "mixed LIVE W:" + origin_key)
        need(bool(live_g["delta"] < 0), "mixed LIVE G no-real:" + origin_key)
        chart_row, margins = contact_W_margins(origin, (tlo, thi), live_r)
        need(all(bool(value > 0) for value in margins.values()), "strict W chart:" + origin_key)

        midpoint = sum(origin["t_domain_q"], Q(0)) / 2
        ex_t = (midpoint - epsilon, midpoint + epsilon)
        ex_s = (-epsilon, epsilon)
        ex_r = (Q(127, 128), Q(1))
        ex_g_row, ex_g = flight(origin, ex_r, g_target, t_domain=ex_t, s_domain=ex_s)
        ex_w_row, ex_w = flight(origin, ex_r, "W[1,0]", t_domain=ex_t, s_domain=ex_s)
        need_hit(ex_g, Q(1), "mixed EXCLUDED G:" + origin_key)
        need(bool(ex_w["ell"] - aq(RW) > ex_g["tau_minus"]),
             "G precedes every possible W contact:" + origin_key)
        need(live_r[1] < ex_r[0], "LIVE/EXCLUDED subboxes disjoint")
        rows.append({
            **common,
            "research_disposition": "RESOLVED_MIXED",
            "reason": "EXHAUSTIVE_FIRST_TARGET_AND_HALF_OPEN_OUTGOING_CHART_PARTITION",
            "strict_positive_measure_LIVE_subbox": {
                "half_open_box": {"t": f"[{tlo},{thi})", "s": f"[{live_s[0]},{live_s[1]})",
                                  "r": f"[{live_r[0]},{live_r[1]})"},
                "W_unique_first": live_w_row, "G_no_real_contact": live_g_row,
                "strict_outgoing_W_chart": chart_row,
            },
            "strict_positive_measure_EXCLUDED_subbox": {
                "half_open_box": {"t": f"[{ex_t[0]},{ex_t[1]})", "s": f"[{ex_s[0]},{ex_s[1]})",
                                  "r": f"({ex_r[0]},{ex_r[1]}]"},
                "G_unique_first": ex_g_row, "possible_W_lower_bound": ex_w_row,
                "G_precedes_every_possible_W_contact": True,
            },
            "LIVE_and_EXCLUDED_subboxes_are_disjoint_and_nonempty": True,
        })

    # Exact minimality for the fixed W-left/G-right two-witness template family.
    first = census["W:N:04.00.00001010"]
    last = census["W:N:04.00.10000000"]
    test_r = Q(3, 4)
    first_mid = sum(first["t_domain_q"], Q(0)) / 2
    last_mid = sum(last["t_domain_q"], Q(0)) / 2
    first_bad_row, first_bad = flight(first, (test_r, test_r), "W[1,0]",
                                      t_domain=(first_mid, first_mid), s_domain=(Q(0), Q(0)))
    last_bad_row, last_bad = flight(last, (test_r, test_r), "G[1,1]",
                                    t_domain=(last_mid, last_mid), s_domain=(Q(0), Q(0)))
    need(bool(first_bad["delta"] < 0) and bool(last_bad["delta"] < 0),
         "one-switch impossibility counterexample")
    minimality = {
        "parameterized_template_schema_count": 1,
        "distinct_switch_value_count": 2,
        "switch_values": ["1/2", "63/64"],
        "two_switches_suffice_for_all_twelve_origins": True,
        "one_shared_switch_is_impossible": True,
        "proof": (
            "At r=3/4 the first token has no real W[1,0] contact and the last token "
            "has no real reflected-G contact. If a shared c>=3/4 its closed left-W proof "
            "contains the first counterexample; if c<=3/4 its closed right-G proof contains "
            "the last counterexample."
        ),
        "first_counterexample": first_bad_row,
        "last_counterexample": last_bad_row,
        "historic_root_by_root_subdivision_used": False,
    }
    return rows, minimality


def build() -> dict[str, Any]:
    ctx.prec = 256
    for name in ("geometry_registry", "round176_verifier", "c30b_producer"):
        pinned(name)
    census, q8 = load_q8()
    t1 = completeness(Q(1))
    t32 = completeness(Q(3, 2))
    bridge_rows = physical_bridge(census)
    miss_rows = miss_resolution(census)
    route_rows, minimality = route_resolution(census)

    inherited = set(q8["inherited_research_EXCLUDED_origin_keys"])
    bridge = set(origins(BRIDGE_TOKENS))
    native = inherited - bridge
    miss = set(origins(MISS_TOKENS))
    route_excluded = set(origins([ROUTE_TOKENS[0]]))
    mixed = set(origins(MIXED_TOKENS))
    need(len(native) == 34 and len(bridge) == 2 and len(miss) == 6
         and len(route_excluded) == 2 and len(mixed) == 10, "34+2+6+2+10 partition")
    groups = [native, bridge, miss, route_excluded, mixed]
    need(all(left.isdisjoint(right) for index, left in enumerate(groups)
             for right in groups[index + 1:]) and set().union(*groups) == set(census),
         "full mutually exclusive 54-origin partition")
    disposition_rows = sorted(
        ([{"origin_key": key, "research_disposition": "EXCLUDED",
           "evidence_class": "Q8_NATIVE_GLOBAL_TEMPLATE"} for key in native]
         + [{"origin_key": key, "research_disposition": "EXCLUDED",
             "evidence_class": "Q9_T1_PHYSICAL_COMPLETENESS_BRIDGE"} for key in bridge]
         + [{"origin_key": key, "research_disposition": "EXCLUDED",
             "evidence_class": "Q9_T3_OVER_2_UNIQUE_NONFROZEN_FIRST"} for key in miss]
         + [{"origin_key": key, "research_disposition": "EXCLUDED",
             "evidence_class": "Q9_TWO_TARGET_WHOLE_OUTGOING_MISMATCH"} for key in route_excluded]
         + [{"origin_key": key, "research_disposition": "RESOLVED_MIXED",
             "evidence_class": "Q9_TWO_TARGET_HALF_OPEN_EXHAUSTIVE_MIXED"} for key in mixed]),
        key=lambda row: row["origin_key"],
    )
    need(len(disposition_rows) == 54 and len({row["origin_key"] for row in disposition_rows}) == 54,
         "54-row disposition ledger")
    need(sum(row["research_disposition"] == "EXCLUDED" for row in disposition_rows) == 44
         and sum(row["research_disposition"] == "RESOLVED_MIXED" for row in disposition_rows) == 10,
         "44 EXCLUDED + 10 RESOLVED_MIXED")

    before = {"excluded": 74768, "conservative_live": 2064,
              "resolved_nonexcluded": 2010, "remaining": 54,
              "remaining_partition": {"compact_q": 54}}
    after = {"excluded": 74812, "conservative_live": 2020,
             "resolved_nonexcluded": 2020, "remaining": 0,
             "remaining_partition": {"compact_q": 0}}
    need(before["excluded"] + before["conservative_live"] == 76832
         and after["excluded"] + after["conservative_live"] == 76832
         and after["excluded"] - before["excluded"] == 44
         and after["resolved_nonexcluded"] - before["resolved_nonexcluded"] == 10
         and before["remaining"] - after["remaining"] == 54,
         "future C30f handoff arithmetic")

    return {
        "status": (
            "PASS_Q9_FULL_PHYSICAL_FIRST_HIT_RESEARCH_DISPOSITION__"
            "44_EXCLUDED__10_RESOLVED_MIXED__ZERO_CREDIT_PRE_TERMINAL"
        ),
        "verdict": "COMPLETE_RESEARCH_HANDOFF_CANDIDATE_ONLY__NO_LEDGER_MUTATION",
        "authority_binding": {
            "Q8": q8,
            "geometry_registry_sha256": INPUTS["geometry_registry"][1],
            "round176_semantics_sha256": INPUTS["round176_verifier"][1],
            "C30b_half_open_semantics_sha256": INPUTS["c30b_producer"][1],
            "all_inputs_hash_pinned_and_stable": True,
        },
        "physical_target_completeness": {
            "horizon_1": t1, "horizon_3_over_2": t32,
            "source_self": self_no_reentry(),
            "strict_obstacle_disjointness": {
                "G_G_center_distance_minus_radius_sum": "7/25",
                "W_W_center_distance_minus_radius_sum": "17/25",
                "nearest_G_W_squared_distance_minus_squared_radius_sum": "36337/160000",
                "simultaneous_first_target_tie_impossible": True,
            },
        },
        "template_inventory": {
            "irreducible_semantic_template_count": 3,
            "templates": [
                "T1_COMPLETE_PHYSICAL_FAMILY_AT_LEAST_ONE_NONFROZEN_HIT",
                "T3_OVER_2_COMPLETE_FAMILY_UNIQUE_NONFROZEN_FIRST",
                "T1_TWO_SURVIVOR_FIRST_TARGET_PLUS_HALF_OPEN_OUTGOING_PARTITION",
            ],
            "why_three_are_irreducible": (
                "the hypotheses use two different horizons and three different conclusions: "
                "existence/nonfrozen, unique-first, and mixed outgoing-chart disposition"
            ),
            "route_template_minimality": minimality,
            "historic_root_by_root_subdivision_used": False,
        },
        "bridge_rows": bridge_rows,
        "global_miss_resolution_rows": miss_rows,
        "route_resolution_rows": route_rows,
        "lower_strata_half_open_closure": {
            "r_split": "[0,c) is left-W proof; [c,1] is right-G proof; c belongs right",
            "r_endpoints": {"0": "left", "c": "right", "1": "right"},
            "t_and_s_boundaries": "no Q9 split; inherit the unique upstream origin/token owner",
            "first_target_ties": "impossible by strict pairwise obstacle disjointness",
            "outgoing_chart_partition": {
                "E": "nx>=abs(ny)", "W": "-nx>=abs(ny)",
                "N": "ny>abs(nx)", "S": "-ny>abs(nx)",
                "seam_owner_rule": "E_OR_W_OWNS__N_OR_S_SHADOWS",
            },
            "mixed_witness_subbox_boundaries": (
                "existence-only strict positive-volume half-open boxes; all inequalities are "
                "strict on their closed hulls, so endpoint reassignment cannot change class"
            ),
            "formal_atomic_3D_2D_1D_0D_rebuild_still_required": True,
        },
        "research_disposition_ledger": disposition_rows,
        "classification_closure": {
            "total_origins": 54,
            "mutually_exclusive_and_exhaustive": True,
            "research_EXCLUDED_candidates": 44,
            "research_RESOLVED_MIXED_candidates": 10,
            "strict_LIVE_subboxes_for_all_mixed": 10,
            "strict_EXCLUDED_subboxes_for_all_mixed": 10,
            "unresolved_research_origins": 0,
            "formal_EXCLUDED_minted": 0,
            "formal_RESOLVED_MIXED_minted": 0,
            "formal_dispositions_minted": 0,
        },
        "future_C30f_gated_handoff_candidate": {
            "required_predecessor": "C30f v2 exact terminal replay authorizing the 56-to-54 step",
            "predecessor_exists_in_this_audit": False,
            "before": before,
            "candidate_credit": {"EXCLUDED": 44, "RESOLVED_MIXED": 10,
                                 "total_dispositions": 54},
            "candidate_after": after,
            "conservation": {
                "before_excluded_plus_live": 76832,
                "after_excluded_plus_live": 76832,
                "partition_before": 54, "partition_after": 0,
            },
            "terminal_adapter_present": False,
            "formal_54_to_0_minted": False,
            "release_state": "PROHIBITED_PRE_TERMINAL",
        },
        "formal_boundary": {
            "formal_credit": 0,
            "ledger_unchanged": True,
            "current_formal_round": "Round306C30b",
            "source_W_formal_remaining": 80,
            "compact_q_formal_remaining_origins": 54,
            "diagnostic_research_coverage": "54/54",
            "future_C30f_handoff_is_diagnostic_only": True,
            "terminal_gate_present": False,
            "can_serve_as_compact_q_formal_predecessor": False,
            "D02": "BLOCKED_COMPOSITE",
            "D03": "UNAUTHORIZED",
            "D04": "NOT_MINTED",
            "Gate5": "10/18",
            "CM2": "NO-GO_FOR_CLAIM",
        },
    }


def main() -> int:
    try:
        result = build()
        output = {"schema": SCHEMA, "result": result, "result_sha256": digest(result)}
        sys.stdout.buffer.write(canonical(output) + b"\n")
        return 0
    except (OSError, KeyError, TypeError, ValueError, StopIteration, Reject) as error:
        sys.stderr.write("REJECT_C30Q9:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
