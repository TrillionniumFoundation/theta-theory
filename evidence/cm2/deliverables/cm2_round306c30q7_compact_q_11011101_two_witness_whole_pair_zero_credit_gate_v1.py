#!/usr/bin/env python3
"""Append-only zero-credit Q7 theorem for the 03.15.11011101 N/S pair.

The old Q1 sufficient test required ``f(1) < 0`` for one fixed future
target.  That test closes only four of the sixteen analytic roots on each
origin.  Here the sixteen frozen roots are audited first, then one global
interval calculation (not a twelve-root subdivision) uses W[-1,0] up to
r=13/16 and the reflected G target afterwards.  The G chord enters and
leaves before time one, so its strictly positive f(1) is expected.

This is research evidence only.  It binds the current C30b W80/Q54 state and
the Q6 zero-credit receipt, but it is not a formal cohort predecessor.
"""

from __future__ import annotations

from fractions import Fraction as Q
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any

from flint import arb, ctx


sys.dont_write_bytecode = True
HERE = Path(__file__).absolute().parent
ROOT = HERE.parent
SCHEMA = (
    "cm2.round306c30q7.compact-q-11011101-two-witness-whole-pair-"
    "zero-credit-gate.v1"
)
ORIGINS = (
    "W:N:03.15.11011101",
    "W:S:H.03.15.11011101",
)
G_TARGET = {
    ORIGINS[0]: "G[0,1]",
    ORIGINS[1]: "G[0,0]",
}
LEFT_TARGET = "W[-1,0]"
FROZEN_TARGET = "W[1,0]"
T_DOMAIN = (Q(-531, 8000), Q(-177, 3200))
S_DOMAIN = (Q(-1, 400), Q(1, 400))
R_DOMAIN = (Q(0), Q(1))
SWITCH = Q(13, 16)
K = Q(1023, 262144)
SOURCE_RADIUS = Q(4, 25)
G_RADIUS = Q(9, 25)
T_INTERVALS = (
    (Q(-531, 8000), Q(-8319, 128000)),
    (Q(-8319, 128000), Q(-4071, 64000)),
    (Q(-4071, 64000), Q(-1593, 25600)),
    (Q(-1593, 25600), Q(-1947, 32000)),
    (Q(-1947, 32000), Q(-7611, 128000)),
    (Q(-7611, 128000), Q(-3717, 64000)),
    (Q(-3717, 64000), Q(-7257, 128000)),
    (Q(-7257, 128000), Q(-177, 3200)),
)
S_INTERVALS = ((Q(-1, 400), Q(0)), (Q(0), Q(1, 400)))

PATHS = {
    "c30b_manifest": "deliverables/cm2_round306c30b_source_w_outgoing_h_whole_origin_disposition_manifest.sha256",
    "c30b_result": "deliverables/cm2_round306c30b_sealed/cm2_round306c30b_source_w_outgoing_h_whole_origin_disposition_result.json",
    "c30b_verification": "deliverables/cm2_round306c30b_source_w_outgoing_h_whole_origin_disposition_verification.json",
    "q1_a": ".cm2-runtime/audit/c30q1-cohort-counterexample-v3-20260807T1205/seed30630071_stdout.json",
    "q1_b": ".cm2-runtime/audit/c30q1-cohort-counterexample-v3-20260807T1205/seed30630929_stdout.json",
    "q2_a": ".cm2-runtime/audit/c30q2-seven-cohort-routing-v3-20260807T1325/seed30630071_stdout.json",
    "q2_b": ".cm2-runtime/audit/c30q2-seven-cohort-routing-v3-20260807T1325/seed30630929_stdout.json",
    "q6_manifest": ".cm2-runtime/audit/c30q6-six-origin-clean-room-zero-credit-v1-20260808T085007Z/manifest.sha256",
    "q6_receipt": ".cm2-runtime/audit/c30q6-six-origin-clean-room-zero-credit-v1-20260808T085007Z/receipt.json",
}
PINS = {
    "c30b_manifest": "6af636a4239f390712d057030f03e09fbbca332c6170f183d3d0095f19f0f248",
    "c30b_result": "b015e5bd6a4ee01d71ac95765d07dcbc63c3888f0c8ff9205e2d8c688958c11b",
    "c30b_verification": "e9e72536be9ba707fe2fdf6034b47978be4d09235e5133414ec7b0a31acf4e71",
    "q1_a": "037e30eb015ab5c9eb802ecda7641144c4f6fd74b6db115c75aa0c7467793574",
    "q1_b": "037e30eb015ab5c9eb802ecda7641144c4f6fd74b6db115c75aa0c7467793574",
    "q2_a": "a3af728ac34b07ad86f9045c28bc3eabe88ea446e051cbe37b26d3baa270637b",
    "q2_b": "a3af728ac34b07ad86f9045c28bc3eabe88ea446e051cbe37b26d3baa270637b",
    "q6_manifest": "6df3516930ae49a655e2bcdb000db89040f3bb5040db5032afc6afb1dd0eece6",
    "q6_receipt": "8906bd8fa15f7b73f988847c0782de1367a14928aaa991ddeda90f764b47469b",
}


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
    fields = ("st_dev", "st_ino", "st_mode", "st_nlink", "st_size",
              "st_mtime_ns", "st_ctime_ns", "st_uid", "st_gid")
    need(all(getattr(before, key) == getattr(after, key) for key in fields),
         "stable input:" + str(path))
    return raw


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in result, "duplicate JSON key:" + label)
            result[key] = value
        return result
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


def pinned_raw(name: str) -> bytes:
    raw = capture(ROOT / PATHS[name])
    need(hashlib.sha256(raw).hexdigest() == PINS[name], "pin:" + name)
    return raw


def document(name: str) -> dict[str, Any]:
    return strict_json(pinned_raw(name), name)


def verify_manifest(name: str, base: Path) -> int:
    raw = pinned_raw(name)
    rows = raw.decode("ascii", "strict").splitlines()
    seen: set[str] = set()
    for row in rows:
        need(len(row) >= 67 and row[64:66] == "  ", "manifest row:" + name)
        expected, relative = row[:64], row[66:]
        need(all(char in "0123456789abcdef" for char in expected),
             "manifest digest:" + name)
        part = Path(relative)
        need(not part.is_absolute() and ".." not in part.parts
             and relative not in seen, "manifest path:" + name)
        seen.add(relative)
        workspace = ROOT / part
        target = workspace if workspace.exists() else base / part
        need(target.absolute().is_relative_to(ROOT), "manifest scope:" + name)
        need(hashlib.sha256(capture(target)).hexdigest() == expected,
             "manifest member:" + name + ":" + relative)
    need(bool(rows), "nonempty manifest:" + name)
    return len(rows)


def result_closed(document_value: dict[str, Any], label: str) -> None:
    need(document_value.get("result_sha256") == digest(document_value.get("result")),
         "inner result closure:" + label)


def fraction_pair(values: list[str]) -> tuple[Q, Q]:
    need(type(values) is list and len(values) == 2
         and all(type(value) is str for value in values), "fraction pair")
    return Q(values[0]), Q(values[1])


def authority_binding() -> dict[str, Any]:
    c30b_members = verify_manifest("c30b_manifest", ROOT / "deliverables")
    q6_dir = (ROOT / PATHS["q6_manifest"]).parent
    q6_members = verify_manifest("q6_manifest", q6_dir)
    c30b = document("c30b_result")
    verification = document("c30b_verification")
    need(c30b["status"] == "PASS_BOUNDED_ROUND306C30B_OUTGOING_H_DISPOSITION",
         "C30b status")
    need(verification["status"] ==
         "PASS_FORMAL_C30B__688_H_CELLS__2_WHOLE_ORIGIN_EXCLUSIONS__10_RESOLVED_MIXED__SOURCE_W_92_TO_80__D02_STILL_BLOCKED",
         "C30b verification")
    after = c30b["source_W_ledger_transition"]["after"]
    need(after["remaining"] == 80
         and after["remaining_partition"]["compact_q"] == 54
         and after["excluded"] + after["conservative_live"] == 76832,
         "C30b W80/Q54 conservation")
    q6 = document("q6_receipt")
    need(q6["status"] ==
         "PASS_C30Q6_CLEAN_ROOM_DUAL_SEED_COLD_REPLAY_AND_ATTACKS__FAIL_CLOSED_ZERO_CREDIT",
         "Q6 status")
    need(q6["strict_nonpromotion"] == {
        "CM2": "NO-GO_FOR_CLAIM", "D02": "BLOCKED_COMPOSITE",
        "D03": "UNAUTHORIZED", "D04": "NOT_MINTED", "Gate5": "10/18",
        "compact_q_formal_remaining_origins": 54, "formal_credit": 0,
        "ledger_unchanged": True, "source_W_formal_remaining": 80,
    }, "Q6 nonpromotion")
    return {
        "formal_round": "Round306C30b",
        "c30b_manifest_sha256": PINS["c30b_manifest"],
        "c30b_manifest_member_count": c30b_members,
        "c30b_result_sha256": PINS["c30b_result"],
        "c30b_verification_sha256": PINS["c30b_verification"],
        "source_W_formal_remaining": 80,
        "compact_q_formal_remaining": 54,
        "q6_zero_credit_manifest_sha256": PINS["q6_manifest"],
        "q6_zero_credit_manifest_member_count": q6_members,
        "q6_zero_credit_receipt_sha256": PINS["q6_receipt"],
        "q6_is_research_evidence_not_formal_predecessor": True,
    }


def audit_roots() -> dict[str, Any]:
    raw1a, raw1b = pinned_raw("q1_a"), pinned_raw("q1_b")
    raw2a, raw2b = pinned_raw("q2_a"), pinned_raw("q2_b")
    need(raw1a == raw1b and raw2a == raw2b, "Q1/Q2 dual-seed bytes")
    q1, q2 = strict_json(raw1a, "q1"), strict_json(raw2a, "q2")
    result_closed(q1, "Q1")
    result_closed(q2, "Q2")
    need(q1["result"]["status"].startswith(
         "REJECT_AUTOMATIC_REPRESENTATIVE_CERTIFICATE_EXTENSION__"),
         "Q1 historical fail-closed status")
    need(q2["result"]["status"] ==
         "PASS_EXACT_SEVEN_COHORT_ROUTING_LEDGER__REJECT_AUTOMATIC_EXTENSION__ZERO_FORMAL_CREDIT",
         "Q2 routing status")
    pattern = next(
        row for row in q2["result"]["exact_seven_cohort_ledger"]["patterns"]
        if row["origin_keys"] == list(ORIGINS)
    )
    need(pattern["pattern"] == {
        "analytic_root_count_per_origin": 16,
        "applicable_root_count_per_origin": 4,
        "frozen_behind_root_count_per_origin": 16,
        "future_witness_root_count_per_origin": 4,
    }, "Q2 old 4/16 pattern")
    need(pattern["root_failure_summary"] == {
        "applicability_gap_root_count": 24,
        "frozen_behind_gap_root_count": 0,
        "future_witness_gap_root_count": 24,
    }, "Q2 exact 12+12 old gaps")

    all_roots = q1["result"]["analytic_cohort_census"]["root_results"]
    selected = sorted(
        (row for row in all_roots if row["origin_key"] in ORIGINS),
        key=lambda row: row["root_key"],
    )
    need(len(selected) == 32, "exact pair root count")
    need([row["root_key"] for row in selected] == pattern["root_keys"],
         "Q1/Q2 root keys")
    need(digest(pattern["root_keys"]) == pattern["root_keys_sha256"],
         "Q2 root key digest")
    complement = {
        row["origin_key"]: row
        for row in q1["result"]["pinned_complement_replay"]["origin_rows"]
        if row["origin_key"] in ORIGINS
    }
    need(set(complement) == set(ORIGINS), "pair complement rows")

    origin_rows: list[dict[str, Any]] = []
    for origin in ORIGINS:
        rows = [row for row in selected if row["origin_key"] == origin]
        need(len(rows) == 16, "16 roots:" + origin)
        p_sign = 1 if origin == ORIGINS[0] else -1
        p_domain = (Q(511, 512), Q(1)) if p_sign == 1 else (
            Q(-1), Q(-511, 512)
        )
        boxes: set[tuple[Q, Q, Q, Q]] = set()
        old_pass = 0
        old_gap = 0
        for row in rows:
            parameters = row["cohort_parameters"]
            need(parameters["p_sign"] == p_sign
                 and parameters["exact_q_squared_scale"] == str(K)
                 and fraction_pair(parameters["exact_r_domain"]) == R_DOMAIN
                 and fraction_pair(parameters["source_p_endpoint_domain"]) == p_domain,
                 "root parameterization:" + row["root_key"])
            required = {FROZEN_TARGET, LEFT_TARGET, G_TARGET[origin]}
            need(required.issubset(set(parameters["active_target_set"])),
                 "required targets:" + row["root_key"])
            t0, t1 = fraction_pair(parameters["exact_t_domain"])
            s0, s1 = fraction_pair(parameters["exact_s_domain"])
            boxes.add((t0, t1, s0, s1))
            need(row["frozen_target"]["strict"]["ell_negative"] is True
                 and row["frozen_target"]["strict"]["f_at_0_positive"] is True,
                 "frozen owner behind:" + row["root_key"])
            if row["analytic_root_applicable"] is True:
                old_pass += 1
                need(row["failure_reasons"] == [], "old pass reasons")
            else:
                old_gap += 1
                need(row["failure_reasons"] == [
                    "NO_NONFROZEN_F0_POSITIVE_F1_NEGATIVE_TRANSVERSE_WITNESS"
                ], "exact old sufficient-condition gap")
        expected_boxes = {
            (t0, t1, s0, s1)
            for t0, t1 in T_INTERVALS for s0, s1 in S_INTERVALS
        }
        need(boxes == expected_boxes and old_pass == 4 and old_gap == 12,
             "exact 16-root tiling and 12-root gap:" + origin)
        comp = complement[origin]
        need(comp["Round180_final_child_count"] == 539
             and comp["P215_exact_behind_closed_child_count"] == 411
             and comp["P215_residual_child_count"] == 128
             and comp["P215_residual_category_count"] == {
                 "SOURCE_GRAZING_COMPACT_Q_RESIDUAL": 128
             } and comp["source_grazing_root_count"] == 16,
             "complement conservation:" + origin)
        root_keys = [row["root_key"] for row in rows]
        origin_rows.append({
            "origin_key": origin,
            "root_count": 16,
            "old_sufficient_test_pass_count": old_pass,
            "old_sufficient_test_gap_count": old_gap,
            "all_16_frozen_W_1_0_strictly_behind": True,
            "root_keys_sha256": digest(root_keys),
            "root_keys": root_keys,
            "global_t_domain": [str(T_DOMAIN[0]), str(T_DOMAIN[1])],
            "global_s_domain": [str(S_DOMAIN[0]), str(S_DOMAIN[1])],
            "global_r_domain": ["0", "1"],
            "root_box_tiling": "8 exact t intervals x 2 exact s intervals",
            "P215_exact_behind_closed_child_count": 411,
            "analytic_compact_q_residual_child_count": 128,
        })
    return {
        "q1_dual_seed_stdout_sha256": PINS["q1_a"],
        "q2_dual_seed_stdout_sha256": PINS["q2_a"],
        "pair_root_count": 32,
        "roots_per_origin": 16,
        "old_gap_roots_per_origin": 12,
        "old_gap_root_count_pair": 24,
        "old_gap_is_failure_of_f1_negative_sufficient_test_not_counterexample": True,
        "pair_root_keys_sha256": pattern["root_keys_sha256"],
        "exact_global_t_s_tiling_verified": True,
        "origin_rows_sha256": digest(origin_rows),
        "origin_rows": origin_rows,
    }


def arbq(value: Q) -> arb:
    return arb(value.numerator) / value.denominator


def interval(lower: Q, upper: Q) -> arb:
    need(lower <= upper, "interval order")
    middle = (lower + upper) / 2
    radius = (upper - lower) / 2
    return arbq(middle) + arb(0, arbq(radius).upper())


def bounds(value: arb) -> dict[str, str]:
    return {
        "enclosure": str(value),
        "lower": str(value.lower()),
        "upper": str(value.upper()),
    }


def root_metric(C: arb, D: arb, b: arb, P: arb, radius: Q) -> tuple[dict[str, Any], dict[str, arb]]:
    ell = b * C + P * D
    transverse = b * D - P * C
    f0 = C * C + D * D - arbq(radius * radius)
    delta = arbq(radius * radius) - transverse * transverse
    need(bool(delta > 0), "strict discriminant")
    square_root = delta.sqrt()
    tau_minus = ell - square_root
    tau_plus = ell + square_root
    f1 = f0 + arb(1) - 2 * ell
    values = {
        "forward_projection_ell": ell,
        "signed_transverse": transverse,
        "f_at_0": f0,
        "f_at_1": f1,
        "discriminant": delta,
        "tau_minus": tau_minus,
        "tau_plus": tau_plus,
    }
    return ({key: bounds(value) for key, value in values.items()}, values)


def analytic_theorem() -> tuple[dict[str, Any], dict[str, Any]]:
    t = interval(*T_DOMAIN)
    s = interval(*S_DOMAIN)
    a = (arb(1) - t * t).sqrt()
    u = arbq(Q(1, 2)) + s
    A = a * u + t / 2
    B = t * u - a / 2 + arbq(SOURCE_RADIUS)
    q_scale = arbq(K).sqrt()

    def p_data(r0: Q, r1: Q) -> tuple[arb, arb]:
        b = q_scale * interval(r0, r1)
        P = (arb(1) - b * b).sqrt()
        return b, P

    b_all, P_all = p_data(Q(0), Q(1))
    frozen_C, frozen_D = t - arbq(SOURCE_RADIUS), -a
    frozen = {
        "forward_projection_ell": b_all * frozen_C + P_all * frozen_D,
        "signed_transverse": b_all * frozen_D - P_all * frozen_C,
        "f_at_0": (
            frozen_C * frozen_C + frozen_D * frozen_D
            - arbq(SOURCE_RADIUS * SOURCE_RADIUS)
        ),
    }
    frozen_bounds = {key: bounds(value) for key, value in frozen.items()}
    need(bool(frozen["f_at_0"] > 0) and bool(frozen["forward_projection_ell"] < 0),
         "global frozen owner strictly behind")

    b_left, P_left = p_data(Q(0), SWITCH)
    left_bounds, left = root_metric(
        -t - arbq(SOURCE_RADIUS), a, b_left, P_left, SOURCE_RADIUS
    )
    need(bool(left["f_at_0"] > 0) and bool(left["forward_projection_ell"] > 0)
         and bool(left["discriminant"] > 0) and bool(left["tau_minus"] > 0)
         and bool(left["tau_minus"] < 1) and bool(left["f_at_1"] < 0),
         "global left W witness")

    b_right, P_right = p_data(SWITCH, Q(1))
    right_bounds, right = root_metric(-B, A, b_right, P_right, G_RADIUS)
    need(bool(right["f_at_0"] > 0) and bool(right["forward_projection_ell"] > 0)
         and bool(right["discriminant"] > 0) and bool(right["tau_minus"] > 0)
         and bool(right["tau_plus"] < 1) and bool(right["f_at_1"] > 0),
         "global right G two-crossing chord witness")

    b_seam, P_seam = p_data(SWITCH, SWITCH)
    seam_left_bounds, seam_left = root_metric(
        -t - arbq(SOURCE_RADIUS), a, b_seam, P_seam, SOURCE_RADIUS
    )
    seam_right_bounds, seam_right = root_metric(-B, A, b_seam, P_seam, G_RADIUS)
    for label, values in (("left", seam_left), ("right", seam_right)):
        need(bool(values["f_at_0"] > 0)
             and bool(values["forward_projection_ell"] > 0)
             and bool(values["discriminant"] > 0)
             and bool(values["tau_minus"] > 0)
             and bool(values["tau_minus"] < 1), "strict seam:" + label)
    need(bool(seam_right["tau_plus"] < 1) and bool(seam_right["f_at_1"] > 0),
         "right seam chord")

    # Exact endpoint algebra backs the interval result without enumerating
    # any of the twelve historic gap roots.
    c2 = K * SWITCH * SWITCH
    h2 = Q(1) - c2
    worst_t = T_DOMAIN[1]
    a2 = Q(1) - worst_t * worst_t
    tangent_shift = worst_t + SOURCE_RADIUS
    outside_half = Q(1) + SOURCE_RADIUS * worst_t
    left_square_gap = (
        h2 * a2 - outside_half * outside_half
        - c2 * tangent_shift * tangent_shift
    )
    left_unsquared_gap = (
        left_square_gap * left_square_gap
        - 4 * outside_half * outside_half
        * tangent_shift * tangent_shift * c2
    )
    need(
        (c2, h2, a2, tangent_shift, outside_half, left_square_gap,
         left_unsquared_gap) == (
            Q(172887, 67108864), Q(66935977, 67108864),
            Q(10208671, 10240000), Q(67, 640), Q(19823, 20000),
            Q(5018751356871, 419430400000000),
            Q(5670073442246922990910641,
              175921860444160000000000000000),
        ) and left_square_gap > 0 and left_unsquared_gap > 0,
        "exact left endpoint algebra",
    )
    need(
        bool(a > arbq(Q(997, 1000))) and bool(a < 1)
        and bool(b_right > arbq(Q(1, 20)))
        and bool(b_right < arbq(Q(1, 16)))
        and bool(P_right > arbq(Q(499, 500))) and bool(P_right < 1)
        and bool(A > arbq(Q(23141, 50000)))
        and bool(A < arbq(Q(3039, 6400)))
        and bool(-B > arbq(Q(468503, 1280000)))
        and bool(-B < arbq(Q(1194731, 3200000)))
        and bool(right["forward_projection_ell"] > arbq(Q(1536624827, 3200000000)))
        and bool(right["forward_projection_ell"] < arbq(Q(25506731, 51200000)))
        and bool(right["signed_transverse"] > -arbq(Q(5603399, 16000000)))
        and bool(right["signed_transverse"] < -arbq(Q(214789247, 640000000)))
        and bool(right["f_at_0"] > arbq(Q(541, 2500))),
        "global rational right chord guards",
    )

    coordinate_model = {
        "source_normal": {
            "North": "n=(t,+sqrt(1-t^2))",
            "South": "n=(t,-sqrt(1-t^2))",
        },
        "velocity": "v=b*n+P*n_perp with b=sqrt(1023/262144)*r and P=sqrt(1-b^2)",
        "global_domains": {
            "t": [str(T_DOMAIN[0]), str(T_DOMAIN[1])],
            "s": [str(S_DOMAIN[0]), str(S_DOMAIN[1])],
            "r": ["0", "1"],
        },
        "reflection": "(North,p>0,G[0,1]) <-> (South,p<0,G[0,0]) by y -> -y",
        "selected_G_target": G_TARGET,
        "shared_scalar_definitions": {
            "a": "sqrt(1-t^2)", "u": "1/2+s",
            "A": "a*u+t/2", "B": "t*u-a/2+4/25",
            "G_ell": "P*A-b*B", "G_transverse": "b*A+P*B",
        },
        "shared_scalar_interval_bounds": {
            "a": bounds(a), "A": bounds(A), "B": bounds(B),
        },
    }
    theorem = {
        "proof_method": (
            "two global 256-bit Arb interval boxes plus one exact switch seam; "
            "no finite subdivision of the twelve old gap roots"
        ),
        "finite_old_gap_root_subdivision_count": 0,
        "global_witness_interval_box_count": 2,
        "frozen_owner_global": {
            "target": FROZEN_TARGET,
            "domain": "t,s,r full global product",
            "strict_f_at_0_positive": True,
            "strict_forward_projection_negative": True,
            "therefore_no_positive_frozen_root": True,
            "interval_bounds": frozen_bounds,
        },
        "left_witness": {
            "targets": {origin: LEFT_TARGET for origin in ORIGINS},
            "closed_proof_domain": ["0", str(SWITCH)],
            "assigned_half_open_domain": "[0,13/16)",
            "criterion": "outside start, strict discriminant, 0<tau_minus<1",
            "strict_f_at_1_negative_observed_but_not_used_as_global_language": True,
            "interval_bounds": left_bounds,
        },
        "right_witness": {
            "targets": G_TARGET,
            "closed_proof_domain": [str(SWITCH), "1"],
            "assigned_half_open_domain": "[13/16,1]",
            "criterion": "two-crossing chord: outside at 0 and 1, 0<tau_minus<tau_plus<1",
            "strict_f_at_1_sign": "POSITIVE",
            "old_f_at_1_negative_sufficient_condition_satisfied": False,
            "old_f_at_1_negative_condition_is_not_necessary": True,
            "interval_bounds": right_bounds,
        },
        "switch_seam": {
            "r": str(SWITCH),
            "assignment_owner": "right_witness",
            "left_closed_proof_strict_at_seam": True,
            "right_closed_proof_strict_at_seam": True,
            "assigned_domains_have_gap": False,
            "assigned_domains_have_overlap": False,
            "left_interval_bounds": seam_left_bounds,
            "right_interval_bounds": seam_right_bounds,
        },
        "analytic_rational_guards": {
            "left_monotone_endpoint": {
                "worst_t": str(worst_t), "worst_r": str(SWITCH),
                "c_squared": str(c2), "h_squared": str(h2),
                "a_squared": str(a2), "t_plus_4_over_25": str(tangent_shift),
                "one_plus_4t_over_25": str(outside_half),
                "first_square_gap": str(left_square_gap),
                "unsquared_strict_gap": str(left_unsquared_gap),
                "both_gaps_strict_positive": True,
            },
            "right_global_bounds": {
                "a": ["997/1000", "1"],
                "b": ["1/20", "1/16"],
                "P": ["499/500", "1"],
                "A": ["23141/50000", "3039/6400"],
                "minus_B": ["468503/1280000", "1194731/3200000"],
                "ell": ["1536624827/3200000000", "25506731/51200000"],
                "signed_transverse": ["-5603399/16000000", "-214789247/640000000"],
                "f_at_0_strict_lower": "541/2500",
                "implied_chord": "0<tau_minus<tau_plus<1",
            },
            "proof_uses_global_monotonicity_and_interval_bounds": True,
            "proof_does_not_enumerate_twelve_gap_roots": True,
        },
        "witness_language": {
            "kind": "PIECEWISE_TWO_WITNESS_GLOBAL_ANALYTIC_COVER",
            "single_uniform_witness_claimed": False,
            "north_south_target_reflection_verified": True,
            "every_r_in_closed_unit_interval_assigned_exactly_once": True,
            "both_closed_proof_domains_strict_at_shared_switch": True,
        },
    }
    return coordinate_model, theorem


def build() -> dict[str, Any]:
    ctx.prec = 256
    binding = authority_binding()
    root_audit = audit_roots()
    coordinate_model, theorem = analytic_theorem()
    return {
        "status": (
            "PASS_11011101_NORTH_SOUTH_WHOLE_PAIR_GLOBAL_TWO_WITNESS_"
            "ANALYTIC_THEOREM__ZERO_FORMAL_CREDIT"
        ),
        "verdict": "RESEARCH_WHOLE_PAIR_EXCLUSION_PASS__FORMAL_STATE_UNCHANGED",
        "scope": "the two frozen 03.15.11011101 compact-q origins only",
        "authority_binding": binding,
        "exact_root_and_old_gap_audit": root_audit,
        "global_coordinate_model": coordinate_model,
        "two_witness_analytic_theorem": theorem,
        "whole_pair_research_conclusion": {
            "origin_count": 2,
            "origin_keys": list(ORIGINS),
            "per_origin_Round180_children": 539,
            "per_origin_P215_exact_behind_closed_children": 411,
            "per_origin_compact_q_residual_children_covered_by_global_theorem": 128,
            "per_origin_all_16_full_r_roots_covered_without_gap_root_subdivision": True,
            "both_origins_research_excluded_from_frozen_W_1_0_first_ownership": True,
            "formal_disposition_minted": False,
        },
        "formal_boundary": {
            "formal_credit": 0,
            "ledger_unchanged": True,
            "source_W_formal_remaining": 80,
            "compact_q_formal_remaining_origins": 54,
            "diagnostic_transition_only": "54 -> 52",
            "diagnostic_transition_authorized": False,
            "terminal_gate_present": False,
            "uniform_formal_predecessor_authority": False,
            "can_serve_as_compact_q_cohort_formal_predecessor": False,
            "D02": "BLOCKED_COMPOSITE", "D03": "UNAUTHORIZED",
            "D04": "NOT_MINTED", "Gate5": "10/18",
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
        sys.stderr.write("REJECT_C30Q7:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
