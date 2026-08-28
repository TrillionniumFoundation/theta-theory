#!/usr/bin/env python3
"""No-import verifier for the Q7 03.15.11011101 two-witness theorem."""

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
PRODUCER = (
    HERE
    / "cm2_round306c30q7_compact_q_11011101_two_witness_whole_pair_"
      "zero_credit_gate_v1.py"
)
PRODUCER_SHA256 = "f1e7d8e983d6783f8acc5d72a4790c6aecae7726c7a20c8d959b638a5ef6d8d9"
SCHEMA = (
    "cm2.round306c30q7.compact-q-11011101-two-witness-whole-pair-"
    "zero-credit-gate.v1"
)
EXPECTED_RESULT_SHA256 = "a9cfc853eb97bbea1cd0c078a3e40a048f092ecb10d79026237d79dec8ceaace"
ORIGINS = ("W:N:03.15.11011101", "W:S:H.03.15.11011101")
G_TARGET = {ORIGINS[0]: "G[0,1]", ORIGINS[1]: "G[0,0]"}
T_DOMAIN = (Q(-531, 8000), Q(-177, 3200))
S_DOMAIN = (Q(-1, 400), Q(1, 400))
SWITCH = Q(13, 16)
K = Q(1023, 262144)
RW, RG = Q(4, 25), Q(9, 25)
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
    "q6_manifest": (
        ".cm2-runtime/audit/c30q6-six-origin-clean-room-zero-credit-v1-20260808T085007Z/manifest.sha256",
        "6df3516930ae49a655e2bcdb000db89040f3bb5040db5032afc6afb1dd0eece6",
    ),
    "q6_receipt": (
        ".cm2-runtime/audit/c30q6-six-origin-clean-room-zero-credit-v1-20260808T085007Z/receipt.json",
        "8906bd8fa15f7b73f988847c0782de1367a14928aaa991ddeda90f764b47469b",
    ),
}


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


def capture(path: Path, require_single_link: bool = True) -> bytes:
    absolute = path.absolute()
    need(absolute.resolve(strict=True) == absolute, "canonical file:" + str(path))
    before = os.lstat(absolute)
    need(stat.S_ISREG(before.st_mode)
         and (not require_single_link or before.st_nlink == 1),
         "regular file:" + str(path))
    raw = absolute.read_bytes()
    after = os.lstat(absolute)
    fields = ("st_dev", "st_ino", "st_mode", "st_nlink", "st_size",
              "st_mtime_ns", "st_ctime_ns", "st_uid", "st_gid")
    need(all(getattr(before, key) == getattr(after, key) for key in fields),
         "stable file:" + str(path))
    return raw


def strict_json(raw: bytes, label: str) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in result, "duplicate key:" + label)
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


def pinned(name: str) -> bytes:
    relative, expected = INPUTS[name]
    raw = capture(ROOT / relative)
    need(hashlib.sha256(raw).hexdigest() == expected, "input pin:" + name)
    return raw


def doc(name: str) -> dict[str, Any]:
    return strict_json(pinned(name), name)


def verify_manifest(name: str, base: Path) -> int:
    rows = pinned(name).decode("ascii", "strict").splitlines()
    seen: set[str] = set()
    for row in rows:
        need(len(row) >= 67 and row[64:66] == "  ", "manifest syntax:" + name)
        expected, relative = row[:64], row[66:]
        part = Path(relative)
        need(all(char in "0123456789abcdef" for char in expected)
             and not part.is_absolute() and ".." not in part.parts
             and relative not in seen, "manifest row:" + name)
        seen.add(relative)
        workspace = ROOT / part
        target = workspace if workspace.exists() else base / part
        need(hashlib.sha256(capture(target)).hexdigest() == expected,
             "manifest member:" + name + ":" + relative)
    need(bool(rows), "manifest nonempty:" + name)
    return len(rows)


def pair(value: Any) -> tuple[Q, Q]:
    need(type(value) is list and len(value) == 2
         and all(type(item) is str for item in value), "fraction pair")
    return Q(value[0]), Q(value[1])


def independently_audit_authority_and_roots(candidate: dict[str, Any]) -> dict[str, Any]:
    c30b_members = verify_manifest("c30b_manifest", ROOT / "deliverables")
    q6_members = verify_manifest("q6_manifest", (ROOT / INPUTS["q6_manifest"][0]).parent)
    c30b, c30bv, q6 = doc("c30b_result"), doc("c30b_verification"), doc("q6_receipt")
    need(c30b["status"] == "PASS_BOUNDED_ROUND306C30B_OUTGOING_H_DISPOSITION",
         "C30b result")
    need(c30bv["status"].endswith("SOURCE_W_92_TO_80__D02_STILL_BLOCKED"),
         "C30b verification")
    after = c30b["source_W_ledger_transition"]["after"]
    need(after["remaining"] == 80 and after["remaining_partition"]["compact_q"] == 54
         and after["excluded"] + after["conservative_live"] == 76832,
         "formal W80/Q54")
    need(q6["strict_nonpromotion"]["formal_credit"] == 0
         and q6["strict_nonpromotion"]["source_W_formal_remaining"] == 80
         and q6["strict_nonpromotion"]["compact_q_formal_remaining_origins"] == 54,
         "Q6 state")
    binding = candidate["result"]["authority_binding"]
    need(binding["c30b_manifest_member_count"] == c30b_members
         and binding["q6_zero_credit_manifest_member_count"] == q6_members
         and binding["c30b_manifest_sha256"] == INPUTS["c30b_manifest"][1]
         and binding["q6_zero_credit_receipt_sha256"] == INPUTS["q6_receipt"][1]
         and binding["source_W_formal_remaining"] == 80
         and binding["compact_q_formal_remaining"] == 54
         and binding["q6_is_research_evidence_not_formal_predecessor"] is True,
         "candidate authority binding")

    q1a, q1b, q2a, q2b = pinned("q1a"), pinned("q1b"), pinned("q2a"), pinned("q2b")
    need(q1a == q1b and q2a == q2b, "historic dual seed bytes")
    q1, q2 = strict_json(q1a, "Q1"), strict_json(q2a, "Q2")
    need(q1["result_sha256"] == digest(q1["result"])
         and q2["result_sha256"] == digest(q2["result"]), "historic result closure")
    pattern = next(row for row in q2["result"]["exact_seven_cohort_ledger"]["patterns"]
                   if row["origin_keys"] == list(ORIGINS))
    need(pattern["pattern"]["analytic_root_count_per_origin"] == 16
         and pattern["pattern"]["applicable_root_count_per_origin"] == 4
         and pattern["pattern"]["frozen_behind_root_count_per_origin"] == 16
         and pattern["root_failure_summary"]["future_witness_gap_root_count"] == 24,
         "Q2 4/16 and 12+12 gaps")
    roots = sorted((row for row in q1["result"]["analytic_cohort_census"]["root_results"]
                    if row["origin_key"] in ORIGINS), key=lambda row: row["root_key"])
    need(len(roots) == 32 and [row["root_key"] for row in roots] == pattern["root_keys"],
         "exact Q1/Q2 roots")
    per_origin: dict[str, dict[str, Any]] = {}
    expected_boxes = {(t0, t1, s0, s1) for t0, t1 in T_INTERVALS
                      for s0, s1 in S_INTERVALS}
    complements = {row["origin_key"]: row
                   for row in q1["result"]["pinned_complement_replay"]["origin_rows"]
                   if row["origin_key"] in ORIGINS}
    for origin in ORIGINS:
        selected = [row for row in roots if row["origin_key"] == origin]
        boxes, gaps, passes = set(), 0, 0
        p_sign = 1 if origin == ORIGINS[0] else -1
        p_domain = (Q(511, 512), Q(1)) if p_sign == 1 else (Q(-1), Q(-511, 512))
        for row in selected:
            p = row["cohort_parameters"]
            boxes.add((*pair(p["exact_t_domain"]), *pair(p["exact_s_domain"])))
            need(p["p_sign"] == p_sign and pair(p["source_p_endpoint_domain"]) == p_domain
                 and pair(p["exact_r_domain"]) == (Q(0), Q(1))
                 and {"W[1,0]", "W[-1,0]", G_TARGET[origin]}.issubset(
                     set(p["active_target_set"]))
                 and row["frozen_target"]["strict"]["ell_negative"] is True,
                 "root semantics:" + row["root_key"])
            if row["analytic_root_applicable"]:
                passes += 1
            else:
                gaps += 1
                need(row["failure_reasons"] == [
                    "NO_NONFROZEN_F0_POSITIVE_F1_NEGATIVE_TRANSVERSE_WITNESS"
                ], "old gap reason")
        comp = complements[origin]
        need(len(selected) == 16 and boxes == expected_boxes and passes == 4 and gaps == 12
             and comp["Round180_final_child_count"] == 539
             and comp["P215_exact_behind_closed_child_count"] == 411
             and comp["P215_residual_child_count"] == 128,
             "origin root/complement closure:" + origin)
        per_origin[origin] = {"roots": 16, "old_pass": 4, "old_gap": 12,
                              "closed": 411, "residual": 128}
    audit = candidate["result"]["exact_root_and_old_gap_audit"]
    need(audit["pair_root_count"] == 32 and audit["old_gap_roots_per_origin"] == 12
         and audit["pair_root_keys_sha256"] == pattern["root_keys_sha256"]
         and audit["exact_global_t_s_tiling_verified"] is True
         and audit["old_gap_is_failure_of_f1_negative_sufficient_test_not_counterexample"] is True,
         "candidate root audit")
    return {"c30b_manifest_members": c30b_members, "q6_manifest_members": q6_members,
            "pair_roots": len(roots), "per_origin": per_origin}


def aq(value: Q) -> arb:
    return arb(value.numerator) / value.denominator


def iv(lower: Q, upper: Q) -> arb:
    middle, radius = (lower + upper) / 2, (upper - lower) / 2
    return aq(middle) + arb(0, aq(radius).upper())


def bounds(value: arb) -> dict[str, str]:
    return {"enclosure": str(value), "lower": str(value.lower()),
            "upper": str(value.upper())}


def metric(C: arb, D: arb, b: arb, P: arb, radius: Q) -> tuple[dict[str, dict[str, str]], dict[str, arb]]:
    ell = b * C + P * D
    transverse = b * D - P * C
    f0 = C * C + D * D - aq(radius * radius)
    delta = aq(radius * radius) - transverse * transverse
    need(bool(delta > 0), "independent delta")
    square = delta.sqrt()
    values = {"forward_projection_ell": ell, "signed_transverse": transverse,
              "f_at_0": f0, "f_at_1": f0 + 1 - 2 * ell,
              "discriminant": delta, "tau_minus": ell - square,
              "tau_plus": ell + square}
    return {key: bounds(value) for key, value in values.items()}, values


def independently_verify_analytic(candidate: dict[str, Any]) -> dict[str, Any]:
    ctx.prec = 256
    t, s = iv(*T_DOMAIN), iv(*S_DOMAIN)
    a = (arb(1) - t * t).sqrt()
    u = aq(Q(1, 2)) + s
    A, B = a * u + t / 2, t * u - a / 2 + aq(RW)
    scale = aq(K).sqrt()

    def bp(lo: Q, hi: Q) -> tuple[arb, arb]:
        b = scale * iv(lo, hi)
        return b, (arb(1) - b * b).sqrt()

    ba, Pa = bp(Q(0), Q(1))
    Cf, Df = t - aq(RW), -a
    frozen = {"forward_projection_ell": ba * Cf + Pa * Df,
              "signed_transverse": ba * Df - Pa * Cf,
              "f_at_0": Cf * Cf + Df * Df - aq(RW * RW)}
    need(bool(frozen["forward_projection_ell"] < 0) and bool(frozen["f_at_0"] > 0),
         "independent frozen behind")
    bl, Pl = bp(Q(0), SWITCH)
    left_bounds, left = metric(-t - aq(RW), a, bl, Pl, RW)
    need(bool(left["forward_projection_ell"] > 0) and bool(left["f_at_0"] > 0)
         and bool(left["tau_minus"] > 0) and bool(left["tau_minus"] < 1)
         and bool(left["f_at_1"] < 0), "independent left interval")
    br, Pr = bp(SWITCH, Q(1))
    right_bounds, right = metric(-B, A, br, Pr, RG)
    need(bool(right["forward_projection_ell"] > 0) and bool(right["f_at_0"] > 0)
         and bool(right["tau_minus"] > 0) and bool(right["tau_plus"] < 1)
         and bool(right["f_at_1"] > 0), "independent right two-crossing chord")
    bs, Ps = bp(SWITCH, SWITCH)
    seam_left_bounds, seam_left = metric(-t - aq(RW), a, bs, Ps, RW)
    seam_right_bounds, seam_right = metric(-B, A, bs, Ps, RG)
    need(bool(seam_left["tau_minus"] > 0) and bool(seam_left["tau_minus"] < 1)
         and bool(seam_right["tau_minus"] > 0) and bool(seam_right["tau_plus"] < 1),
         "independent strict seam")

    c2 = K * SWITCH * SWITCH
    h2 = Q(1) - c2
    worst_t = T_DOMAIN[1]
    a2 = Q(1) - worst_t * worst_t
    shift = worst_t + RW
    outside = Q(1) + RW * worst_t
    square_gap = h2 * a2 - outside * outside - c2 * shift * shift
    unsquared_gap = square_gap * square_gap - 4 * outside * outside * shift * shift * c2
    need(square_gap == Q(5018751356871, 419430400000000)
         and unsquared_gap == Q(
             5670073442246922990910641,
             175921860444160000000000000000,
         ) and square_gap > 0 and unsquared_gap > 0,
         "independent exact left algebra")
    need(bool(a > aq(Q(997, 1000))) and bool(br > aq(Q(1, 20)))
         and bool(br < aq(Q(1, 16))) and bool(Pr > aq(Q(499, 500)))
         and bool(A > aq(Q(23141, 50000))) and bool(A < aq(Q(3039, 6400)))
         and bool(-B > aq(Q(468503, 1280000)))
         and bool(-B < aq(Q(1194731, 3200000)))
         and bool(right["forward_projection_ell"] > aq(Q(1536624827, 3200000000)))
         and bool(right["forward_projection_ell"] < aq(Q(25506731, 51200000)))
         and bool(right["signed_transverse"] > -aq(Q(5603399, 16000000)))
         and bool(right["signed_transverse"] < -aq(Q(214789247, 640000000)))
         and bool(right["f_at_0"] > aq(Q(541, 2500))),
         "independent rational right guards")

    theorem = candidate["result"]["two_witness_analytic_theorem"]
    need(theorem["finite_old_gap_root_subdivision_count"] == 0
         and theorem["global_witness_interval_box_count"] == 2,
         "global not finite-root proof")
    need(theorem["left_witness"]["closed_proof_domain"] == ["0", "13/16"]
         and theorem["left_witness"]["assigned_half_open_domain"] == "[0,13/16)"
         and theorem["left_witness"]["targets"] == {origin: "W[-1,0]" for origin in ORIGINS}
         and theorem["left_witness"]["interval_bounds"] == left_bounds,
         "candidate left witness")
    need(theorem["right_witness"]["closed_proof_domain"] == ["13/16", "1"]
         and theorem["right_witness"]["assigned_half_open_domain"] == "[13/16,1]"
         and theorem["right_witness"]["targets"] == G_TARGET
         and theorem["right_witness"]["interval_bounds"] == right_bounds
         and theorem["right_witness"]["strict_f_at_1_sign"] == "POSITIVE"
         and theorem["right_witness"]["old_f_at_1_negative_sufficient_condition_satisfied"] is False
         and theorem["right_witness"]["old_f_at_1_negative_condition_is_not_necessary"] is True,
         "candidate right chord witness")
    seam = theorem["switch_seam"]
    need(seam["r"] == "13/16" and seam["assignment_owner"] == "right_witness"
         and seam["left_closed_proof_strict_at_seam"] is True
         and seam["right_closed_proof_strict_at_seam"] is True
         and seam["assigned_domains_have_gap"] is False
         and seam["assigned_domains_have_overlap"] is False
         and seam["left_interval_bounds"] == seam_left_bounds
         and seam["right_interval_bounds"] == seam_right_bounds,
         "candidate half-open strict seam")
    language = theorem["witness_language"]
    need(language == {
        "kind": "PIECEWISE_TWO_WITNESS_GLOBAL_ANALYTIC_COVER",
        "single_uniform_witness_claimed": False,
        "north_south_target_reflection_verified": True,
        "every_r_in_closed_unit_interval_assigned_exactly_once": True,
        "both_closed_proof_domains_strict_at_shared_switch": True,
    }, "two-witness language")
    frozen_expected = {key: bounds(value) for key, value in frozen.items()}
    need(theorem["frozen_owner_global"]["interval_bounds"] == frozen_expected,
         "candidate frozen bounds")
    guards = theorem["analytic_rational_guards"]
    need(guards["left_monotone_endpoint"]["first_square_gap"] == str(square_gap)
         and guards["left_monotone_endpoint"]["unsquared_strict_gap"] == str(unsquared_gap)
         and guards["left_monotone_endpoint"]["both_gaps_strict_positive"] is True
         and guards["right_global_bounds"]["f_at_0_strict_lower"] == "541/2500"
         and guards["right_global_bounds"]["implied_chord"] == "0<tau_minus<tau_plus<1"
         and guards["proof_uses_global_monotonicity_and_interval_bounds"] is True
         and guards["proof_does_not_enumerate_twelve_gap_roots"] is True,
         "candidate rational guards")
    return {
        "global_interval_boxes": 2, "switch": "13/16",
        "frozen_ell_upper": str(frozen["forward_projection_ell"].upper()),
        "left_tau_minus_upper": str(left["tau_minus"].upper()),
        "right_tau_minus_lower": str(right["tau_minus"].lower()),
        "right_tau_plus_upper": str(right["tau_plus"].upper()),
        "right_f_at_1_lower": str(right["f_at_1"].lower()),
    }


def verify(path: Path) -> dict[str, Any]:
    need(hashlib.sha256(capture(PRODUCER)).hexdigest() == PRODUCER_SHA256,
         "producer byte pin")
    raw = capture(path)
    candidate = strict_json(raw, "candidate")
    need(raw == canonical(candidate) + b"\n", "canonical candidate bytes")
    need(set(candidate) == {"schema", "result", "result_sha256"}
         and candidate["schema"] == SCHEMA, "candidate envelope")
    need(candidate["result_sha256"] == digest(candidate["result"])
         == EXPECTED_RESULT_SHA256, "candidate frozen result closure")
    result = candidate["result"]
    need(result["status"] ==
         "PASS_11011101_NORTH_SOUTH_WHOLE_PAIR_GLOBAL_TWO_WITNESS_ANALYTIC_THEOREM__ZERO_FORMAL_CREDIT",
         "candidate status")
    audit = independently_audit_authority_and_roots(candidate)
    analytic = independently_verify_analytic(candidate)
    conclusion = result["whole_pair_research_conclusion"]
    need(conclusion["origin_keys"] == list(ORIGINS)
         and conclusion["per_origin_Round180_children"] == 539
         and conclusion["per_origin_P215_exact_behind_closed_children"] == 411
         and conclusion["per_origin_compact_q_residual_children_covered_by_global_theorem"] == 128
         and conclusion["formal_disposition_minted"] is False,
         "whole-pair conclusion")
    need(result["formal_boundary"] == {
        "CM2": "NO-GO_FOR_CLAIM", "D02": "BLOCKED_COMPOSITE",
        "D03": "UNAUTHORIZED", "D04": "NOT_MINTED", "Gate5": "10/18",
        "can_serve_as_compact_q_cohort_formal_predecessor": False,
        "compact_q_formal_remaining_origins": 54,
        "diagnostic_transition_authorized": False,
        "diagnostic_transition_only": "54 -> 52", "formal_credit": 0,
        "ledger_unchanged": True, "source_W_formal_remaining": 80,
        "terminal_gate_present": False,
        "uniform_formal_predecessor_authority": False,
    }, "exact formal boundary")
    return {"audit": audit, "analytic": analytic}


def main(argv: list[str]) -> int:
    try:
        need(len(argv) == 2, "usage: verifier CANDIDATE")
        reconstruction = verify(Path(argv[1]).absolute())
        output = {
            "schema": "cm2.round306c30q7.two-witness-independent-verification.v1",
            "status": "PASS_INDEPENDENT_GLOBAL_TWO_WITNESS_REBUILD__ZERO_FORMAL_CREDIT",
            "candidate_result_sha256": EXPECTED_RESULT_SHA256,
            "producer_sha256": PRODUCER_SHA256,
            "producer_imported_or_executed": False,
            "independent_reconstruction": reconstruction,
            "formal_credit": 0,
            "source_W_formal_remaining": 80,
            "compact_q_formal_remaining": 54,
            "can_serve_as_formal_predecessor": False,
        }
        sys.stdout.buffer.write(canonical(output) + b"\n")
        return 0
    except (OSError, KeyError, TypeError, ValueError, StopIteration, Reject) as error:
        sys.stderr.write("REJECT_C30Q7_VERIFY:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
