#!/usr/bin/env python3
"""No-import independent verifier for the C30q6 zero-credit census."""

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
PRODUCER = HERE / "cm2_round306c30q6_compact_q_six_origin_clean_room_zero_credit_gate_v1.py"
PRODUCER_SHA256 = "3f9eeaf6043d7247d7f493a58aef7e384388b9936988fd32b58934e0407f9890"
SCHEMA = "cm2.round306c30q6.compact-q-six-origin-clean-room-zero-credit-gate.v1"
RESULT_SHA256 = "dcfc1a34d79ddee0024bfe27818d90bee604ea087552b89bd13ef36b31e67d5b"
ORIGINS = (
    "W:N:03.15.01111111",
    "W:N:03.15.11010101",
    "W:N:03.15.11010111",
    "W:S:H.03.15.01111111",
    "W:S:H.03.15.11010101",
    "W:S:H.03.15.11010111",
)

INPUTS = {
    "c30b_manifest": ("deliverables/cm2_round306c30b_source_w_outgoing_h_whole_origin_disposition_manifest.sha256", "6af636a4239f390712d057030f03e09fbbca332c6170f183d3d0095f19f0f248"),
    "c30b_result": ("deliverables/cm2_round306c30b_sealed/cm2_round306c30b_source_w_outgoing_h_whole_origin_disposition_result.json", "b015e5bd6a4ee01d71ac95765d07dcbc63c3888f0c8ff9205e2d8c688958c11b"),
    "q0_verification": (".cm2-runtime/audit/c30q0-independent-v1-20260807T105735/verifier_stdout.json", "f1f257aab856a6bd8fd6a51650ec15fea5189147dde9ed0720db017ed546e72a"),
    "q0_attacks": (".cm2-runtime/audit/c30q0-independent-v1-20260807T105735/harness_stdout.json", "fb16fa32796825abfe6e16e5a4666dac0b898254f4065765da610c4f323f589d"),
    "q1": (".cm2-runtime/audit/c30q1-cohort-counterexample-v3-20260807T1205/seed30630071_stdout.json", "037e30eb015ab5c9eb802ecda7641144c4f6fd74b6db115c75aa0c7467793574"),
    "q2": (".cm2-runtime/audit/c30q2-seven-cohort-routing-v3-20260807T1325/seed30630071_stdout.json", "a3af728ac34b07ad86f9045c28bc3eabe88ea446e051cbe37b26d3baa270637b"),
    "q3_manifest": (".cm2-runtime/audit/c30q3-south-theorem-zero-credit-v1-20260808T064505Z/manifest.sha256", "fb479b15280a3027f702896470475b0cb3c16a0970d70f6dbfcde5964aa646df"),
    "q3_receipt": (".cm2-runtime/audit/c30q3-south-theorem-zero-credit-v1-20260808T064505Z/receipt.json", "1df7d32921c08ab950c479bee8b6914aeb08468a4840a5664c662acfcbedd9e8"),
    "q4_manifest": (".cm2-runtime/audit/c30q4-11010111-universal-containment-zero-credit-v1-20260808T070947Z/manifest.sha256", "29c1616561a43ee77a1407d039a89f8a4a064b9d57b8674ca1bca6ab86a6ae5f"),
    "q4_receipt": (".cm2-runtime/audit/c30q4-11010111-universal-containment-zero-credit-v1-20260808T070947Z/receipt.json", "99a7db9356768e08678950585c2d1eb32236a36949e0c8551a0d344406ea6af6"),
    "q4_candidate": (".cm2-runtime/audit/c30q4-11010111-universal-containment-zero-credit-v1-20260808T070947Z/seed30630071_producer_stdout.json", "1ca9aba6ce58beea20d662a7c669f6a14aee98df1938a67eca39c5654213d230"),
    "q5_manifest": (".cm2-runtime/audit/c30q5-11010101-clipped-graph-zero-credit-v1-20260808T075621Z/manifest.sha256", "452590a90f53607647949e73177aa010c7961dfae53e37f5d6d0eb6bd2fee5e3"),
    "q5_receipt": (".cm2-runtime/audit/c30q5-11010101-clipped-graph-zero-credit-v1-20260808T075621Z/receipt.json", "cdebf9a357de0de2612f6b8493d0c56c2a703fd25423967ba771cea12224cc79"),
    "q5_candidate": (".cm2-runtime/audit/c30q5-11010101-clipped-graph-zero-credit-v1-20260808T075621Z/producer_seed30630071_stdout.json", "ac8043dc1945ddb5d4926712b5caab6478e4abe9eec67a37f4cd2a0b218c6e01"),
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


def stable(path: Path) -> bytes:
    path = path.absolute()
    need(path.resolve(strict=True) == path, "canonical path")
    before = os.lstat(path)
    need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "regular input")
    raw = path.read_bytes()
    after = os.lstat(path)
    names = ("st_dev", "st_ino", "st_mode", "st_nlink", "st_size",
             "st_mtime_ns", "st_ctime_ns", "st_uid", "st_gid")
    need(all(getattr(before, name) == getattr(after, name) for name in names),
         "stable input")
    return raw


def parse(raw: bytes, label: str, canonical_required: bool = False) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for key, value in pairs:
            need(key not in output, "duplicate key:" + label)
            output[key] = value
        return output
    try:
        value = json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=unique,
                           parse_float=lambda token: token,
                           parse_constant=lambda token: (_ for _ in ()).throw(ValueError(token)))
    except (UnicodeDecodeError, ValueError, json.JSONDecodeError) as error:
        raise Reject("strict JSON:" + label) from error
    need(type(value) is dict, "object:" + label)
    if canonical_required:
        need(raw == canonical(value) + b"\n", "canonical candidate")
    return value


def read_input(name: str) -> bytes:
    relative, expected = INPUTS[name]
    raw = stable(ROOT / relative)
    need(hashlib.sha256(raw).hexdigest() == expected, "input pin:" + name)
    return raw


def doc(name: str) -> dict[str, Any]:
    return parse(read_input(name), name)


def manifest_count(name: str, base: Path) -> int:
    rows = read_input(name).decode("ascii", "strict").splitlines()
    seen: set[str] = set()
    for row in rows:
        need(len(row) >= 67 and row[64:66] == "  ", "manifest row")
        expected, relative = row[:64], row[66:]
        need(len(expected) == 64 and all(c in "0123456789abcdef" for c in expected),
             "manifest hash")
        part = Path(relative)
        need(not part.is_absolute() and ".." not in part.parts and relative not in seen,
             "manifest path")
        seen.add(relative)
        workspace = ROOT / part
        target = workspace if workspace.exists() else base / part
        need(target.absolute().is_relative_to(ROOT), "manifest scope")
        need(hashlib.sha256(stable(target)).hexdigest() == expected,
             "manifest member:" + relative)
    need(bool(rows), "manifest nonempty")
    return len(rows)


def verify(candidate_path: Path) -> dict[str, Any]:
    need(hashlib.sha256(stable(PRODUCER)).hexdigest() == PRODUCER_SHA256,
         "producer source pin")
    raw = stable(candidate_path)
    candidate = parse(raw, "candidate", True)
    need(set(candidate) == {"schema", "result", "result_sha256"}, "candidate keys")
    need(candidate["schema"] == SCHEMA, "candidate schema")
    result = candidate["result"]
    need(type(result) is dict and digest(result) == candidate["result_sha256"] == RESULT_SHA256,
         "candidate result closure")

    c30b_count = manifest_count("c30b_manifest", ROOT / "deliverables")
    q3_count = manifest_count("q3_manifest", (ROOT / INPUTS["q3_manifest"][0]).parent)
    q4_count = manifest_count("q4_manifest", (ROOT / INPUTS["q4_manifest"][0]).parent)
    q5_count = manifest_count("q5_manifest", (ROOT / INPUTS["q5_manifest"][0]).parent)
    c30b = doc("c30b_result")
    after = c30b["source_W_ledger_transition"]["after"]
    need(after["remaining"] == 80 and after["remaining_partition"]["compact_q"] == 54,
         "formal predecessor state")

    q0v, q0a = doc("q0_verification"), doc("q0_attacks")
    need(q0v["independent_reconstruction"]["origin_key"] == ORIGINS[0]
         and q0v["formal_credit"] == 0
         and q0a["status"].startswith("PASS_20_OF_20_"), "Q0 research evidence")
    q1, q2 = doc("q1"), doc("q2")
    need(q1["result"]["strict_nonpromotion"]["no_seal_or_release_authority"] is True,
         "Q1 no authority")
    patterns = q2["result"]["exact_seven_cohort_ledger"]["patterns"]
    fully = [row for row in patterns
             if row["pattern"]["applicable_root_count_per_origin"] == 16]
    need(len(fully) == 1 and tuple(fully[0]["origin_keys"]) == ORIGINS,
         "Q2 six origin derivation")

    q3 = doc("q3_receipt")
    q4, q4c = doc("q4_receipt"), doc("q4_candidate")
    q5, q5c = doc("q5_receipt"), doc("q5_candidate")
    need(q3["formal_boundary"]["seal_or_release_authority"] is False
         and q3["theorem"]["origin_key"] == ORIGINS[3], "Q3 boundary")
    need(q4["control_history"]["initial_wrapper_exit_code"] == 2
         and q4["producer"]["stderr_size_bytes"] == 43
         and q4["formal_boundary"]["seal_or_release_authority"] is False,
         "Q4 boundary")
    q4_keys = sorted(row["origin_key"] for row in
                     q4c["result"]["universal_residual_containment"]["origin_rows"])
    need(q4_keys == sorted((ORIGINS[2], ORIGINS[5])), "Q4 origin keys")
    need(q5["strict_nonpromotion"]["formal_credit"] == 0
         and q5["strict_nonpromotion"]["ledger_unchanged"] is True,
         "Q5 boundary")
    q5_keys = sorted(row["origin_key"] for row in
                     q5c["result"]["universal_residual_containment"]["origin_rows"])
    need(q5_keys == sorted((ORIGINS[1], ORIGINS[4])), "Q5 origin keys")

    need(result["status"] ==
         "PASS_SIX_ORIGIN_RESEARCH_CLOSURE__FAIL_CLOSED_NO_UNIFORM_PREDECESSOR__ZERO_CREDIT",
         "result status")
    closure = result["six_origin_research_closure"]
    need(closure["origin_count"] == 6 and tuple(closure["origin_keys"]) == ORIGINS
         and closure["all_six_research_closed"] is True
         and closure["uniform_formal_predecessor_authority"] is False,
         "six origin closure boundary")
    fail = result["authority_fail_closed"]
    need(fail["formal_transition_requested_for_diagnostic_only"] == "54 -> 48"
         and fail["formal_transition_authorized"] is False
         and len(fail["blocking_reasons"]) == 6,
         "fail-closed authority")
    strict = result["strict_nonpromotion"]
    need(strict == {
        "CM2": "NO-GO_FOR_CLAIM", "D02": "BLOCKED_COMPOSITE",
        "D03": "UNAUTHORIZED", "D04": "NOT_MINTED", "Gate5": "10/18",
        "compact_q_formal_remaining_origins": 54, "formal_credit": 0,
        "ledger_unchanged": True, "source_W_formal_remaining": 80,
    }, "strict nonpromotion")
    need(result["formal_predecessor"]["manifest_member_count"] == c30b_count
         and result["upstream_manifest_closure"] == {
             "Q3_members": q3_count, "Q4_members": q4_count, "Q5_members": q5_count,
         }, "manifest counts")
    return {
        "schema": "cm2.round306c30q6.compact-q-six-origin-clean-room-zero-credit-independent-verification.v1",
        "status": "PASS_INDEPENDENT_C30Q6_SIX_RESEARCH_ORIGINS__FORMAL_54_TO_48_REJECTED",
        "candidate_sha256": hashlib.sha256(raw).hexdigest(),
        "candidate_result_sha256": RESULT_SHA256,
        "origin_count": 6,
        "origin_keys_sha256": digest(list(ORIGINS)),
        "all_upstream_manifests_replayed": True,
        "producer_imported_or_executed": False,
        "uniform_formal_predecessor_authority": False,
        "formal_credit": 0,
        "source_W_formal_remaining": 80,
        "compact_q_formal_remaining": 54,
        "CM2": "NO-GO_FOR_CLAIM",
    }


def main(argv: list[str]) -> int:
    try:
        need(len(argv) == 2, "usage")
        output = verify(Path(argv[1]))
        sys.stdout.buffer.write(canonical(output) + b"\n")
        return 0
    except (OSError, KeyError, TypeError, Reject) as error:
        sys.stderr.write("REJECT:" + str(error) + "\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
