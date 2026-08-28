#!/usr/bin/env python3
"""Append-only, zero-credit structural audit of all 54 compact-q origins.

This audit deliberately does not mint a Source-W disposition.  It reconstructs
the frozen Q1/Q2 census, groups every origin into a disjoint analytic cohort,
and tests whole-origin interval templates without subdividing any historical
root.  Thirty-six origins obtain research exclusion theorems; eighteen remain
explicit blockers.  The formal C30b W80/Q54 boundary is unchanged.
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
SCHEMA = "cm2.round306c30q8.compact-q-54-global-template-audit.zero-credit.v1"
K = Q(1023, 262144)
RW = Q(4, 25)
RG = Q(9, 25)
R_DOMAIN = (Q(0), Q(1))

INPUTS = {
    "c30b_manifest": (
        "deliverables/cm2_round306c30b_source_w_outgoing_h_whole_origin_disposition_manifest.sha256",
        "6af636a4239f390712d057030f03e09fbbca332c6170f183d3d0095f19f0f248",
    ),
    "c30b_result": (
        "deliverables/cm2_round306c30b_sealed/cm2_round306c30b_source_w_outgoing_h_whole_origin_disposition_result.json",
        "b015e5bd6a4ee01d71ac95765d07dcbc63c3888f0c8ff9205e2d8c688958c11b",
    ),
    "c30b_verification": (
        "deliverables/cm2_round306c30b_source_w_outgoing_h_whole_origin_disposition_verification.json",
        "e9e72536be9ba707fe2fdf6034b47978be4d09235e5133414ec7b0a31acf4e71",
    ),
    "q1a": (
        ".cm2-runtime/audit/c30q1-cohort-counterexample-v3-20260807T1205/seed30630071_stdout.json",
        "037e30eb015ab5c9eb802ecda7641144c4f6fd74b6db115c75aa0c7467793574",
    ),
    "q1b": (
        ".cm2-runtime/audit/c30q1-cohort-counterexample-v3-20260807T1205/seed30630929_stdout.json",
        "037e30eb015ab5c9eb802ecda7641144c4f6fd74b6db115c75aa0c7467793574",
    ),
    "q2a": (
        ".cm2-runtime/audit/c30q2-seven-cohort-routing-v3-20260807T1325/seed30630071_stdout.json",
        "a3af728ac34b07ad86f9045c28bc3eabe88ea446e051cbe37b26d3baa270637b",
    ),
    "q2b": (
        ".cm2-runtime/audit/c30q2-seven-cohort-routing-v3-20260807T1325/seed30630929_stdout.json",
        "a3af728ac34b07ad86f9045c28bc3eabe88ea446e051cbe37b26d3baa270637b",
    ),
    "q5_manifest": (
        ".cm2-runtime/audit/c30q5-11010101-clipped-graph-zero-credit-v1-20260808T075621Z/manifest.sha256",
        "452590a90f53607647949e73177aa010c7961dfae53e37f5d6d0eb6bd2fee5e3",
    ),
    "q5_receipt": (
        ".cm2-runtime/audit/c30q5-11010101-clipped-graph-zero-credit-v1-20260808T075621Z/receipt.json",
        "cdebf9a357de0de2612f6b8493d0c56c2a703fd25423967ba771cea12224cc79",
    ),
    "q6_manifest": (
        ".cm2-runtime/audit/c30q6-six-origin-clean-room-zero-credit-v1-20260808T085007Z/manifest.sha256",
        "6df3516930ae49a655e2bcdb000db89040f3bb5040db5032afc6afb1dd0eece6",
    ),
    "q6_receipt": (
        ".cm2-runtime/audit/c30q6-six-origin-clean-room-zero-credit-v1-20260808T085007Z/receipt.json",
        "8906bd8fa15f7b73f988847c0782de1367a14928aaa991ddeda90f764b47469b",
    ),
    "q7_manifest": (
        ".cm2-runtime/audit/c30q7-11011101-two-witness-zero-credit-v1-20260808T093031Z/manifest.sha256",
        "69f4907da8a972bf127e96b434cd42e6372ba25a9254caf3f20201a561a09049",
    ),
    "q7_receipt": (
        ".cm2-runtime/audit/c30q7-11011101-two-witness-zero-credit-v1-20260808T093031Z/receipt.json",
        "1056ea89cf7151d5a20f7d4bb1661588385673d5a8ade44f48161ce1833ab174",
    ),
}


UNIFORM_W_TOKENS = (
    "03.15.01111111",
    "03.15.11010101",
    "03.15.11010111",
)
UNIFORM_G_TOKENS = (
    "03.15.11110111",
    "03.15.11111101",
    "03.15.11111111",
    "04.15.01010101",
    "05.15.01010111",
    "05.15.01111111",
    "05.15.11010101",
    "05.15.11010111",
    "05.15.11011101",
    "05.15.11011111",
    "05.15.11110101",
    "05.15.11111111",
)
PIECEWISE_SWITCH = {
    "03.15.11011101": Q(13, 16),
    "03.15.11011111": Q(1, 2),
    "03.15.11110101": Q(1, 2),
}
MIXED_ROUTE_TOKENS = (
    "04.00.00001010",
    "04.00.00100000",
    "04.00.00100010",
    "04.00.00101000",
    "04.00.00101010",
    "04.00.10000000",
)
GLOBAL_MISS_TOKENS = (
    "06.00.00101010",
    "06.00.10000000",
    "06.00.10000010",
)


class Reject(RuntimeError):
    pass


def need(condition: bool, label: str) -> None:
    if type(condition) is not bool or not condition:
        raise Reject(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


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
    fields = (
        "st_dev", "st_ino", "st_mode", "st_nlink", "st_size",
        "st_mtime_ns", "st_ctime_ns", "st_uid", "st_gid",
    )
    need(all(getattr(before, key) == getattr(after, key) for key in fields),
         "stable input:" + str(path))
    return raw


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in output, "duplicate JSON key:" + label)
            output[key] = value
        return output
    try:
        value = json.loads(
            raw.decode("utf-8", "strict"), object_pairs_hook=unique,
            parse_float=lambda token: token,
            parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)),
        )
    except (UnicodeDecodeError, ValueError, json.JSONDecodeError) as error:
        raise Reject("strict JSON:" + label) from error
    need(type(value) is dict, "JSON object:" + label)
    return value


def pinned(name: str) -> bytes:
    relative, expected = INPUTS[name]
    raw = capture(ROOT / relative)
    need(hashlib.sha256(raw).hexdigest() == expected, "input pin:" + name)
    return raw


def document(name: str) -> dict[str, Any]:
    return strict_json(pinned(name), name)


def verify_manifest(name: str) -> int:
    relative, _expected = INPUTS[name]
    manifest_path = ROOT / relative
    base = manifest_path.parent
    rows = pinned(name).decode("ascii", "strict").splitlines()
    seen: set[str] = set()
    for row in rows:
        need(len(row) >= 67 and row[64:66] == "  ", "manifest syntax:" + name)
        expected, member = row[:64], row[66:]
        part = Path(member)
        need(all(char in "0123456789abcdef" for char in expected)
             and not part.is_absolute() and ".." not in part.parts
             and member not in seen, "manifest row:" + name)
        seen.add(member)
        workspace_path = ROOT / part
        target = workspace_path if workspace_path.exists() else base / part
        need(target.absolute().is_relative_to(ROOT), "manifest scope:" + name)
        need(hashlib.sha256(capture(target)).hexdigest() == expected,
             "manifest member:" + name + ":" + member)
    need(bool(rows), "nonempty manifest:" + name)
    return len(rows)


def pair(value: Any, label: str) -> tuple[Q, Q]:
    need(type(value) is list and len(value) == 2
         and all(type(item) is str for item in value), "fraction pair:" + label)
    return Q(value[0]), Q(value[1])


def origins(tokens: tuple[str, ...] | list[str]) -> list[str]:
    return sorted(
        origin
        for token in tokens
        for origin in ("W:N:" + token, "W:S:H." + token)
    )


def authority_binding() -> dict[str, Any]:
    manifest_counts = {
        name: verify_manifest(name)
        for name in ("c30b_manifest", "q5_manifest", "q6_manifest", "q7_manifest")
    }
    c30b = document("c30b_result")
    c30b_verification = document("c30b_verification")
    need(c30b["status"] == "PASS_BOUNDED_ROUND306C30B_OUTGOING_H_DISPOSITION",
         "C30b result status")
    need(c30b_verification["status"] ==
         "PASS_FORMAL_C30B__688_H_CELLS__2_WHOLE_ORIGIN_EXCLUSIONS__10_RESOLVED_MIXED__SOURCE_W_92_TO_80__D02_STILL_BLOCKED",
         "C30b verification status")
    after = c30b["source_W_ledger_transition"]["after"]
    need(after["remaining"] == 80
         and after["remaining_partition"]["compact_q"] == 54
         and after["excluded"] + after["conservative_live"] == 76832,
         "C30b W80/Q54 conservation")
    expected_status = {
        "q5_receipt": "PASS_C30Q5_DUAL_SEED_COLD_REPLAY_AND_ATTACKS__ZERO_CREDIT",
        "q6_receipt": "PASS_C30Q6_CLEAN_ROOM_DUAL_SEED_COLD_REPLAY_AND_ATTACKS__FAIL_CLOSED_ZERO_CREDIT",
        "q7_receipt": "PASS_C30Q7_DUAL_SEED_GLOBAL_TWO_WITNESS_ATTACKS_AND_COLD_REPLAY__ZERO_FORMAL_CREDIT",
    }
    receipt_rows: list[dict[str, Any]] = []
    for name, status_value in expected_status.items():
        receipt = document(name)
        need(receipt["status"] == status_value, "historical receipt status:" + name)
        boundary = receipt.get("strict_nonpromotion") or receipt.get("formal_boundary")
        need(boundary["formal_credit"] == 0
             and boundary["ledger_unchanged"] is True
             and boundary["source_W_formal_remaining"] == 80
             and boundary["compact_q_formal_remaining_origins"] == 54
             and boundary["CM2"] == "NO-GO_FOR_CLAIM",
             "historical zero-credit boundary:" + name)
        receipt_rows.append({
            "name": name,
            "sha256": INPUTS[name][1],
            "status": status_value,
            "research_only": True,
        })
    return {
        "formal_round": "Round306C30b",
        "source_W_formal_remaining": 80,
        "compact_q_formal_remaining": 54,
        "c30b_manifest_sha256": INPUTS["c30b_manifest"][1],
        "c30b_manifest_member_count": manifest_counts["c30b_manifest"],
        "c30b_result_sha256": INPUTS["c30b_result"][1],
        "c30b_verification_sha256": INPUTS["c30b_verification"][1],
        "historical_zero_credit_receipts": receipt_rows,
        "historical_manifest_member_counts": {
            name: manifest_counts[name]
            for name in ("q5_manifest", "q6_manifest", "q7_manifest")
        },
        "no_historical_zero_credit_receipt_is_a_formal_predecessor": True,
    }


def historic_census() -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    q1a, q1b = pinned("q1a"), pinned("q1b")
    q2a, q2b = pinned("q2a"), pinned("q2b")
    need(q1a == q1b and q2a == q2b, "Q1/Q2 dual-seed byte identity")
    q1, q2 = strict_json(q1a, "Q1"), strict_json(q2a, "Q2")
    need(q1["result_sha256"] == digest(q1["result"])
         and q2["result_sha256"] == digest(q2["result"]),
         "Q1/Q2 result closure")
    need(q1["result"]["status"].startswith(
         "REJECT_AUTOMATIC_REPRESENTATIVE_CERTIFICATE_EXTENSION__"),
         "Q1 truthful rejection")
    need(q2["result"]["status"] ==
         "PASS_EXACT_SEVEN_COHORT_ROUTING_LEDGER__REJECT_AUTOMATIC_EXTENSION__ZERO_FORMAL_CREDIT",
         "Q2 routing status")

    patterns = q2["result"]["exact_seven_cohort_ledger"]["patterns"]
    pattern_for: dict[str, dict[str, Any]] = {}
    for pattern_index, pattern_row in enumerate(patterns):
        for origin in pattern_row["origin_keys"]:
            need(origin not in pattern_for, "unique Q2 origin")
            pattern_for[origin] = {
                "pattern_index": pattern_index,
                "pattern": pattern_row["pattern"],
                "root_failure_summary": pattern_row["root_failure_summary"],
            }
    roots: dict[str, list[dict[str, Any]]] = {}
    for row in q1["result"]["analytic_cohort_census"]["root_results"]:
        roots.setdefault(row["origin_key"], []).append(row)
    complements = {
        row["origin_key"]: row
        for row in q1["result"]["pinned_complement_replay"]["origin_rows"]
    }
    need(set(pattern_for) == set(roots) == set(complements)
         and len(roots) == 54, "exact 54-origin historic join")

    census: dict[str, dict[str, Any]] = {}
    for origin in sorted(roots):
        selected = sorted(roots[origin], key=lambda row: row["root_key"])
        first = selected[0]["cohort_parameters"]
        t_intervals = sorted({pair(row["cohort_parameters"]["exact_t_domain"], "t")
                              for row in selected})
        s_intervals = sorted({pair(row["cohort_parameters"]["exact_s_domain"], "s")
                              for row in selected})
        boxes = {
            (*pair(row["cohort_parameters"]["exact_t_domain"], "t"),
             *pair(row["cohort_parameters"]["exact_s_domain"], "s"))
            for row in selected
        }
        need(all(left[1] == right[0]
                 for left, right in zip(t_intervals, t_intervals[1:])),
             "contiguous t tiling:" + origin)
        need(all(left[1] == right[0]
                 for left, right in zip(s_intervals, s_intervals[1:])),
             "contiguous s tiling:" + origin)
        need(boxes == {(t0, t1, s0, s1)
                       for t0, t1 in t_intervals for s0, s1 in s_intervals},
             "Cartesian root tiling:" + origin)
        common = set(first["active_target_set"])
        applicable = 0
        frozen_behind = 0
        future = 0
        for row in selected:
            parameters = row["cohort_parameters"]
            need(parameters["source_chart"] == first["source_chart"]
                 and parameters["p_sign"] == first["p_sign"]
                 and Q(parameters["exact_q_squared_scale"]) == K
                 and pair(parameters["exact_r_domain"], "r") == R_DOMAIN,
                 "stable root parameter family:" + row["root_key"])
            common.intersection_update(parameters["active_target_set"])
            applicable += int(row["analytic_root_applicable"] is True)
            frozen_behind += int(row["frozen_target"]["strict"]["ell_negative"] is True)
            future += int(bool(row["certified_future_witness_targets"]))
        pattern = pattern_for[origin]["pattern"]
        need(len(selected) == pattern["analytic_root_count_per_origin"]
             and applicable == pattern["applicable_root_count_per_origin"]
             and frozen_behind == pattern["frozen_behind_root_count_per_origin"]
             and future == pattern["future_witness_root_count_per_origin"],
             "Q1/Q2 pattern closure:" + origin)
        complement = complements[origin]
        need(complement["Round180_final_child_count"]
             == complement["P215_exact_behind_closed_child_count"]
             + complement["P215_residual_child_count"]
             and complement["source_grazing_root_count"] == len(selected),
             "Round180=P215-closed+residual complement:" + origin)
        census[origin] = {
            "origin_key": origin,
            "source_chart": first["source_chart"],
            "p_sign": first["p_sign"],
            "p_endpoint_domain": list(first["source_p_endpoint_domain"]),
            "t_domain_q": (t_intervals[0][0], t_intervals[-1][1]),
            "s_domain_q": (s_intervals[0][0], s_intervals[-1][1]),
            "t_domain": [str(t_intervals[0][0]), str(t_intervals[-1][1])],
            "s_domain": [str(s_intervals[0][0]), str(s_intervals[-1][1])],
            "r_domain": ["0", "1"],
            "root_count": len(selected),
            "t_interval_count": len(t_intervals),
            "s_interval_count": len(s_intervals),
            "root_tiling_is_exact_Cartesian_product": True,
            "root_keys_sha256": digest([row["root_key"] for row in selected]),
            "common_active_targets": sorted(common),
            "old_pattern": pattern,
            "old_root_failure_summary": pattern_for[origin]["root_failure_summary"],
            "Round180_children": complement["Round180_final_child_count"],
            "P215_exact_behind_closed_children": (
                complement["P215_exact_behind_closed_child_count"]
            ),
            "compact_q_residual_children": complement["P215_residual_child_count"],
        }
    public_rows = []
    for origin in sorted(census):
        public_rows.append({key: value for key, value in census[origin].items()
                            if not key.endswith("_q")})
    summary = {
        "q1_dual_seed_stdout_sha256": INPUTS["q1a"][1],
        "q2_dual_seed_stdout_sha256": INPUTS["q2a"][1],
        "origin_count": 54,
        "Round180_child_count": sum(
            row["Round180_children"] for row in census.values()
        ),
        "P215_exact_behind_closed_child_count": sum(
            row["P215_exact_behind_closed_children"] for row in census.values()
        ),
        "compact_q_residual_child_count": sum(
            row["compact_q_residual_children"] for row in census.values()
        ),
        "all_origin_root_tilings_exact": True,
        "origin_rows_sha256": digest(public_rows),
        "origin_rows": public_rows,
    }
    return census, summary


def aq(value: Q) -> arb:
    return arb(value.numerator) / value.denominator


def interval(lower: Q, upper: Q) -> arb:
    need(lower <= upper, "interval order")
    middle, radius = (lower + upper) / 2, (upper - lower) / 2
    return aq(middle) + arb(0, aq(radius).upper())


def bounds(value: arb) -> dict[str, str]:
    return {
        "enclosure": str(value),
        "lower": str(value.lower()),
        "upper": str(value.upper()),
    }


def target_definition(target_id: str, s: arb) -> tuple[arb, arb, Q]:
    match = re.fullmatch(r"([GW])\[(-?\d+),(-?\d+)\]", target_id)
    need(match is not None, "target id:" + target_id)
    obstacle, ix_text, iy_text = match.groups()
    ix, iy = int(ix_text), int(iy_text)
    need(-4 <= ix <= 4 and -4 <= iy <= 4, "pinned physical target family")
    if obstacle == "G":
        return arb(ix), arb(iy), RG
    return arb(ix) + aq(Q(1, 2)) + s, arb(iy) + aq(Q(1, 2)), RW


def metric(origin: dict[str, Any], r_domain: tuple[Q, Q],
           target_id: str) -> tuple[dict[str, Any], dict[str, arb]]:
    t = interval(*origin["t_domain_q"])
    s = interval(*origin["s_domain_q"])
    a = (arb(1) - t * t).sqrt()
    nx, ny = t, a if origin["source_chart"] == "W:N" else -a
    b = aq(K).sqrt() * interval(*r_domain)
    p_absolute = (arb(1) - b * b).sqrt()
    p = p_absolute if origin["p_sign"] == 1 else -p_absolute
    ux, uy = b * nx - p * ny, b * ny + p * nx
    qx = aq(Q(1, 2)) + s + aq(RW) * nx
    qy = aq(Q(1, 2)) + aq(RW) * ny
    ax, ay, radius = target_definition(target_id, s)
    dx, dy = ax - qx, ay - qy
    ell = ux * dx + uy * dy
    transverse = -uy * dx + ux * dy
    f0 = dx * dx + dy * dy - aq(radius * radius)
    delta = aq(radius * radius) - transverse * transverse
    values = {
        "forward_projection_ell": ell,
        "signed_transverse": transverse,
        "f_at_0": f0,
        "f_at_1": f0 + arb(1) - 2 * ell,
        "discriminant": delta,
    }
    if bool(delta > 0):
        square = delta.sqrt()
        values["tau_minus"] = ell - square
        values["tau_plus"] = ell + square
    return ({
        "target": target_id,
        "closed_r_proof_domain": [str(r_domain[0]), str(r_domain[1])],
        "interval_bounds": {key: bounds(value) for key, value in values.items()},
    }, values)


def need_frozen_behind(values: dict[str, arb], label: str) -> None:
    need(bool(values["f_at_0"] > 0)
         and bool(values["forward_projection_ell"] < 0),
         "global frozen-behind:" + label)


def need_future_hit(values: dict[str, arb], label: str) -> None:
    need("tau_minus" in values
         and bool(values["f_at_0"] > 0)
         and bool(values["forward_projection_ell"] > 0)
         and bool(values["discriminant"] > 0)
         and bool(values["tau_minus"] > 0)
         and bool(values["tau_minus"] < 1),
         "global future hit:" + label)


def analytic_templates(census: dict[str, dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    theorem_rows: list[dict[str, Any]] = []
    blocker_rows: list[dict[str, Any]] = []

    for origin_key in origins(UNIFORM_W_TOKENS):
        origin = census[origin_key]
        frozen_row, frozen = metric(origin, R_DOMAIN, "W[1,0]")
        witness_row, witness = metric(origin, R_DOMAIN, "W[-1,0]")
        need_frozen_behind(frozen, origin_key)
        need_future_hit(witness, origin_key)
        need("W[-1,0]" in origin["common_active_targets"],
             "uniform W active-target membership")
        theorem_rows.append({
            "origin_key": origin_key,
            "template_id": "T1_UNIFORM_W_MINUS_1_FIRST_ENTRY",
            "proposed_disposition_after_formal_bridge": "EXCLUDED",
            "historic_root_subdivision_count_used_by_theorem": 0,
            "global_interval_box_count": 1,
            "frozen_owner": frozen_row,
            "witnesses": [{
                **witness_row,
                "assigned_half_open_r_domain": "[0,1]",
                "criterion": "f0>0, ell>0, delta>0, 0<tau_minus<1",
            }],
            "selected_witness_in_every_historic_active_target_set": True,
            "physical_target_completeness_bridge_required": False,
            "formal_disposition_minted": False,
        })

    for origin_key in origins(UNIFORM_G_TOKENS):
        origin = census[origin_key]
        target = "G[0,1]" if origin["source_chart"] == "W:N" else "G[0,0]"
        frozen_row, frozen = metric(origin, R_DOMAIN, "W[1,0]")
        witness_row, witness = metric(origin, R_DOMAIN, target)
        need_frozen_behind(frozen, origin_key)
        need_future_hit(witness, origin_key)
        need(target in origin["common_active_targets"],
             "uniform G active-target membership")
        theorem_rows.append({
            "origin_key": origin_key,
            "template_id": "T2_UNIFORM_REFLECTED_G0_FIRST_ENTRY",
            "proposed_disposition_after_formal_bridge": "EXCLUDED",
            "historic_root_subdivision_count_used_by_theorem": 0,
            "global_interval_box_count": 1,
            "frozen_owner": frozen_row,
            "witnesses": [{
                **witness_row,
                "assigned_half_open_r_domain": "[0,1]",
                "criterion": "f0>0, ell>0, delta>0, 0<tau_minus<1",
                "f_at_1_negative_is_not_required": True,
            }],
            "selected_witness_in_every_historic_active_target_set": True,
            "physical_target_completeness_bridge_required": False,
            "formal_disposition_minted": False,
        })

    for token, switch in sorted(PIECEWISE_SWITCH.items()):
        for origin_key in origins([token]):
            origin = census[origin_key]
            right_target = (
                "G[0,1]" if origin["source_chart"] == "W:N" else "G[0,0]"
            )
            frozen_row, frozen = metric(origin, R_DOMAIN, "W[1,0]")
            left_row, left = metric(origin, (Q(0), switch), "W[-1,0]")
            right_row, right = metric(origin, (switch, Q(1)), right_target)
            seam_left_row, seam_left = metric(origin, (switch, switch), "W[-1,0]")
            seam_right_row, seam_right = metric(origin, (switch, switch), right_target)
            need_frozen_behind(frozen, origin_key)
            for label, values in (
                ("left", left), ("right", right),
                ("seam-left", seam_left), ("seam-right", seam_right),
            ):
                need_future_hit(values, origin_key + ":" + label)
            bridge = "W[-1,0]" not in origin["common_active_targets"]
            need(bridge == (token == "03.15.11110101"),
                 "exact physical-target bridge cohort")
            theorem_rows.append({
                "origin_key": origin_key,
                "template_id": "T3_PIECEWISE_W_MINUS_1_TO_REFLECTED_G0_FIRST_ENTRY",
                "proposed_disposition_after_formal_bridge": "EXCLUDED",
                "historic_root_subdivision_count_used_by_theorem": 0,
                "global_interval_box_count": 2,
                "switch": str(switch),
                "frozen_owner": frozen_row,
                "witnesses": [
                    {
                        **left_row,
                        "assigned_half_open_r_domain": "[0," + str(switch) + ")",
                        "criterion": "f0>0, ell>0, delta>0, 0<tau_minus<1",
                    },
                    {
                        **right_row,
                        "assigned_half_open_r_domain": "[" + str(switch) + ",1]",
                        "criterion": "f0>0, ell>0, delta>0, 0<tau_minus<1",
                        "f_at_1_negative_is_not_required": True,
                    },
                ],
                "switch_seam": {
                    "r": str(switch),
                    "assignment_owner": "right_witness",
                    "left_closed_proof_strict": True,
                    "right_closed_proof_strict": True,
                    "assigned_domains_have_gap": False,
                    "assigned_domains_have_overlap": False,
                    "left": seam_left_row,
                    "right": seam_right_row,
                },
                "selected_witness_in_every_historic_active_target_set": not bridge,
                "physical_target_completeness_bridge_required": bridge,
                "bridge_reason": (
                    "W[-1,0] is a valid pinned physical lift and is globally hit, "
                    "but is absent from the intersection of the old residual active-target sets"
                    if bridge else "none"
                ),
                "formal_disposition_minted": False,
            })

    for origin_key in origins(MIXED_ROUTE_TOKENS):
        origin = census[origin_key]
        t0, t1 = origin["t_domain_q"]
        witness_t = (t0 + t1) / 2
        point_origin = dict(origin)
        point_origin["t_domain_q"] = (witness_t, witness_t)
        point_origin["s_domain_q"] = (Q(0), Q(0))
        frozen_row, frozen = metric(point_origin, (Q(1, 2), Q(1, 2)), "W[1,0]")
        need_future_hit(frozen, "strict interior frozen hit:" + origin_key)
        need(t0 < witness_t < t1
             and origin["s_domain_q"][0] < 0 < origin["s_domain_q"][1],
             "strict interior point:" + origin_key)
        q2 = K * Q(1, 4)
        a2 = Q(1) - witness_t * witness_t
        square_gap = (Q(1) - q2) * a2 - q2 * (RW - witness_t) ** 2
        need(square_gap > 0, "exact positive projection square gap:" + origin_key)
        blocker_rows.append({
            "origin_key": origin_key,
            "blocker_class": "B1_STRICT_INTERIOR_FROZEN_HIT",
            "whole_origin_EXCLUDED_falsified": True,
            "proposed_route": "RESOLVED_MIXED",
            "RESOLVED_MIXED_exhaustive_partition_proved": False,
            "exact_interior_parameters": {
                "t": str(witness_t), "s": "0", "r": "1/2",
                "q_squared": str(q2), "a_squared": str(a2),
                "positive_projection_square_gap": str(square_gap),
                "square_gap_strict_positive": True,
            },
            "strict_frozen_hit": frozen_row,
            "missing_theorem": (
                "one whole-origin analytic partition proving exhaustive excluded/live "
                "coverage and an authorized RESOLVED_MIXED disposition"
            ),
            "formal_disposition_minted": False,
        })

    for origin_key in origins(GLOBAL_MISS_TOKENS):
        origin = census[origin_key]
        frozen_row, frozen = metric(origin, R_DOMAIN, "W[1,0]")
        need(bool(frozen["f_at_0"] > 0)
             and bool(frozen["forward_projection_ell"] > 0)
             and bool(frozen["discriminant"] < 0)
             and "tau_minus" not in frozen,
             "global frozen miss:" + origin_key)
        blocker_rows.append({
            "origin_key": origin_key,
            "blocker_class": "B2_GLOBAL_FROZEN_DISCRIMINANT_NEGATIVE",
            "whole_origin_EXCLUDED_falsified": False,
            "proposed_route": "UNDECIDED_OUTGOING_OR_MIXED",
            "global_frozen_miss": frozen_row,
            "missing_theorem": (
                "authorized whole-origin no-hit/outgoing disposition semantics or a "
                "different global physical-target cover"
            ),
            "formal_disposition_minted": False,
        })

    theorem_rows.sort(key=lambda row: row["origin_key"])
    blocker_rows.sort(key=lambda row: row["origin_key"])
    need(len(theorem_rows) == 36 and len(blocker_rows) == 18,
         "36 theorem candidates plus 18 blockers")
    need({row["origin_key"] for row in theorem_rows}.isdisjoint(
         {row["origin_key"] for row in blocker_rows}), "disjoint theorem/blocker rows")
    need({row["origin_key"] for row in theorem_rows + blocker_rows} == set(census),
         "full 54-origin classification")
    return theorem_rows, blocker_rows


def build() -> dict[str, Any]:
    ctx.prec = 256
    authority = authority_binding()
    census, historic = historic_census()
    theorem_rows, blocker_rows = analytic_templates(census)
    cohort_ledger = [
        {
            "cohort_id": "C1_UNIFORM_W",
            "origin_count": 6,
            "origin_keys": origins(UNIFORM_W_TOKENS),
            "research_result": "WHOLE_ORIGIN_EXCLUSION_THEOREM_CANDIDATE",
            "proposed_formal_disposition": "EXCLUDED",
        },
        {
            "cohort_id": "C2_UNIFORM_REFLECTED_G0",
            "origin_count": 24,
            "origin_keys": origins(UNIFORM_G_TOKENS),
            "research_result": "WHOLE_ORIGIN_EXCLUSION_THEOREM_CANDIDATE",
            "proposed_formal_disposition": "EXCLUDED",
        },
        {
            "cohort_id": "C3_PIECEWISE_W_TO_G",
            "origin_count": 6,
            "origin_keys": origins(list(PIECEWISE_SWITCH)),
            "research_result": "WHOLE_ORIGIN_EXCLUSION_THEOREM_CANDIDATE",
            "proposed_formal_disposition": "EXCLUDED_AFTER_TWO_ORIGIN_PHYSICAL_TARGET_BRIDGE",
        },
        {
            "cohort_id": "C4_FROZEN_INTERIOR_HIT",
            "origin_count": 12,
            "origin_keys": origins(MIXED_ROUTE_TOKENS),
            "research_result": "WHOLE_EXCLUSION_FALSIFIED__MIXED_ROUTE_NOT_EXHAUSTIVE",
            "proposed_formal_disposition": "RESOLVED_MIXED_AFTER_NEW_GLOBAL_PARTITION",
        },
        {
            "cohort_id": "C5_GLOBAL_FROZEN_MISS",
            "origin_count": 6,
            "origin_keys": origins(GLOBAL_MISS_TOKENS),
            "research_result": "NO_AUTHORIZED_DISPOSITION_SEMANTICS",
            "proposed_formal_disposition": "UNDECIDED",
        },
    ]
    need(sum(row["origin_count"] for row in cohort_ledger) == 54
         and len({origin for row in cohort_ledger for origin in row["origin_keys"]}) == 54,
         "cohort ledger full disjoint cover")
    return {
        "status": (
            "PASS_FULL_54_ORIGIN_DISJOINT_GLOBAL_TEMPLATE_AUDIT__"
            "36_RESEARCH_EXCLUSION_CANDIDATES__18_EXPLICIT_BLOCKERS__ZERO_CREDIT"
        ),
        "verdict": "RESEARCH_PROGRESS_ONLY__FORMAL_COMPACT_Q_REMAINS_54",
        "authority_binding": authority,
        "historic_full_census": historic,
        "exact_global_coordinate_model": {
            "source": (
                "W source center=(1/2+s,1/2)+(4/25)n; "
                "n=(t,+sqrt(1-t^2)) North and (t,-sqrt(1-t^2)) South"
            ),
            "velocity": (
                "v=b*n+p*n_perp; b=sqrt(1023/262144)*r; "
                "p=branch_sign*sqrt(1-b^2)"
            ),
            "target_centers": {
                "G[i,j]": "(i,j), radius 9/25",
                "W[i,j]": "(i+1/2+s,j+1/2), radius 4/25",
            },
            "first_entry_invariants": {
                "ell": "v dot (target_center-source_point)",
                "transverse": "det(v,target_center-source_point)",
                "f0": "distance_squared-radius_squared",
                "delta": "radius_squared-transverse_squared",
                "tau_minus": "ell-sqrt(delta)",
                "strict_hit_before_one": "f0>0 and ell>0 and delta>0 and 0<tau_minus<1",
            },
            "reflection": "North/G[0,1],p=+ mirrors South/G[0,0],p=-",
            "all_input_domains_are_exact_rationals": True,
            "directed_interval_precision_bits": 256,
        },
        "minimal_template_inventory": {
            "theorem_template_count": 3,
            "templates": [
                "T1_UNIFORM_W_MINUS_1_FIRST_ENTRY",
                "T2_UNIFORM_REFLECTED_G0_FIRST_ENTRY",
                "T3_PIECEWISE_W_MINUS_1_TO_REFLECTED_G0_FIRST_ENTRY",
            ],
            "historic_root_by_root_subdivision_used": False,
            "piecewise_domains_are_half_open_and_seam_owned_by_right": True,
        },
        "full_disjoint_cohort_ledger": cohort_ledger,
        "whole_origin_theorem_candidates": theorem_rows,
        "explicit_blockers": blocker_rows,
        "classification_closure": {
            "total_origins": 54,
            "research_EXCLUDED_candidates": 36,
            "active_set_native_EXCLUDED_candidates": 34,
            "physical_target_bridge_EXCLUDED_candidates": 2,
            "RESOLVED_MIXED_route_candidates_not_exhaustively_proved": 12,
            "undecided_global_miss_origins": 6,
            "formal_EXCLUDED_minted": 0,
            "formal_RESOLVED_MIXED_minted": 0,
            "formal_dispositions_minted": 0,
        },
        "proof_boundary": {
            "exact_symbolic_content": (
                "exact rational domains, algebraic coordinate identities, exact half-open "
                "endpoint ownership, and exact rational strict-interior square gaps"
            ),
            "inequality_engine": "256-bit directed Arb interval enclosures",
            "independent_per_origin_polynomial_or_SOS_certificate_present": False,
            "why_zero_credit": (
                "research interval theorems are not a C30f-terminal-bound formal authority; "
                "two origins also need a physical-target-completeness bridge and eighteen "
                "origins still lack exhaustive disposition theorems"
            ),
        },
        "future_C30f_terminal_adapter_contract": {
            "adapter_exists_now": False,
            "required_predecessor": "C30f v2 exact terminal replay authorizing Source-W 56->54",
            "required_captures": [
                "terminal receipt and exact PASS.lock",
                "chain status, terminal replay and outer verification",
                "root and payload manifests plus every payload member",
                "pre/post SHA256 and nine-field stat for all authority inputs",
            ],
            "required_release_order": [
                "C30f terminal exact validation",
                "fresh dual-real-seed compact-q producer",
                "no-import independent verifier",
                "candidate and release-only coherent attacks",
                "cold and TOCTOU replay",
                "payload/root manifests and outer verifier",
                "terminal seal and independent terminal byte replay",
            ],
            "may_not_consume_Q5_Q6_Q7_as_formal_predecessors": True,
            "formal_54_to_0_authorized": False,
        },
        "formal_boundary": {
            "formal_credit": 0,
            "ledger_unchanged": True,
            "source_W_formal_remaining": 80,
            "compact_q_formal_remaining_origins": 54,
            "diagnostic_research_coverage_only": "36/54",
            "diagnostic_54_to_18_authorized": False,
            "formal_54_to_0_authorized": False,
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
        sys.stderr.write("REJECT_C30Q8:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
