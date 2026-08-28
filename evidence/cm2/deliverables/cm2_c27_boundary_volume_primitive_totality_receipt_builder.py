#!/usr/bin/env python3
"""Seal the exact zero-credit blocker receipt for three support terminals."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
AUDIT = ROOT.parent / ".cm2-runtime" / "audit"
RUNS = [
    AUDIT / "c27-boundary-volume-primitive-totality-seed-30628111",
    AUDIT / "c27-boundary-volume-primitive-totality-seed-30628991",
]
ATTACK = AUDIT / "c27-boundary-volume-primitive-totality-attacks-v1" / "result.json"
OUTPUT = ROOT / "cm2_c27_boundary_volume_primitive_totality_unresolved_receipt.json"
PRODUCER = ROOT / "cm2_c27_boundary_volume_primitive_totality_probe.py"
ATTACK_SCRIPT = ROOT / "cm2_c27_boundary_volume_primitive_totality_attack_harness.py"
EXPECTED_PRODUCER_SHA256 = "cc2f29fc0b40017ffac6ef5010f422f52e148feb16aaa484746ffc954de10e1a"
EXPECTED_ATTACK_SCRIPT_SHA256 = "4f4be0e5b9b8235b93f0d8549ebabddf27711c1abf51ecafb79f91b54fe2759e"


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 * 1024 * 1024):
            state.update(block)
    return state.hexdigest()


def closed(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    need(raw.endswith(b"\n") and b"\n" not in raw[:-1], f"single JSON:{path}")
    value = json.loads(raw[:-1])
    need(type(value) is dict and canonical(value) + b"\n" == raw, f"canonical:{path}")
    body = dict(value)
    claimed = body.pop("result_sha256", None)
    need(type(claimed) is str and claimed == digest(body), f"closure:{path}")
    return value


def main() -> int:
    need(file_hash(PRODUCER) == EXPECTED_PRODUCER_SHA256, "producer pin")
    need(file_hash(ATTACK_SCRIPT) == EXPECTED_ATTACK_SCRIPT_SHA256, "attack script pin")
    for run in RUNS:
        need((Path(str(run) + ".exit")).read_text().strip() == "0", f"exit:{run.name}")
        need((Path(str(run) + ".stderr")).read_bytes() == b"", f"stderr:{run.name}")
        need((Path(str(run) + ".stdout")).read_bytes() == b"", f"stdout:{run.name}")
    need((RUNS[0] / "result.json").read_bytes() == (RUNS[1] / "result.json").read_bytes(),
         "double-seed result bytes")
    need((RUNS[0] / "half_open_endpoint_ownership_unresolved.jsonl.gz").read_bytes() ==
         (RUNS[1] / "half_open_endpoint_ownership_unresolved.jsonl.gz").read_bytes(),
         "double-seed unresolved ledger bytes")
    result = closed(RUNS[0] / "result.json")
    attack = closed(ATTACK)
    need(result["status"] ==
         "PASS_LOCAL_PRIMITIVE_CENSUS__REJECT_THREE_TERMINAL_TOTALITY_WITH_EXACT_MINIMAL_AUTHORITY_GAPS__ZERO_CREDIT",
         "truthful result status")
    need(result["primitive_atom_universe"]["atom_count"] == 483_232 and
         result["primitive_atom_universe"]["distinct_owner_member_count"] == 482_380,
         "primitive atom census")
    need(result["positive_volume_census"]["positive_coordinate_volume_atom_count"] == 483_232 and
         result["positive_volume_census"]["nonpositive_coordinate_volume_atom_count"] == 0,
         "positive-volume local geometry")
    need(result["boundary_face_census"]["geometric_oriented_face_count"] == 2_899_392 and
         result["boundary_face_census"]["half_open_endpoint_membership_unknown_face_count"] == 200_064,
         "boundary face census")
    need(result["minimal_missing_authority"]["half_open_endpoint_ownership"]["atom_count"] == 33_344 and
         result["minimal_missing_authority"]["three_terminal_selection"]["assigned_atom_count"] == 0,
         "minimal gaps")
    need(result["C26_audit"]["direct_boundary_or_volume_terminal_assignment_row_count"] == 0,
         "C26 terminal routing gap")
    need(attack["attack_count"] == 27 and attack["rejected_count"] == 27 and
         attack["all_rejected"] is True, "attacks")
    need(result["formal_credit"] == attack["formal_credit"] == 0 and
         result["C27_C28_C29"] == "REJECT" and result["CM2"] == "NO-GO_FOR_CLAIM",
         "strict nonpromotion")

    receipt = {
        "schema": "cm2.c27-independent.boundary-volume-primitive-totality-unresolved-receipt.v1",
        "C27_C28_C29": "REJECT",
        "CM2": "NO-GO_FOR_CLAIM",
        "attack_harness": {
            "all_rejected": True,
            "attack_count": 27,
            "result_file_sha256": file_hash(ATTACK),
            "result_object_sha256": attack["result_sha256"],
            "script_sha256": EXPECTED_ATTACK_SCRIPT_SHA256,
        },
        "double_seed": {
            "ledger_byte_identical": True,
            "result_byte_identical": True,
            "seeds": [30628111, 30628991],
        },
        "formal_credit": 0,
        "local_proved_geometry": {
            "positive_volume_atom_count": 483_232,
            "positive_area_oriented_face_count": 2_899_392,
        },
        "minimal_missing_authority": {
            "C19C_half_open_atom_count": 33_344,
            "endpoint_ownership_bit_count": 200_064,
            "C26_direct_three_terminal_assignment_row_count": 0,
            "three_terminal_unassigned_atom_count": 483_232,
            "unresolved_ledger_file_sha256": result["minimal_missing_authority"]["half_open_endpoint_ownership"]["ledger_file_sha256"],
            "unresolved_ledger_rows_sha256": result["minimal_missing_authority"]["half_open_endpoint_ownership"]["ledger_rows_sha256"],
        },
        "producer_sha256": EXPECTED_PRODUCER_SHA256,
        "result_file_sha256": file_hash(RUNS[0] / "result.json"),
        "result_object_sha256": result["result_sha256"],
        "status": "PASS_EXACT_BLOCKER_MATERIALIZATION__SIGNED_COMPLETE_POSITIVE_TERMINALS_REMAIN_OPEN__ZERO_CREDIT",
        "terminal_credit_counted": {
            "COMPLETE_BOUNDARY_FACES": False,
            "POSITIVE_VOLUME_CARRIERS": False,
            "SIGNED_BOUNDARY_FACES": False,
        },
    }
    receipt["receipt_sha256"] = digest(receipt)
    OUTPUT.write_bytes(canonical(receipt) + b"\n")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Failure as error:
        print(f"FAIL:{error}")
        raise SystemExit(2)
