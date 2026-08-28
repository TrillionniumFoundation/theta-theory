#!/usr/bin/env python3
"""Build the append-only v4 receipt for the primitive 20-terminal audit gate.

This builder is deliberately non-promotional.  It verifies two complete
producer/verifier/attack executions, independently pins the decisive local
receipts, and records the only admissible aggregate conclusion: sixteen
evidence-level terminals closed, four totality obligations open, and the old
C27--C29 semantic authority invalidated by confirmed legal witnesses.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent
AUDIT = WORKSPACE / ".cm2-runtime" / "audit"

PRODUCER = ROOT / "cm2_c27_primitive_twenty_family_partition_gate.py"
VERIFIER = ROOT / "cm2_c27_primitive_twenty_family_partition_independent_verifier.py"
ATTACK = ROOT / "cm2_c27_primitive_twenty_family_partition_attack_harness.py"

SOURCE_PINS = {
    PRODUCER: "1c1128f3dcbfacd1757d087d9adc561e37085f18b85acd0393e1950a887a4f89",
    VERIFIER: "743889d2b4b985f66bb2d3e3151f658a969b33f7a93fd7a9fd0ee5c751e76e17",
    ATTACK: "c54d7b5bd74090507190e864ecc26b802943a43314c476abe2bf5327dcfc263d",
}

RUN_LABELS = (30630401, 30630901)
PRODUCER_DIRS = {
    label: AUDIT / f"c27-primitive-20-terminal-v4-seed-{label}"
    for label in RUN_LABELS
}
VERIFIER_DIRS = {
    label: AUDIT / f"c27-primitive-20-terminal-v4-verifier-resume-seed-{label}"
    for label in RUN_LABELS
}
ATTACK_DIRS = {
    label: AUDIT / f"c27-primitive-20-terminal-v4-attacks-seed-{label}"
    for label in RUN_LABELS
}

CANDIDATE_FILE_SHA256 = "9620709f965bab0f3d6728d35d4f57123600ddcde6e6763bdbe4e4b3c1f00c3d"
VERIFICATION_FILE_SHA256 = "d0bfa30f1a9c9310272fc2990571567b26f21456ff0fc214a7153719a6e8e675"
ATTACK_FILE_SHA256 = "05b43085480791d79799b3ccb5fc87a2b08765c9f4ef8f91f0a8f60605b26ded"
CANDIDATE_OBJECT_SHA256 = "43f776d34e1413ff480b0f6eb9eefc6b05c7329c6ab7e3273a0f5e043e0848d4"

OWNER = ROOT / "cm2_c27_sheet_owner_shadow_physical_totality_subgate_receipt.json"
SAME_DIRECT = ROOT / "cm2_c27_same_chart_exact_equal_cross_component_final_receipt_v2.json"
SAME_CROSS = (
    AUDIT
    / "c27-same-chart-witness-cross-implementation-comparator-20260807T2319"
    / "cm2_c27_same_chart_witness_cross_implementation_zero_credit_receipt.json"
)
BOUNDARY = ROOT / "cm2_c27_boundary_volume_primitive_totality_unresolved_receipt.json"
OVERLAY = AUDIT / "c27r1bc-provisional-overlay-v2-final-receipt.json"

EVIDENCE_PINS = {
    OWNER: ("2833cc5f1c9d35eeca36722dfb348ad16e9d09e8d44d8983e63b61f390a93d0f", "receipt_sha256"),
    SAME_DIRECT: ("bb58cfb7a8929e322c81b8be617a184f523da862cb4d3f4c260acd80a4ba9969", "receipt_sha256"),
    SAME_CROSS: ("e4bdb0ca3f594602b61efa218ef3efe62ef048638ba618a443110c66c905eaf1", "receipt_sha256"),
    BOUNDARY: ("772bdcc750a44400342005c14230e2ea26fdf01c2d92244611ba6f66817689b7", "receipt_sha256"),
    OVERLAY: ("cd05b9c1260bc037f38ff5edde22c635a1dc40fe5dff3d10a632b453361ac6de", "receipt_object_sha256"),
}

EXPECTED_OPEN = [
    "SAME_CHART_RELATIVE_CELLS",
    "SIGNED_BOUNDARY_FACES",
    "COMPLETE_BOUNDARY_FACES",
    "POSITIVE_VOLUME_CARRIERS",
]


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_hash(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 * 1024 * 1024):
            state.update(block)
    return state.hexdigest()


def canonical_object(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    payload = raw[:-1] if raw.endswith(b"\n") else raw
    need(payload != b"" and b"\n" not in payload, f"single JSON object:{path}")
    value = json.loads(payload)
    need(type(value) is dict and canonical(value) == payload, f"canonical JSON:{path}")
    return value


def closed_object(path: Path, field: str) -> dict[str, Any]:
    value = canonical_object(path)
    body = dict(value)
    claimed = body.pop(field, None)
    need(type(claimed) is str and claimed == digest(body), f"object closure:{path}")
    return value


def read_exit(path: Path) -> int:
    raw = path.read_text(encoding="ascii")
    need(raw.endswith("\n") and raw[:-1] in {"0", "2"}, f"numeric exit:{path}")
    return int(raw[:-1])


def read_time_status(path: Path) -> int:
    lines = [line for line in path.read_text(encoding="ascii").splitlines() if line]
    need(bool(lines), f"time receipt:{path}")
    value = json.loads(lines[-1])
    need(type(value) is dict, f"time object:{path}")
    status = value.get("time_exit_status")
    need(type(status) is int and status in {0, 2}, f"time exit status:{path}")
    need(type(value.get("elapsed_seconds")) in {int, float}, f"elapsed seconds:{path}")
    need(type(value.get("maximum_resident_kb")) is int, f"maximum resident:{path}")
    return status


def validate_runs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    candidates: list[bytes] = []
    verifications: list[bytes] = []
    attacks: list[bytes] = []
    run_receipts: dict[str, Any] = {}

    for label in RUN_LABELS:
        producer_dir = PRODUCER_DIRS[label]
        verifier_dir = VERIFIER_DIRS[label]
        attack_dir = ATTACK_DIRS[label]

        candidate_path = producer_dir / "candidate.json"
        verification_path = verifier_dir / "verification.json"
        attack_path = attack_dir / "attack.json"

        need(read_exit(producer_dir / "producer.exit") == 2, f"producer truthful-reject exit:{label}")
        need((producer_dir / "producer.stderr").read_bytes() == b"", f"producer stderr empty:{label}")
        need(read_time_status(producer_dir / "producer.time.json") == 2, f"producer time exit:{label}")
        need(read_exit(verifier_dir / "exit_code.txt") == 0, f"verifier exit:{label}")
        need((verifier_dir / "stderr.txt").read_bytes() == b"", f"verifier stderr empty:{label}")
        need(read_time_status(verifier_dir / "time.json") == 0, f"verifier time exit:{label}")
        need(read_exit(attack_dir / "exit_code.txt") == 0, f"attack exit:{label}")
        need((attack_dir / "stderr.txt").read_bytes() == b"", f"attack stderr empty:{label}")
        need(read_time_status(attack_dir / "time.json") == 0, f"attack time exit:{label}")

        need(file_hash(candidate_path) == CANDIDATE_FILE_SHA256, f"candidate file pin:{label}")
        need(file_hash(verification_path) == VERIFICATION_FILE_SHA256, f"verification file pin:{label}")
        need(file_hash(attack_path) == ATTACK_FILE_SHA256, f"attack file pin:{label}")
        candidates.append(candidate_path.read_bytes())
        verifications.append(verification_path.read_bytes())
        attacks.append(attack_path.read_bytes())
        run_receipts[str(label)] = {
            "producer": {"numeric_exit": 2, "stderr_empty": True, "time_exit_status": 2},
            "verifier": {"numeric_exit": 0, "stderr_empty": True, "time_exit_status": 0},
            "attack": {"numeric_exit": 0, "stderr_empty": True, "time_exit_status": 0},
        }

    need(candidates[0] == candidates[1], "producer duplicate-run candidate bytes")
    need(verifications[0] == verifications[1], "verifier duplicate-run bytes")
    need(attacks[0] == attacks[1], "attack duplicate-run bytes")

    candidate = closed_object(PRODUCER_DIRS[RUN_LABELS[0]] / "candidate.json", "result_sha256")
    verification = canonical_object(VERIFIER_DIRS[RUN_LABELS[0]] / "verification.json")
    attack = canonical_object(ATTACK_DIRS[RUN_LABELS[0]] / "attack.json")

    need(candidate["result_sha256"] == CANDIDATE_OBJECT_SHA256, "candidate object pin")
    need(candidate.get("closed_zero_credit_terminal_count") == 16, "candidate closed count")
    need(candidate.get("remaining_terminal_totality_proof_count") == 4, "candidate open count")
    need(candidate.get("remaining_terminal_totality_proofs") == EXPECTED_OPEN, "candidate exact open terminals")
    need(candidate.get("legal_same_chart_witness_group_count") == 228, "candidate witness groups")
    need(candidate.get("unique_witness_component_edge_count") == 192, "candidate witness edges")
    need(candidate.get("prior_C27_C28_C29_authority") == "INVALIDATED__REBUILD_REQUIRED", "candidate old authority")
    need(candidate.get("C29_patch_or_preservation_permitted") is False, "candidate C29 patch forbidden")
    need(candidate.get("provisional_overlay_is_maximality_authority") is False, "candidate overlay nonauthority")
    need(candidate.get("formal_credit") == 0, "candidate zero credit")
    need(candidate.get("C27_C28_C29") == "REJECT_AND_REBUILD_REQUIRED", "candidate C27-C29 reject")
    need(candidate.get("CM2") == "NO-GO_FOR_CLAIM", "candidate CM2 reject")

    need(verification.get("candidate_result_sha256") == CANDIDATE_OBJECT_SHA256, "verification candidate binding")
    need(verification.get("closed_zero_credit_terminal_count") == 16, "verification closed count")
    need(verification.get("remaining_terminal_totality_proof_count") == 4, "verification open count")
    need(verification.get("legal_same_chart_witness_group_count") == 228, "verification witness groups")
    need(verification.get("unique_witness_component_edge_count") == 192, "verification witness edges")
    need(verification.get("prior_C27_C28_C29_authority") == "INVALIDATED__REBUILD_REQUIRED", "verification old authority")
    need(verification.get("provisional_overlay_authority") == "PROVISIONAL_UPPER_BOUND_ONLY", "verification overlay limit")
    need(verification.get("formal_credit") == 0, "verification zero credit")

    rejected = attack.get("rejected_attacks")
    need(type(rejected) is list and len(rejected) == 41 and len(set(rejected)) == 41, "41 unique rejected attacks")
    need(attack.get("status") == "PASS_41_OF_41_COHERENT_MUTATION_ATTACKS_REJECTED__ZERO_CREDIT_FAIL_CLOSE", "attack status")
    need(attack.get("candidate_result_sha256") == CANDIDATE_OBJECT_SHA256, "attack candidate binding")
    need(attack.get("closed_zero_credit_terminal_count") == 16, "attack closed count")
    need(attack.get("remaining_terminal_totality_proof_count") == 4, "attack open count")
    need(attack.get("prior_C27_C28_C29_authority") == "INVALIDATED__REBUILD_REQUIRED", "attack old authority")
    need(attack.get("provisional_overlay_authority") == "PROVISIONAL_UPPER_BOUND_ONLY", "attack overlay limit")
    need(attack.get("formal_credit") == 0, "attack zero credit")

    return candidate, verification, attack, run_receipts


def validate_evidence() -> dict[str, dict[str, Any]]:
    values: dict[str, dict[str, Any]] = {}
    for path, (expected_file_hash, closure_field) in EVIDENCE_PINS.items():
        need(file_hash(path) == expected_file_hash, f"evidence file pin:{path}")
        values[path.name] = closed_object(path, closure_field)

    owner = values[OWNER.name]
    need(owner.get("terminal_census") == {"SHEET_OWNER": 17_940, "SHEET_SHADOW": 17_940}, "owner/shadow census")
    need(owner.get("coherent_attacks_rejected") == 50, "owner/shadow attacks")
    need(owner.get("unresolved") == 0 and owner.get("legal_cross_component_witness") == 0, "owner/shadow closure")
    need(owner.get("formal_credit") == 0, "owner/shadow zero credit")

    direct = values[SAME_DIRECT.name]
    need(direct.get("legal_cross_component_witness_found") is True, "direct same-chart witnesses")
    need(direct.get("witness_census", {}).get("witness_group_count") == 228, "direct witness groups")
    need(direct.get("witness_census", {}).get("witness_component_occurrence_count") == 456, "direct witness projections")
    need(direct.get("formal_credit") == 0, "direct zero credit")

    cross = values[SAME_CROSS.name]
    match = cross.get("cross_implementation_exact_match", {})
    need(cross.get("legal_cross_component_witness_found") is True, "cross-implementation witnesses")
    need(match.get("group_count") == 228 and match.get("projection_count") == 456, "cross-implementation exact counts")
    need(match.get("unique_component_edge_count") == 192, "cross-implementation edge count")
    need(match.get("affected_component_vertex_count") == 312, "cross-implementation vertices")
    need(match.get("DSU_rank_reduction") == 192, "cross-implementation rank")
    need(cross.get("formal_credit") == 0, "cross-implementation zero credit")

    boundary = values[BOUNDARY.name]
    missing = boundary.get("minimal_missing_authority", {})
    need(missing.get("C19C_half_open_atom_count") == 33_344, "boundary half-open atom count")
    need(missing.get("endpoint_ownership_bit_count") == 200_064, "boundary endpoint bits")
    need(missing.get("three_terminal_unassigned_atom_count") == 483_232, "boundary unassigned atoms")
    need(missing.get("C26_direct_three_terminal_assignment_row_count") == 0, "boundary C26 assignments")
    need(boundary.get("terminal_credit_counted") == {
        "SIGNED_BOUNDARY_FACES": False,
        "COMPLETE_BOUNDARY_FACES": False,
        "POSITIVE_VOLUME_CARRIERS": False,
    }, "boundary terminals remain open")
    need(boundary.get("formal_credit") == 0, "boundary zero credit")

    overlay = values[OVERLAY.name]
    census = overlay.get("census", {})
    need(overlay.get("authority_limit") == "WITNESS_ONLY_PROVISIONAL_OVERLAY__NOT_A_FORMAL_C27R1_C28R1_OR_C29R1_SEAL", "overlay authority limit")
    need(census.get("old_components") == 57_876 and census.get("provisional_components") == 57_684, "overlay component census")
    need(census.get("certain_component_edges") == 192 and census.get("forced_rank_reduction") == 192, "overlay forced rank")
    need(census.get("affected_vertices") == 312 and census.get("affected_clusters") == 120, "overlay affected census")
    need(census.get("newly_internalized_pairs") == 691_416, "overlay internalized pairs")
    need(census.get("provisional_cross_denominator") == 125_615_784_254, "overlay provisional denominator")
    need(overlay.get("formal_credit") == 0, "overlay zero credit")

    return values


def main() -> int:
    need(sys.flags.isolated == 1 and sys.dont_write_bytecode is True, "isolated -I -B runtime")
    for path, expected in SOURCE_PINS.items():
        need(file_hash(path) == expected, f"source pin:{path.name}")

    candidate, verification, attack, run_receipts = validate_runs()
    evidence = validate_evidence()
    receipt = {
        "schema": "cm2.c27-independent.primitive-twenty-family-partition.aggregate-v4.zero-credit-receipt.v1",
        "status": "PASS_APPEND_ONLY_V4_AGGREGATE__16_OF_20_EVIDENCE_CLOSED__4_TOTALITY_PROOFS_OPEN__228_WITNESS_GROUPS_FORCE_C27_C28_C29_REBUILD__ZERO_CREDIT",
        "source_sha256": {path.name: expected for path, expected in SOURCE_PINS.items()},
        "receipt_builder_sha256": file_hash(Path(__file__)),
        "append_only_repetitions": {
            "count": 2,
            "run_directory_labels": list(RUN_LABELS),
            "producer_seed_parameter_present": False,
            "run_directory_labels_claimed_as_random_seeds": False,
        },
        "duplicate_run_bytes": {
            "candidate_byte_identical": True,
            "verification_byte_identical": True,
            "attack_byte_identical": True,
        },
        "run_receipts": run_receipts,
        "producer": {
            "file_sha256": CANDIDATE_FILE_SHA256,
            "result_sha256": candidate["result_sha256"],
            "truthful_reject_numeric_exit": 2,
        },
        "independent_verifier": {
            "file_sha256": VERIFICATION_FILE_SHA256,
            "status": verification["status"],
            "numeric_exit": 0,
        },
        "coherent_attacks": {
            "file_sha256": ATTACK_FILE_SHA256,
            "status": attack["status"],
            "rejected": len(attack["rejected_attacks"]),
            "total": 41,
            "numeric_exit": 0,
        },
        "evidence_file_sha256": {
            path.name: file_pin for path, (file_pin, _) in EVIDENCE_PINS.items()
        },
        "evidence_receipt_object_sha256": {
            OWNER.name: evidence[OWNER.name]["receipt_sha256"],
            SAME_DIRECT.name: evidence[SAME_DIRECT.name]["receipt_sha256"],
            SAME_CROSS.name: evidence[SAME_CROSS.name]["receipt_sha256"],
            BOUNDARY.name: evidence[BOUNDARY.name]["receipt_sha256"],
            OVERLAY.name: evidence[OVERLAY.name]["receipt_object_sha256"],
        },
        "terminal_census": {
            "grammar_terminals": 20,
            "evidence_closed_zero_credit": 16,
            "totality_open": 4,
            "open_terminals": EXPECTED_OPEN,
        },
        "confirmed_same_chart_witnesses": {
            "legal_witness_groups": 228,
            "member_projections": 456,
            "unique_old_component_edges": 192,
            "affected_old_component_vertices": 312,
            "forced_DSU_rank_reduction": 192,
        },
        "provisional_overlay": {
            "authority": "PROVISIONAL_UPPER_BOUND_ONLY__NOT_MAXIMALITY",
            "old_component_count": 57_876,
            "provisional_component_count": 57_684,
            "provisional_cross_component_denominator": 125_615_784_254,
            "newly_internalized_member_pairs": 691_416,
        },
        "prior_C27_C28_C29_authority": "INVALIDATED__SEMANTIC_REBUILD_REQUIRED__FILE_INTEGRITY_ONLY",
        "C29_patch_or_preservation_permitted": False,
        "rebuild_required": True,
        "formal_credit": 0,
        "C27_C28_C29": "REJECT_AND_REBUILD_REQUIRED",
        "CM2": "NO-GO_FOR_CLAIM",
    }
    print(canonical({**receipt, "receipt_sha256": digest(receipt)}).decode("ascii"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Failure as exc:
        print(canonical({
            "status": "REJECT_AGGREGATE_V4_RECEIPT_BUILD",
            "reason": str(exc),
            "formal_credit": 0,
            "C27_C28_C29": "REJECT_AND_REBUILD_REQUIRED",
            "CM2": "NO-GO_FOR_CLAIM",
        }).decode("ascii"))
        raise SystemExit(2)
