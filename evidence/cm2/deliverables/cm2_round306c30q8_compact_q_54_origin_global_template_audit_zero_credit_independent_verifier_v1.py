#!/usr/bin/env python3
"""No-import verifier for the append-only C30q8 54-origin audit."""

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
PRODUCER = (
    HERE
    / "cm2_round306c30q8_compact_q_54_origin_global_template_audit_zero_credit_gate_v1.py"
)
PRODUCER_SHA256 = "d82e72b4063147810fbb2dbce9d8589c39dbf213ad8327e72613ef5f501dfdcb"
EXPECTED_RESULT_SHA256 = "e04b1f73a898b8408062f5feee2618dc51171dc59c14bce15c38ccd1cbb0aab5"
SCHEMA = "cm2.round306c30q8.compact-q-54-global-template-audit.zero-credit.v1"
K, RW, RG = Q(1023, 262144), Q(4, 25), Q(9, 25)

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
    "03.15.01111111", "03.15.11010101", "03.15.11010111",
)
UNIFORM_G_TOKENS = (
    "03.15.11110111", "03.15.11111101", "03.15.11111111",
    "04.15.01010101", "05.15.01010111", "05.15.01111111",
    "05.15.11010101", "05.15.11010111", "05.15.11011101",
    "05.15.11011111", "05.15.11110101", "05.15.11111111",
)
PIECEWISE_SWITCH = {
    "03.15.11011101": Q(13, 16),
    "03.15.11011111": Q(1, 2),
    "03.15.11110101": Q(1, 2),
}
MIXED_ROUTE_TOKENS = (
    "04.00.00001010", "04.00.00100000", "04.00.00100010",
    "04.00.00101000", "04.00.00101010", "04.00.10000000",
)
GLOBAL_MISS_TOKENS = (
    "06.00.00101010", "06.00.10000000", "06.00.10000010",
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
    need(absolute.resolve(strict=True) == absolute, "canonical file:" + str(path))
    before = os.lstat(absolute)
    need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
         "regular single-link file:" + str(path))
    raw = absolute.read_bytes()
    after = os.lstat(absolute)
    fields = (
        "st_dev", "st_ino", "st_mode", "st_nlink", "st_size",
        "st_mtime_ns", "st_ctime_ns", "st_uid", "st_gid",
    )
    need(all(getattr(before, key) == getattr(after, key) for key in fields),
         "stable file:" + str(path))
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


def doc(name: str) -> dict[str, Any]:
    return strict_json(pinned(name), name)


def verify_manifest(name: str) -> int:
    relative, _expected = INPUTS[name]
    base = (ROOT / relative).parent
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
        workspace = ROOT / part
        target = workspace if workspace.exists() else base / part
        need(hashlib.sha256(capture(target)).hexdigest() == expected,
             "manifest member:" + name + ":" + member)
    need(bool(rows), "nonempty manifest:" + name)
    return len(rows)


def pair(value: Any) -> tuple[Q, Q]:
    need(type(value) is list and len(value) == 2
         and all(type(item) is str for item in value), "fraction pair")
    return Q(value[0]), Q(value[1])


def origins(tokens: tuple[str, ...] | list[str]) -> list[str]:
    return sorted(origin for token in tokens
                  for origin in ("W:N:" + token, "W:S:H." + token))


def independent_authority(candidate: dict[str, Any]) -> dict[str, Any]:
    counts = {name: verify_manifest(name)
              for name in ("c30b_manifest", "q5_manifest", "q6_manifest", "q7_manifest")}
    c30b, verification = doc("c30b_result"), doc("c30b_verification")
    need(c30b["status"] == "PASS_BOUNDED_ROUND306C30B_OUTGOING_H_DISPOSITION"
         and verification["status"].endswith("SOURCE_W_92_TO_80__D02_STILL_BLOCKED"),
         "C30b statuses")
    after = c30b["source_W_ledger_transition"]["after"]
    need(after["remaining"] == 80
         and after["remaining_partition"]["compact_q"] == 54
         and after["excluded"] + after["conservative_live"] == 76832,
         "C30b W80/Q54")
    receipt_statuses = {
        "q5_receipt": "PASS_C30Q5_DUAL_SEED_COLD_REPLAY_AND_ATTACKS__ZERO_CREDIT",
        "q6_receipt": "PASS_C30Q6_CLEAN_ROOM_DUAL_SEED_COLD_REPLAY_AND_ATTACKS__FAIL_CLOSED_ZERO_CREDIT",
        "q7_receipt": "PASS_C30Q7_DUAL_SEED_GLOBAL_TWO_WITNESS_ATTACKS_AND_COLD_REPLAY__ZERO_FORMAL_CREDIT",
    }
    for name, expected in receipt_statuses.items():
        receipt = doc(name)
        boundary = receipt.get("strict_nonpromotion") or receipt.get("formal_boundary")
        need(receipt["status"] == expected and boundary["formal_credit"] == 0
             and boundary["source_W_formal_remaining"] == 80
             and boundary["compact_q_formal_remaining_origins"] == 54
             and boundary["ledger_unchanged"] is True
             and boundary["CM2"] == "NO-GO_FOR_CLAIM",
             "zero-credit receipt:" + name)
    authority = candidate["result"]["authority_binding"]
    need(authority["c30b_manifest_member_count"] == counts["c30b_manifest"]
         and authority["historical_manifest_member_counts"] == {
             name: counts[name] for name in ("q5_manifest", "q6_manifest", "q7_manifest")
         }
         and authority["source_W_formal_remaining"] == 80
         and authority["compact_q_formal_remaining"] == 54
         and authority["no_historical_zero_credit_receipt_is_a_formal_predecessor"] is True,
         "candidate authority binding")
    return {"manifest_member_counts": counts, "receipt_count": 3}


def independent_census(candidate: dict[str, Any]) -> dict[str, dict[str, Any]]:
    q1a, q1b, q2a, q2b = pinned("q1a"), pinned("q1b"), pinned("q2a"), pinned("q2b")
    need(q1a == q1b and q2a == q2b, "Q1/Q2 dual seed")
    q1, q2 = strict_json(q1a, "Q1"), strict_json(q2a, "Q2")
    need(q1["result_sha256"] == digest(q1["result"])
         and q2["result_sha256"] == digest(q2["result"]), "Q1/Q2 closure")
    pattern_for: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(q2["result"]["exact_seven_cohort_ledger"]["patterns"]):
        for origin in row["origin_keys"]:
            need(origin not in pattern_for, "unique Q2 origin")
            pattern_for[origin] = {
                "pattern_index": index, "pattern": row["pattern"],
                "root_failure_summary": row["root_failure_summary"],
            }
    roots: dict[str, list[dict[str, Any]]] = {}
    for row in q1["result"]["analytic_cohort_census"]["root_results"]:
        roots.setdefault(row["origin_key"], []).append(row)
    complements = {row["origin_key"]: row
                   for row in q1["result"]["pinned_complement_replay"]["origin_rows"]}
    need(set(pattern_for) == set(roots) == set(complements) and len(roots) == 54,
         "independent exact 54 join")
    census: dict[str, dict[str, Any]] = {}
    public_rows: list[dict[str, Any]] = []
    for origin in sorted(roots):
        selected = sorted(roots[origin], key=lambda row: row["root_key"])
        first = selected[0]["cohort_parameters"]
        ts = sorted({pair(row["cohort_parameters"]["exact_t_domain"])
                     for row in selected})
        ss = sorted({pair(row["cohort_parameters"]["exact_s_domain"])
                     for row in selected})
        boxes = {(*pair(row["cohort_parameters"]["exact_t_domain"]),
                  *pair(row["cohort_parameters"]["exact_s_domain"]))
                 for row in selected}
        need(all(a[1] == b[0] for a, b in zip(ts, ts[1:]))
             and all(a[1] == b[0] for a, b in zip(ss, ss[1:]))
             and boxes == {(t0, t1, s0, s1) for t0, t1 in ts for s0, s1 in ss},
             "independent exact tiling:" + origin)
        common = set(first["active_target_set"])
        applicable = frozen_behind = future = 0
        for row in selected:
            parameters = row["cohort_parameters"]
            need(parameters["source_chart"] == first["source_chart"]
                 and parameters["p_sign"] == first["p_sign"]
                 and Q(parameters["exact_q_squared_scale"]) == K
                 and pair(parameters["exact_r_domain"]) == (Q(0), Q(1)),
                 "independent root family:" + row["root_key"])
            common.intersection_update(parameters["active_target_set"])
            applicable += int(row["analytic_root_applicable"] is True)
            frozen_behind += int(row["frozen_target"]["strict"]["ell_negative"] is True)
            future += int(bool(row["certified_future_witness_targets"]))
        pattern = pattern_for[origin]["pattern"]
        need(len(selected) == pattern["analytic_root_count_per_origin"]
             and applicable == pattern["applicable_root_count_per_origin"]
             and frozen_behind == pattern["frozen_behind_root_count_per_origin"]
             and future == pattern["future_witness_root_count_per_origin"],
             "independent pattern:" + origin)
        complement = complements[origin]
        need(complement["Round180_final_child_count"]
             == complement["P215_exact_behind_closed_child_count"]
             + complement["P215_residual_child_count"]
             and complement["source_grazing_root_count"] == len(selected),
             "independent complement:" + origin)
        internal = {
            "origin_key": origin, "source_chart": first["source_chart"],
            "p_sign": first["p_sign"],
            "p_endpoint_domain": list(first["source_p_endpoint_domain"]),
            "t_domain_q": (ts[0][0], ts[-1][1]),
            "s_domain_q": (ss[0][0], ss[-1][1]),
            "t_domain": [str(ts[0][0]), str(ts[-1][1])],
            "s_domain": [str(ss[0][0]), str(ss[-1][1])],
            "r_domain": ["0", "1"], "root_count": len(selected),
            "t_interval_count": len(ts), "s_interval_count": len(ss),
            "root_tiling_is_exact_Cartesian_product": True,
            "root_keys_sha256": digest([row["root_key"] for row in selected]),
            "common_active_targets": sorted(common), "old_pattern": pattern,
            "old_root_failure_summary": pattern_for[origin]["root_failure_summary"],
            "Round180_children": complement["Round180_final_child_count"],
            "P215_exact_behind_closed_children": complement["P215_exact_behind_closed_child_count"],
            "compact_q_residual_children": complement["P215_residual_child_count"],
        }
        census[origin] = internal
        public_rows.append({key: value for key, value in internal.items()
                            if not key.endswith("_q")})
    historic = candidate["result"]["historic_full_census"]
    need(historic["origin_count"] == 54
         and historic["origin_rows"] == public_rows
         and historic["origin_rows_sha256"] == digest(public_rows)
         and historic["Round180_child_count"]
             == sum(row["Round180_children"] for row in census.values())
         and historic["P215_exact_behind_closed_child_count"]
             == sum(row["P215_exact_behind_closed_children"] for row in census.values())
         and historic["compact_q_residual_child_count"]
             == sum(row["compact_q_residual_children"] for row in census.values()),
         "candidate full historic census")
    return census


def aq(value: Q) -> arb:
    return arb(value.numerator) / value.denominator


def interval(lower: Q, upper: Q) -> arb:
    middle, radius = (lower + upper) / 2, (upper - lower) / 2
    return aq(middle) + arb(0, aq(radius).upper())


def bounds(value: arb) -> dict[str, str]:
    return {"enclosure": str(value), "lower": str(value.lower()),
            "upper": str(value.upper())}


def target(target_id: str, s: arb) -> tuple[arb, arb, Q]:
    match = re.fullmatch(r"([GW])\[(-?\d+),(-?\d+)\]", target_id)
    need(match is not None, "target id")
    obstacle, x_text, y_text = match.groups()
    x, y = int(x_text), int(y_text)
    need(-4 <= x <= 4 and -4 <= y <= 4, "target range")
    if obstacle == "G":
        return arb(x), arb(y), RG
    return arb(x) + aq(Q(1, 2)) + s, arb(y) + aq(Q(1, 2)), RW


def metric(origin: dict[str, Any], r_domain: tuple[Q, Q],
           target_id: str) -> tuple[dict[str, Any], dict[str, arb]]:
    t_value = interval(*origin["t_domain_q"])
    s_value = interval(*origin["s_domain_q"])
    normal_y = (arb(1) - t_value * t_value).sqrt()
    if origin["source_chart"] == "W:S":
        normal_y = -normal_y
    b = aq(K).sqrt() * interval(*r_domain)
    p_abs = (arb(1) - b * b).sqrt()
    p = p_abs if origin["p_sign"] == 1 else -p_abs
    ux = b * t_value - p * normal_y
    uy = b * normal_y + p * t_value
    qx = aq(Q(1, 2)) + s_value + aq(RW) * t_value
    qy = aq(Q(1, 2)) + aq(RW) * normal_y
    ax, ay, radius = target(target_id, s_value)
    dx, dy = ax - qx, ay - qy
    ell = ux * dx + uy * dy
    transverse = -uy * dx + ux * dy
    f0 = dx * dx + dy * dy - aq(radius * radius)
    delta = aq(radius * radius) - transverse * transverse
    values = {
        "forward_projection_ell": ell, "signed_transverse": transverse,
        "f_at_0": f0, "f_at_1": f0 + 1 - 2 * ell,
        "discriminant": delta,
    }
    if bool(delta > 0):
        square = delta.sqrt()
        values["tau_minus"], values["tau_plus"] = ell - square, ell + square
    row = {
        "target": target_id,
        "closed_r_proof_domain": [str(r_domain[0]), str(r_domain[1])],
        "interval_bounds": {key: bounds(value) for key, value in values.items()},
    }
    return row, values


def assert_behind(values: dict[str, arb], label: str) -> None:
    need(bool(values["f_at_0"] > 0)
         and bool(values["forward_projection_ell"] < 0), "behind:" + label)


def assert_hit(values: dict[str, arb], label: str) -> None:
    need("tau_minus" in values and bool(values["f_at_0"] > 0)
         and bool(values["forward_projection_ell"] > 0)
         and bool(values["discriminant"] > 0)
         and bool(values["tau_minus"] > 0) and bool(values["tau_minus"] < 1),
         "hit:" + label)


def independent_analytic(candidate: dict[str, Any],
                         census: dict[str, dict[str, Any]]) -> dict[str, Any]:
    rows = {row["origin_key"]: row
            for row in candidate["result"]["whole_origin_theorem_candidates"]}
    blockers = {row["origin_key"]: row
                for row in candidate["result"]["explicit_blockers"]}
    expected_theorems = set(origins(UNIFORM_W_TOKENS + UNIFORM_G_TOKENS))
    expected_theorems.update(origins(list(PIECEWISE_SWITCH)))
    expected_blockers = set(origins(MIXED_ROUTE_TOKENS + GLOBAL_MISS_TOKENS))
    need(set(rows) == expected_theorems and len(rows) == 36
         and set(blockers) == expected_blockers and len(blockers) == 18
         and expected_theorems.isdisjoint(expected_blockers)
         and expected_theorems | expected_blockers == set(census),
         "exact theorem/blocker partition")

    checked_boxes = 0
    for origin_key in origins(UNIFORM_W_TOKENS):
        origin, row = census[origin_key], rows[origin_key]
        frozen_row, frozen = metric(origin, (Q(0), Q(1)), "W[1,0]")
        witness_row, witness = metric(origin, (Q(0), Q(1)), "W[-1,0]")
        assert_behind(frozen, origin_key)
        assert_hit(witness, origin_key)
        expected_witness = {**witness_row, "assigned_half_open_r_domain": "[0,1]",
                            "criterion": "f0>0, ell>0, delta>0, 0<tau_minus<1"}
        need(row["template_id"] == "T1_UNIFORM_W_MINUS_1_FIRST_ENTRY"
             and row["frozen_owner"] == frozen_row
             and row["witnesses"] == [expected_witness]
             and row["selected_witness_in_every_historic_active_target_set"] is True
             and row["physical_target_completeness_bridge_required"] is False,
             "T1 row:" + origin_key)
        checked_boxes += 1

    for origin_key in origins(UNIFORM_G_TOKENS):
        origin, row = census[origin_key], rows[origin_key]
        target_id = "G[0,1]" if origin["source_chart"] == "W:N" else "G[0,0]"
        frozen_row, frozen = metric(origin, (Q(0), Q(1)), "W[1,0]")
        witness_row, witness = metric(origin, (Q(0), Q(1)), target_id)
        assert_behind(frozen, origin_key)
        assert_hit(witness, origin_key)
        expected_witness = {
            **witness_row, "assigned_half_open_r_domain": "[0,1]",
            "criterion": "f0>0, ell>0, delta>0, 0<tau_minus<1",
            "f_at_1_negative_is_not_required": True,
        }
        need(row["template_id"] == "T2_UNIFORM_REFLECTED_G0_FIRST_ENTRY"
             and row["frozen_owner"] == frozen_row
             and row["witnesses"] == [expected_witness]
             and row["selected_witness_in_every_historic_active_target_set"] is True
             and row["physical_target_completeness_bridge_required"] is False,
             "T2 row:" + origin_key)
        checked_boxes += 1

    physical_bridge_count = 0
    for token, switch in sorted(PIECEWISE_SWITCH.items()):
        for origin_key in origins([token]):
            origin, row = census[origin_key], rows[origin_key]
            right_target = "G[0,1]" if origin["source_chart"] == "W:N" else "G[0,0]"
            frozen_row, frozen = metric(origin, (Q(0), Q(1)), "W[1,0]")
            left_row, left = metric(origin, (Q(0), switch), "W[-1,0]")
            right_row, right = metric(origin, (switch, Q(1)), right_target)
            seam_left_row, seam_left = metric(origin, (switch, switch), "W[-1,0]")
            seam_right_row, seam_right = metric(origin, (switch, switch), right_target)
            assert_behind(frozen, origin_key)
            for label, values in (("left", left), ("right", right),
                                  ("seam-left", seam_left), ("seam-right", seam_right)):
                assert_hit(values, origin_key + label)
            bridge = token == "03.15.11110101"
            physical_bridge_count += int(bridge)
            expected_witnesses = [
                {**left_row, "assigned_half_open_r_domain": "[0," + str(switch) + ")",
                 "criterion": "f0>0, ell>0, delta>0, 0<tau_minus<1"},
                {**right_row, "assigned_half_open_r_domain": "[" + str(switch) + ",1]",
                 "criterion": "f0>0, ell>0, delta>0, 0<tau_minus<1",
                 "f_at_1_negative_is_not_required": True},
            ]
            seam = row["switch_seam"]
            need(row["template_id"] ==
                 "T3_PIECEWISE_W_MINUS_1_TO_REFLECTED_G0_FIRST_ENTRY"
                 and row["switch"] == str(switch)
                 and row["frozen_owner"] == frozen_row
                 and row["witnesses"] == expected_witnesses
                 and row["physical_target_completeness_bridge_required"] is bridge
                 and row["selected_witness_in_every_historic_active_target_set"] is not bridge
                 and seam["r"] == str(switch)
                 and seam["assignment_owner"] == "right_witness"
                 and seam["left_closed_proof_strict"] is True
                 and seam["right_closed_proof_strict"] is True
                 and seam["assigned_domains_have_gap"] is False
                 and seam["assigned_domains_have_overlap"] is False
                 and seam["left"] == seam_left_row and seam["right"] == seam_right_row,
                 "T3 row and seam:" + origin_key)
            checked_boxes += 2

    for origin_key in origins(MIXED_ROUTE_TOKENS):
        origin, row = census[origin_key], blockers[origin_key]
        t0, t1 = origin["t_domain_q"]
        middle = (t0 + t1) / 2
        point = dict(origin)
        point["t_domain_q"] = (middle, middle)
        point["s_domain_q"] = (Q(0), Q(0))
        frozen_row, frozen = metric(point, (Q(1, 2), Q(1, 2)), "W[1,0]")
        assert_hit(frozen, origin_key)
        q2_value = K / 4
        a2 = 1 - middle * middle
        gap = (1 - q2_value) * a2 - q2_value * (RW - middle) ** 2
        need(gap > 0 and row["blocker_class"] == "B1_STRICT_INTERIOR_FROZEN_HIT"
             and row["whole_origin_EXCLUDED_falsified"] is True
             and row["proposed_route"] == "RESOLVED_MIXED"
             and row["RESOLVED_MIXED_exhaustive_partition_proved"] is False
             and row["strict_frozen_hit"] == frozen_row
             and row["exact_interior_parameters"]["t"] == str(middle)
             and row["exact_interior_parameters"]["positive_projection_square_gap"] == str(gap),
             "B1 row:" + origin_key)

    for origin_key in origins(GLOBAL_MISS_TOKENS):
        origin, row = census[origin_key], blockers[origin_key]
        frozen_row, frozen = metric(origin, (Q(0), Q(1)), "W[1,0]")
        need(bool(frozen["f_at_0"] > 0)
             and bool(frozen["forward_projection_ell"] > 0)
             and bool(frozen["discriminant"] < 0)
             and "tau_minus" not in frozen
             and row["blocker_class"] == "B2_GLOBAL_FROZEN_DISCRIMINANT_NEGATIVE"
             and row["global_frozen_miss"] == frozen_row
             and row["proposed_route"] == "UNDECIDED_OUTGOING_OR_MIXED",
             "B2 row:" + origin_key)
    return {
        "whole_origin_interval_boxes_recomputed": checked_boxes,
        "research_exclusion_candidates": len(rows),
        "physical_target_bridge_origins": physical_bridge_count,
        "strict_interior_frozen_hit_blockers": 12,
        "global_frozen_miss_blockers": 6,
    }


def static_boundary(candidate: dict[str, Any]) -> None:
    result = candidate["result"]
    need(result["status"] ==
         "PASS_FULL_54_ORIGIN_DISJOINT_GLOBAL_TEMPLATE_AUDIT__36_RESEARCH_EXCLUSION_CANDIDATES__18_EXPLICIT_BLOCKERS__ZERO_CREDIT",
         "status")
    ledger = result["full_disjoint_cohort_ledger"]
    need([row["origin_count"] for row in ledger] == [6, 24, 6, 12, 6]
         and sum(row["origin_count"] for row in ledger) == 54
         and len({origin for row in ledger for origin in row["origin_keys"]}) == 54,
         "cohort ledger")
    need(result["classification_closure"] == {
        "RESOLVED_MIXED_route_candidates_not_exhaustively_proved": 12,
        "active_set_native_EXCLUDED_candidates": 34,
        "formal_EXCLUDED_minted": 0, "formal_RESOLVED_MIXED_minted": 0,
        "formal_dispositions_minted": 0,
        "physical_target_bridge_EXCLUDED_candidates": 2,
        "research_EXCLUDED_candidates": 36, "total_origins": 54,
        "undecided_global_miss_origins": 6,
    }, "classification closure")
    need(result["minimal_template_inventory"] == {
        "historic_root_by_root_subdivision_used": False,
        "piecewise_domains_are_half_open_and_seam_owned_by_right": True,
        "templates": ["T1_UNIFORM_W_MINUS_1_FIRST_ENTRY",
                      "T2_UNIFORM_REFLECTED_G0_FIRST_ENTRY",
                      "T3_PIECEWISE_W_MINUS_1_TO_REFLECTED_G0_FIRST_ENTRY"],
        "theorem_template_count": 3,
    }, "three minimal templates")
    need(result["proof_boundary"]["independent_per_origin_polynomial_or_SOS_certificate_present"] is False
         and result["future_C30f_terminal_adapter_contract"]["adapter_exists_now"] is False
         and result["future_C30f_terminal_adapter_contract"]["formal_54_to_0_authorized"] is False,
         "proof and future adapter boundary")
    need(result["formal_boundary"] == {
        "CM2": "NO-GO_FOR_CLAIM", "D02": "BLOCKED_COMPOSITE",
        "D03": "UNAUTHORIZED", "D04": "NOT_MINTED", "Gate5": "10/18",
        "can_serve_as_compact_q_formal_predecessor": False,
        "compact_q_formal_remaining_origins": 54,
        "diagnostic_54_to_18_authorized": False,
        "diagnostic_research_coverage_only": "36/54",
        "formal_54_to_0_authorized": False, "formal_credit": 0,
        "ledger_unchanged": True, "source_W_formal_remaining": 80,
        "terminal_gate_present": False,
    }, "exact nonpromotion boundary")


def verify(path: Path) -> dict[str, Any]:
    ctx.prec = 256
    need(hashlib.sha256(capture(PRODUCER)).hexdigest() == PRODUCER_SHA256,
         "producer source pin")
    raw = capture(path)
    candidate = strict_json(raw, "candidate")
    need(raw == canonical(candidate) + b"\n", "canonical candidate bytes")
    need(set(candidate) == {"schema", "result", "result_sha256"}
         and candidate["schema"] == SCHEMA, "candidate envelope")
    need(candidate["result_sha256"] == digest(candidate["result"])
         == EXPECTED_RESULT_SHA256, "frozen candidate result closure")
    authority = independent_authority(candidate)
    census = independent_census(candidate)
    analytic = independent_analytic(candidate, census)
    static_boundary(candidate)
    return {"authority": authority, "analytic": analytic, "origin_count": len(census)}


def main(argv: list[str]) -> int:
    try:
        need(len(argv) == 2, "usage: verifier CANDIDATE")
        reconstruction = verify(Path(argv[1]).absolute())
        output = {
            "schema": "cm2.round306c30q8.independent-verification.zero-credit.v1",
            "status": "PASS_INDEPENDENT_FULL_54_GLOBAL_TEMPLATE_REBUILD__ZERO_CREDIT",
            "candidate_result_sha256": EXPECTED_RESULT_SHA256,
            "producer_sha256": PRODUCER_SHA256,
            "producer_imported_or_executed": False,
            "independent_reconstruction": reconstruction,
            "formal_credit": 0,
            "source_W_formal_remaining": 80,
            "compact_q_formal_remaining": 54,
            "formal_54_to_0_authorized": False,
            "can_serve_as_formal_predecessor": False,
        }
        sys.stdout.buffer.write(canonical(output) + b"\n")
        return 0
    except (OSError, KeyError, TypeError, ValueError, StopIteration, Reject) as error:
        sys.stderr.write("REJECT_C30Q8_VERIFY:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
