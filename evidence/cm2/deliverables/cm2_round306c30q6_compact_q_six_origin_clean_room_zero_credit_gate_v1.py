#!/usr/bin/env python3
"""Clean-room census of the six analytically closed compact-q origins.

This program only consolidates pinned research evidence.  It deliberately
fails closed at the authority boundary: none of Q0/Q3/Q4/Q5 is a uniform
formal predecessor capable of changing the Round306C30b Source-W ledger.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any


sys.dont_write_bytecode = True
HERE = Path(__file__).absolute().parent
ROOT = HERE.parent
SCHEMA = "cm2.round306c30q6.compact-q-six-origin-clean-room-zero-credit-gate.v1"
ORIGINS = (
    "W:N:03.15.01111111",
    "W:N:03.15.11010101",
    "W:N:03.15.11010111",
    "W:S:H.03.15.01111111",
    "W:S:H.03.15.11010101",
    "W:S:H.03.15.11010111",
)

PATHS = {
    "c30b_manifest": "deliverables/cm2_round306c30b_source_w_outgoing_h_whole_origin_disposition_manifest.sha256",
    "c30b_result": "deliverables/cm2_round306c30b_sealed/cm2_round306c30b_source_w_outgoing_h_whole_origin_disposition_result.json",
    "c30b_verification": "deliverables/cm2_round306c30b_source_w_outgoing_h_whole_origin_disposition_verification.json",
    "q0_candidate": ".cm2-runtime/audit/c30q0-representative-analytic-v2-20260807T1021/stdout.json",
    "q0_verification": ".cm2-runtime/audit/c30q0-independent-v1-20260807T105735/verifier_stdout.json",
    "q0_attacks": ".cm2-runtime/audit/c30q0-independent-v1-20260807T105735/harness_stdout.json",
    "q1_seed_a": ".cm2-runtime/audit/c30q1-cohort-counterexample-v3-20260807T1205/seed30630071_stdout.json",
    "q1_seed_b": ".cm2-runtime/audit/c30q1-cohort-counterexample-v3-20260807T1205/seed30630929_stdout.json",
    "q2_seed_a": ".cm2-runtime/audit/c30q2-seven-cohort-routing-v3-20260807T1325/seed30630071_stdout.json",
    "q2_seed_b": ".cm2-runtime/audit/c30q2-seven-cohort-routing-v3-20260807T1325/seed30630929_stdout.json",
    "q3_manifest": ".cm2-runtime/audit/c30q3-south-theorem-zero-credit-v1-20260808T064505Z/manifest.sha256",
    "q3_receipt": ".cm2-runtime/audit/c30q3-south-theorem-zero-credit-v1-20260808T064505Z/receipt.json",
    "q3_candidate": ".cm2-runtime/audit/c30q3-south-theorem-zero-credit-v1-20260808T064505Z/seed30630071_producer_stdout.json",
    "q4_manifest": ".cm2-runtime/audit/c30q4-11010111-universal-containment-zero-credit-v1-20260808T070947Z/manifest.sha256",
    "q4_receipt": ".cm2-runtime/audit/c30q4-11010111-universal-containment-zero-credit-v1-20260808T070947Z/receipt.json",
    "q4_candidate": ".cm2-runtime/audit/c30q4-11010111-universal-containment-zero-credit-v1-20260808T070947Z/seed30630071_producer_stdout.json",
    "q5_manifest": ".cm2-runtime/audit/c30q5-11010101-clipped-graph-zero-credit-v1-20260808T075621Z/manifest.sha256",
    "q5_receipt": ".cm2-runtime/audit/c30q5-11010101-clipped-graph-zero-credit-v1-20260808T075621Z/receipt.json",
    "q5_candidate": ".cm2-runtime/audit/c30q5-11010101-clipped-graph-zero-credit-v1-20260808T075621Z/producer_seed30630071_stdout.json",
}

PINS = {
    "c30b_manifest": "6af636a4239f390712d057030f03e09fbbca332c6170f183d3d0095f19f0f248",
    "c30b_result": "b015e5bd6a4ee01d71ac95765d07dcbc63c3888f0c8ff9205e2d8c688958c11b",
    "c30b_verification": "e9e72536be9ba707fe2fdf6034b47978be4d09235e5133414ec7b0a31acf4e71",
    "q0_candidate": "bca0c9882db0fefe5fad65617c73418218330e8cdb651dbe04f8c64ff3725968",
    "q0_verification": "f1f257aab856a6bd8fd6a51650ec15fea5189147dde9ed0720db017ed546e72a",
    "q0_attacks": "fb16fa32796825abfe6e16e5a4666dac0b898254f4065765da610c4f323f589d",
    "q1_seed_a": "037e30eb015ab5c9eb802ecda7641144c4f6fd74b6db115c75aa0c7467793574",
    "q1_seed_b": "037e30eb015ab5c9eb802ecda7641144c4f6fd74b6db115c75aa0c7467793574",
    "q2_seed_a": "a3af728ac34b07ad86f9045c28bc3eabe88ea446e051cbe37b26d3baa270637b",
    "q2_seed_b": "a3af728ac34b07ad86f9045c28bc3eabe88ea446e051cbe37b26d3baa270637b",
    "q3_manifest": "fb479b15280a3027f702896470475b0cb3c16a0970d70f6dbfcde5964aa646df",
    "q3_receipt": "1df7d32921c08ab950c479bee8b6914aeb08468a4840a5664c662acfcbedd9e8",
    "q3_candidate": "7347dfb7d578a4564909ae0214527b5cb0ac682981d7f5f12f9a35eb95eeaa59",
    "q4_manifest": "29c1616561a43ee77a1407d039a89f8a4a064b9d57b8674ca1bca6ab86a6ae5f",
    "q4_receipt": "99a7db9356768e08678950585c2d1eb32236a36949e0c8551a0d344406ea6af6",
    "q4_candidate": "1ca9aba6ce58beea20d662a7c669f6a14aee98df1938a67eca39c5654213d230",
    "q5_manifest": "452590a90f53607647949e73177aa010c7961dfae53e37f5d6d0eb6bd2fee5e3",
    "q5_receipt": "cdebf9a357de0de2612f6b8493d0c56c2a703fd25423967ba771cea12224cc79",
    "q5_candidate": "ac8043dc1945ddb5d4926712b5caab6478e4abe9eec67a37f4cd2a0b218c6e01",
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
    need(absolute.resolve(strict=True) == absolute, "canonical input path:" + str(path))
    before = os.lstat(absolute)
    need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
         "regular single-link input:" + str(path))
    raw = absolute.read_bytes()
    after = os.lstat(absolute)
    fields = ("st_dev", "st_ino", "st_mode", "st_nlink", "st_size",
              "st_mtime_ns", "st_ctime_ns", "st_uid", "st_gid")
    need(all(getattr(before, key) == getattr(after, key) for key in fields),
         "stable input capture:" + str(path))
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


def pinned(name: str) -> bytes:
    raw = capture(ROOT / PATHS[name])
    need(hashlib.sha256(raw).hexdigest() == PINS[name], "pin:" + name)
    return raw


def document(name: str) -> dict[str, Any]:
    return strict_json(pinned(name), name)


def verify_manifest(name: str, base: Path) -> int:
    raw = pinned(name)
    rows = raw.decode("ascii", "strict").splitlines()
    seen: set[str] = set()
    for row in rows:
        need(len(row) >= 67 and row[64:66] == "  ", "manifest row:" + name)
        expected, relative = row[:64], row[66:]
        need(all(char in "0123456789abcdef" for char in expected),
             "manifest digest:" + name)
        part = Path(relative)
        need(not part.is_absolute() and ".." not in part.parts and relative not in seen,
             "manifest path:" + name)
        seen.add(relative)
        workspace_candidate = ROOT / part
        target = workspace_candidate if workspace_candidate.exists() else base / part
        need(target.absolute().is_relative_to(ROOT), "manifest member scope:" + name)
        actual = hashlib.sha256(capture(target)).hexdigest()
        need(actual == expected, "manifest member:" + name + ":" + relative)
    need(bool(rows), "nonempty manifest:" + name)
    return len(rows)


def legacy_controls(directory: Path, prefix: str, stderr_sha256: str | None = None) -> None:
    need(capture(directory / "pre.sha256") == capture(directory / "post.sha256"),
         prefix + " pre/post SHA")
    need(capture(directory / "pre.stat") == capture(directory / "post.stat"),
         prefix + " pre/post stat")
    for item in directory.glob("*_exit_code.txt"):
        need(capture(item) == b"0\n", prefix + " numeric exit:" + item.name)
    stderr_rows = sorted(directory.glob("*_stderr.log"))
    for item in stderr_rows:
        raw = capture(item)
        if stderr_sha256 is None:
            need(raw == b"", prefix + " empty stderr:" + item.name)
        else:
            need(hashlib.sha256(raw).hexdigest() == stderr_sha256,
                 prefix + " declared deterministic stderr:" + item.name)


def build() -> dict[str, Any]:
    c30b_members = verify_manifest("c30b_manifest", ROOT / "deliverables")
    q3_members = verify_manifest("q3_manifest", (ROOT / PATHS["q3_manifest"]).parent)
    q4_members = verify_manifest("q4_manifest", (ROOT / PATHS["q4_manifest"]).parent)
    q5_members = verify_manifest("q5_manifest", (ROOT / PATHS["q5_manifest"]).parent)

    c30b = document("c30b_result")
    c30b_verification = document("c30b_verification")
    need(c30b["status"] == "PASS_BOUNDED_ROUND306C30B_OUTGOING_H_DISPOSITION",
         "C30b result status")
    need(c30b_verification["status"] ==
         "PASS_FORMAL_C30B__688_H_CELLS__2_WHOLE_ORIGIN_EXCLUSIONS__10_RESOLVED_MIXED__SOURCE_W_92_TO_80__D02_STILL_BLOCKED",
         "C30b verification status")
    after = c30b["source_W_ledger_transition"]["after"]
    need(after["remaining"] == 80 and after["remaining_partition"]["compact_q"] == 54,
         "C30b formal remaining")
    need(after["excluded"] + after["conservative_live"] == 76832,
         "C30b conservation")

    q0_dir = ROOT / ".cm2-runtime/audit/c30q0-independent-v1-20260807T105735"
    legacy_controls(q0_dir, "Q0")
    q0 = document("q0_candidate")
    q0v = document("q0_verification")
    q0a = document("q0_attacks")
    need(q0["result"]["status"] ==
         "PASS_REPRESENTATIVE_COMPACT_Q_WHOLE_ORIGIN_ANALYTIC_THEOREM__ZERO_FORMAL_CREDIT",
         "Q0 theorem status")
    need(q0v["independent_reconstruction"]["origin_key"] == ORIGINS[0]
         and q0v["independent_reconstruction"]["root_box_count"] == 16
         and q0v["independent_reconstruction"]["atomic_stratum_count"] == 255,
         "Q0 independent reconstruction")
    need(q0a["status"].startswith("PASS_20_OF_20_COHERENT_NEGATIVE_ATTACKS_REJECTED"),
         "Q0 attacks")

    q1_dir = ROOT / ".cm2-runtime/audit/c30q1-cohort-counterexample-v3-20260807T1205"
    q2_dir = ROOT / ".cm2-runtime/audit/c30q2-seven-cohort-routing-v3-20260807T1325"
    legacy_stderr = "91b2592bdb84c39a0fde3fadc2bea4ce734e617170956375cfab989b4dc092c6"
    legacy_controls(q1_dir, "Q1", legacy_stderr)
    legacy_controls(q2_dir, "Q2", legacy_stderr)
    q1a, q1b = document("q1_seed_a"), document("q1_seed_b")
    q2a, q2b = document("q2_seed_a"), document("q2_seed_b")
    need(canonical(q1a) == canonical(q1b) and canonical(q2a) == canonical(q2b),
         "Q1/Q2 dual-seed equality")
    need(q1a["result"]["status"].startswith("REJECT_AUTOMATIC_REPRESENTATIVE_CERTIFICATE_EXTENSION"),
         "Q1 counterexample boundary")
    need(q2a["result"]["status"] ==
         "PASS_EXACT_SEVEN_COHORT_ROUTING_LEDGER__REJECT_AUTOMATIC_EXTENSION__ZERO_FORMAL_CREDIT",
         "Q2 routing status")
    ledger = q2a["result"]["exact_seven_cohort_ledger"]
    need(ledger["totals"] == {
        "applicable_root_count": 104,
        "final_combined_pass_origin_count": 2,
        "fully_analytic_origin_count": 6,
        "origin_count": 54,
        "root_count": 844,
    }, "Q2 totals")
    fully = [row for row in ledger["patterns"]
             if row["pattern"]["applicable_root_count_per_origin"] == 16]
    need(len(fully) == 1 and tuple(fully[0]["origin_keys"]) == ORIGINS,
         "Q2 exact six-origin cohort")

    q3r, q3 = document("q3_receipt"), document("q3_candidate")
    need(q3r["status"] == "PASS_ZERO_CREDIT_RESEARCH_RECEIPT"
         and q3r["formal_boundary"]["seal_or_release_authority"] is False
         and q3r["theorem"]["origin_key"] == ORIGINS[3]
         and q3r["theorem"]["root_count"] == 16,
         "Q3 research receipt")
    need(q3["result"]["selected_origin"]["origin_key"] == ORIGINS[3],
         "Q3 origin")

    q4r, q4 = document("q4_receipt"), document("q4_candidate")
    need(q4r["status"] ==
         "PASS_RECOVERED_ZERO_CREDIT_RECEIPT_WITH_DECLARED_CONTROL_PARSE_FAILURE"
         and q4r["formal_boundary"]["seal_or_release_authority"] is False
         and q4r["control_history"]["initial_wrapper_exit_code"] == 2
         and q4r["producer"]["stderr_size_bytes"] == 43,
         "Q4 truthful recovered research receipt")
    q4_rows = q4["result"]["universal_residual_containment"]["origin_rows"]
    need(tuple(sorted(row["origin_key"] for row in q4_rows)) ==
         tuple(sorted((ORIGINS[2], ORIGINS[5])))
         and all(row["analytic_residual_child_count"] == 128 for row in q4_rows),
         "Q4 two-origin closure")

    q5r, q5 = document("q5_receipt"), document("q5_candidate")
    need(q5r["status"] ==
         "PASS_C30Q5_DUAL_SEED_COLD_REPLAY_AND_ATTACKS__ZERO_CREDIT"
         and q5r["strict_nonpromotion"]["formal_credit"] == 0
         and q5r["strict_nonpromotion"]["compact_q_formal_remaining_origins"] == 54,
         "Q5 research receipt")
    q5_rows = q5["result"]["universal_residual_containment"]["origin_rows"]
    need(tuple(sorted(row["origin_key"] for row in q5_rows)) ==
         tuple(sorted((ORIGINS[1], ORIGINS[4])))
         and all(row["residual_category_count"] == {
             "CLIPPED_OR_FACE_OVERWRAP_SINGLE_DISCRIMINANT_GRAPH": 8,
             "SOURCE_GRAZING_COMPACT_Q_RESIDUAL": 128,
         } for row in q5_rows), "Q5 two-origin closure")

    evidence = {
        ORIGINS[0]: {"closure": "Q0_NORTH_WHOLE_ORIGIN_THEOREM",
                     "roots": 16, "atomic_strata": 255,
                     "authority_class": "LEGACY_VALIDATED_RESEARCH_RUN_NO_ROOT_RECEIPT"},
        ORIGINS[1]: {"closure": "Q5_CLIPPED_GRAPH_AND_UNIVERSAL_CONTAINMENT",
                     "roots": 16, "residuals": 136,
                     "authority_class": "ZERO_CREDIT_RESEARCH_RECEIPT"},
        ORIGINS[2]: {"closure": "Q4_UNIVERSAL_CONTAINMENT",
                     "roots": 16, "residuals": 128,
                     "authority_class": "RECOVERED_ZERO_CREDIT_RESEARCH_RECEIPT"},
        ORIGINS[3]: {"closure": "Q3_SOUTH_WHOLE_ORIGIN_THEOREM",
                     "roots": 16, "atomic_strata": 255,
                     "authority_class": "ZERO_CREDIT_RESEARCH_RECEIPT"},
        ORIGINS[4]: {"closure": "Q5_CLIPPED_GRAPH_AND_UNIVERSAL_CONTAINMENT",
                     "roots": 16, "residuals": 136,
                     "authority_class": "ZERO_CREDIT_RESEARCH_RECEIPT"},
        ORIGINS[5]: {"closure": "Q4_UNIVERSAL_CONTAINMENT",
                     "roots": 16, "residuals": 128,
                     "authority_class": "RECOVERED_ZERO_CREDIT_RESEARCH_RECEIPT"},
    }
    return {
        "status": "PASS_SIX_ORIGIN_RESEARCH_CLOSURE__FAIL_CLOSED_NO_UNIFORM_PREDECESSOR__ZERO_CREDIT",
        "verdict": "RESEARCH_CENSUS_PASS__FORMAL_TRANSITION_REJECTED",
        "formal_predecessor": {
            "round": "Round306C30b",
            "manifest_sha256": PINS["c30b_manifest"],
            "manifest_member_count": c30b_members,
            "source_W_formal_remaining": 80,
            "compact_q_formal_remaining": 54,
        },
        "historic_routing_boundary": {
            "Q1_automatic_extension_rejected": True,
            "Q2_origin_count": 54,
            "Q2_root_count": 844,
            "Q2_fully_analytic_origin_count": 6,
            "Q2_six_origin_keys_sha256": fully[0]["origin_keys_sha256"],
        },
        "six_origin_research_closure": {
            "origin_count": 6,
            "origin_keys": list(ORIGINS),
            "origin_evidence": evidence,
            "all_six_research_closed": True,
            "uniform_formal_predecessor_authority": False,
        },
        "upstream_manifest_closure": {
            "Q3_members": q3_members,
            "Q4_members": q4_members,
            "Q5_members": q5_members,
        },
        "authority_fail_closed": {
            "formal_transition_requested_for_diagnostic_only": "54 -> 48",
            "formal_transition_authorized": False,
            "blocking_reasons": [
                "Q0 North is a legacy validated research run without a durable root receipt",
                "Q3 explicitly declares seal_or_release_authority=false",
                "Q4 is a recovered research receipt with original wrapper exit 2 and producer stderr nonempty",
                "Q5 explicitly grants zero formal credit",
                "Q1 and Q2 explicitly reject automatic cohort promotion",
                "no C30c->C30d->C30e->C30f terminal predecessor chain is supplied",
            ],
        },
        "strict_nonpromotion": {
            "formal_credit": 0,
            "ledger_unchanged": True,
            "source_W_formal_remaining": 80,
            "compact_q_formal_remaining_origins": 54,
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
    except (OSError, KeyError, TypeError, Reject) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
