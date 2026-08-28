#!/usr/bin/env python3
"""Build the independent append-only C27R1D zero-credit evidence bundle."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from typing import Any


ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parent
PREFIX = "cm2_round306c27r1d_source_g_strict_volume_provisional_overlay"
OUT = ROOT / (PREFIX + "_evidence_bundle.json")
PRODUCER_RUNS = [
    (30633101, WORKSPACE / ".cm2-runtime/audit/c27r1d-strict-volume-overlay-single-capture-seed-30633101"),
    (30633991, WORKSPACE / ".cm2-runtime/audit/c27r1d-strict-volume-overlay-single-capture-seed-30633991"),
]
VERIFIER_RUNS = [
    (30633201, WORKSPACE / ".cm2-runtime/audit/c27r1d-strict-volume-overlay-verifier-seed-30633201"),
    (30633891, WORKSPACE / ".cm2-runtime/audit/c27r1d-strict-volume-overlay-verifier-seed-30633891"),
]
ATTACK_RUN = WORKSPACE / ".cm2-runtime/audit/c27r1d-strict-volume-overlay-attacks-seed-30633777-run3"
LOCAL_FAILED_ATTACK_RUN = WORKSPACE / ".cm2-runtime/audit/c27r1d-strict-volume-overlay-attacks-seed-30633777"
EDGE = WORKSPACE / ".cm2-runtime/audit/c27-same-chart-strict-volume-v1-seed-30632101-run3/candidate/cm2_c27_same_chart_strict_volume_totality_v1_component_edges.jsonl.gz"
C15 = ROOT / "cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz"
STRICT_RECEIPT = ROOT / "cm2_c27_same_chart_strict_volume_totality_subgate_receipt.json"
FAILED_PREDECESSOR = WORKSPACE / ".cm2-runtime/audit/c27-same-chart-strict-volume-v1-seed-30632101-run2/failure_diagnosis.json"
OLD_OVERLAY_RECEIPT = WORKSPACE / ".cm2-runtime/audit/c27r1bc-provisional-overlay-v2-final-receipt.json"
SUPERSEDED_LOCAL_RUN = WORKSPACE / ".cm2-runtime/audit/c27r1d-strict-volume-overlay-seed-30633101"

PINS = {
    EDGE: (2_157_061, "64cb62aa3b5ae298699ef5809e075ce6c2314baad1f589965e675c82deaa4632"),
    C15: (142_025_813, "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a"),
    STRICT_RECEIPT: (4_234, "22f8f8f6635a6083254311f5ee776e9ebe82b3192b0aadac6dc9585a0b0db3a4"),
    FAILED_PREDECESSOR: (488, "ab5499a0e93aab58a963638862f06a9df0844050d0188b43f02c4d497744d75b"),
    OLD_OVERLAY_RECEIPT: (3_609, "cd05b9c1260bc037f38ff5edde22c635a1dc40fe5dff3d10a632b453361ac6de"),
}
STRICT_RECEIPT_OBJECT = "34277fdcb593186e9177e60d1c9fcef9969b732200231895d6c0b3a699621002"
OLD_OVERLAY_OBJECT = "6ea89bb2d752ee0be78d400da8c2602f7efd5c8a9b09de135f68bb0d2e2feaf9"
SOURCE_PINS = {
    PREFIX + "_producer.py": "ab2c5c335c5888a2734b8a05f1224c190bfea14e70191bb4b9e9102214c12fa5",
    PREFIX + "_independent_verifier.py": "0bce7b7d13997332b6a69e4ffcdaffb1bf969f3db880073bfa89a04646c5a981",
    PREFIX + "_attack_harness.py": "34b9e438a1d77361baed73fe81bba80e58ab3e8e1fbee6236b42706766d001f9",
}
OUTPUT_PINS = {
    PREFIX + "_14772_edge_application_ledger.jsonl.gz": (3_344_315, "27c25945cb018ccb4eaba52c7642bba616590523e766f3ddc63a0706ee87ac0b"),
    PREFIX + "_305_affected_cluster_ledger.jsonl.gz": (627_077, "8a7773d334756be5ab187ca40b6e79a180692e675b8de378eaea1f3b15953794"),
    PREFIX + "_43772_component_census_ledger.jsonl.gz": (7_887_418, "afbba7e14a3203b947c04f5f007386ced94851c961a08c08d0694078ffd13c80"),
    PREFIX + "_502204_member_assignment_ledger.jsonl.gz": (116_360_048, "94233878c18e938b4df3984f25b4d33b28d078522f4b074549912f104aad0b8d"),
    PREFIX + "_result.json": (2_629, "62a7cd87fa1f1c0e0e145798028fc2860461702dfa2bdd52da9931e65bfc6a52"),
}


class Failure(RuntimeError):
    pass


def need(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Failure(label)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def stable_identity(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_mode, info.st_nlink, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def capture(path: Path, expected: tuple[int, str] | None = None) -> tuple[bytes, dict[str, Any]]:
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, "rb") as stream:
        before = os.fstat(stream.fileno())
        need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, "regular single-link capture:" + path.name)
        state = hashlib.sha256()
        pieces = []
        while block := stream.read(4 << 20):
            state.update(block)
            pieces.append(block)
        after = os.fstat(stream.fileno())
        need(stable_identity(before) == stable_identity(after), "capture changed:" + path.name)
    raw = b"".join(pieces)
    meta = {"size": before.st_size, "sha256": state.hexdigest()}
    need(len(raw) == before.st_size, "capture byte count:" + path.name)
    if expected is not None:
        need((meta["size"], meta["sha256"]) == expected, "capture pin:" + path.name)
    return raw, meta


def json_capture(path: Path, expected: tuple[int, str] | None = None) -> tuple[dict[str, Any], dict[str, Any]]:
    raw, meta = capture(path, expected)
    value = json.loads(raw)
    need(type(value) is dict and canonical(value) + b"\n" == raw, "canonical json:" + path.name)
    return value, meta


def closure(value: dict[str, Any], field: str, label: str) -> str:
    body = dict(value)
    claimed = body.pop(field, None)
    need(type(claimed) is str and claimed == digest(body), "object closure:" + label)
    return claimed


def run_ok(run: Path) -> None:
    need(capture(run / "exit_code.txt")[0] == b"0\n", "numeric exit:" + run.name)
    need(capture(run / "stderr.txt")[0] == b"", "empty stderr:" + run.name)
    time = capture(run / "time.txt")[0].decode("utf-8")
    need("Exit status: 0" in time, "time exit status:" + run.name)


def verify_strict_receipt() -> dict[str, Any]:
    receipt, _ = json_capture(STRICT_RECEIPT, PINS[STRICT_RECEIPT])
    need(closure(receipt, "receipt_sha256", "strict-volume receipt") == STRICT_RECEIPT_OBJECT, "strict receipt object pin")
    meta = receipt.get("producer_replay", {}).get("ledgers", {}).get("cm2_c27_same_chart_strict_volume_totality_v1_component_edges.jsonl.gz")
    need(type(meta) is dict and meta.get("row_count") == 14_772 and meta.get("sha256") == PINS[EDGE][1] and meta.get("byte_identical_across_producer_seeds") is True, "strict receipt ledger authority")
    need(receipt.get("formal_credit") == 0 and receipt.get("C27_C28_C29") == "REJECT_AND_REBUILD_REQUIRED", "strict receipt qualification")
    return receipt


def verify_old_overlay() -> dict[str, Any]:
    receipt, _ = json_capture(OLD_OVERLAY_RECEIPT, PINS[OLD_OVERLAY_RECEIPT])
    need(closure(receipt, "receipt_object_sha256", "old overlay receipt") == OLD_OVERLAY_OBJECT, "old overlay object pin")
    need(receipt.get("formal_credit") == 0 and receipt.get("census", {}).get("provisional_components") == 57_684, "old overlay qualification")
    return receipt


def verify_producer_run(seed: int, run: Path) -> dict[str, Any]:
    run_ok(run)
    stdout, stdout_meta = json_capture(run / "stdout.json")
    need(stdout.get("status") == "PASS" and stdout.get("execution_seed") == seed, "producer seed/status")
    candidate = run / "candidate"
    need(candidate.is_dir() and not candidate.is_symlink(), "producer candidate directory")
    need({item.name for item in candidate.iterdir()} == set(OUTPUT_PINS), "exclusive producer outputs")
    observed = {}
    for name, pin in OUTPUT_PINS.items():
        _, meta = capture(candidate / name, pin)
        observed[name] = meta
    declared = stdout.get("outputs", {})
    declared["result"] = stdout.get("result")
    roles = {
        "edge_application_ledger": PREFIX + "_14772_edge_application_ledger.jsonl.gz",
        "affected_cluster_ledger": PREFIX + "_305_affected_cluster_ledger.jsonl.gz",
        "component_census_ledger": PREFIX + "_43772_component_census_ledger.jsonl.gz",
        "member_assignment_ledger": PREFIX + "_502204_member_assignment_ledger.jsonl.gz",
        "result": PREFIX + "_result.json",
    }
    for role, name in roles.items():
        need(declared[role] == {"filename": name, **observed[name]}, "producer declared output:" + role)
    result, _ = json_capture(candidate / (PREFIX + "_result.json"), OUTPUT_PINS[PREFIX + "_result.json"])
    need(closure(result, "result_object_sha256", "overlay result") == stdout.get("result_object_sha256"), "producer result object")
    need(result.get("formal_credit") == 0 and result.get("partition_census", {}).get("provisional_components") == 43_772, "producer zero-credit census")
    need(result.get("qualification", {}).get("C27") == result.get("qualification", {}).get("C28") == result.get("qualification", {}).get("C29") == "UNAUTHORIZED", "producer chain unauthorized")
    return {"seed": seed, "run": str(run.relative_to(WORKSPACE)), "stdout": stdout_meta, "result_object_sha256": result["result_object_sha256"], "candidate_files": observed}


def verify_verifier_run(seed: int, run: Path) -> dict[str, Any]:
    run_ok(run)
    value, meta = json_capture(run / "verification.json")
    stdout_raw, _ = capture(run / "stdout.json")
    need(stdout_raw == canonical(value) + b"\n", "verifier stdout/file identical")
    object_sha = closure(value, "verification_object_sha256", "independent verification")
    need(value.get("status") == "PASS_INDEPENDENT_ADJACENCY_BFS__PROVISIONAL_UPPER_BOUND_ONLY", "verifier status")
    need(value.get("implementation") == "ADJACENCY_LIST_AND_RANDOMIZED_BFS__NO_DSU_IMPORT_OR_REUSE", "verifier independence")
    need(value.get("strict_volume_subgate_receipt") == {
        "file_sha256": PINS[STRICT_RECEIPT][1], "object_sha256": STRICT_RECEIPT_OBJECT,
        "sealed_component_edge_ledger_sha256": PINS[EDGE][1], "sealed_component_edge_row_count": 14772,
        "authority_inherited": True,
    }, "verifier strict receipt inheritance")
    need(value.get("candidate_files_sha256") == {name: pin[1] for name, pin in OUTPUT_PINS.items()}, "verifier output pins")
    need((value.get("members"), value.get("strict_volume_edges"), value.get("old_components"), value.get("provisional_components"), value.get("rank_reduction")) == (502204, 14772, 57876, 43772, 14104), "verifier census")
    need((value.get("newly_internalized_unordered_member_pairs"), value.get("provisional_cross_component_pair_denominator")) == (24956788, 125591518882), "verifier pair arithmetic")
    need(value.get("formal_credit") == 0 and value.get("C27") == value.get("C28") == value.get("C29") == "UNAUTHORIZED", "verifier zero credit")
    return {"seed": seed, "run": str(run.relative_to(WORKSPACE)), "file": meta, "verification_object_sha256": object_sha}


def verify_attacks() -> dict[str, Any]:
    run_ok(ATTACK_RUN)
    value, meta = json_capture(ATTACK_RUN / "attacks.json")
    stdout_raw, _ = capture(ATTACK_RUN / "stdout.json")
    need(stdout_raw == canonical(value) + b"\n", "attack stdout/file identical")
    object_sha = closure(value, "attack_result_object_sha256", "coherent attacks")
    required = {"delete_authoritative_edge", "add_fake_edge", "cross_chart_injection", "duplicate_edge", "endpoint_tamper", "component_id_permutation", "missing_member_assignment", "duplicate_member_assignment", "denominator_off_by_one", "rank_tamper", "component_census_tamper"}
    labels = {row.get("attack") for row in value.get("attacks", [])}
    need(value.get("status") == "PASS_ALL_COHERENT_ATTACKS_REJECTED" and value.get("attack_count") == value.get("rejected_count") == 26 and value.get("accepted_count") == 0, "attack census")
    need(required <= labels and all(row.get("status") == "REJECTED" for row in value["attacks"]), "required attacks rejected")
    return {"seed": value["attack_seed"], "run": str(ATTACK_RUN.relative_to(WORKSPACE)), "file": meta, "attack_result_object_sha256": object_sha, "attack_count": 26, "rejected_count": 26}


def main() -> int:
    for path, pin in PINS.items():
        capture(path, pin)
    strict_receipt = verify_strict_receipt()
    old_overlay = verify_old_overlay()
    failed, _ = json_capture(FAILED_PREDECESSOR, PINS[FAILED_PREDECESSOR])
    need(failed.get("status") == "REJECT_IMPLEMENTATION_BUG_FAIL_CLOSED" and failed.get("cause") == "SINGLE_RTREE_QUERY_OMITTED_REQUIRED_CHART_PARTITION_AND_MIXED_CROSS_CHART_COORDINATE_OVERLAPS" and failed.get("formal_credit") == 0, "failed predecessor preserved")
    need(capture(LOCAL_FAILED_ATTACK_RUN / "exit_code.txt")[0] == b"2\n", "local failed attack numeric exit")
    local_failed_stderr, local_failed_meta = capture(LOCAL_FAILED_ATTACK_RUN / "stderr.txt", (52, "aba05003df014595eeca9fb0a20c7fd17b8bedf165836181ea34c5e20e1b0829"))
    local_failed = json.loads(local_failed_stderr)
    need(local_failed == {"error": "compact edges", "status": "FAIL_CLOSED"}, "local failed attack reason")
    need(SUPERSEDED_LOCAL_RUN.is_dir(), "superseded local replay preserved")
    producer_replay = [verify_producer_run(seed, run) for seed, run in PRODUCER_RUNS]
    need(producer_replay[0]["candidate_files"] == producer_replay[1]["candidate_files"], "double producer byte identity")
    independent = [verify_verifier_run(seed, run) for seed, run in VERIFIER_RUNS]
    need(independent[0]["file"] == independent[1]["file"] and independent[0]["verification_object_sha256"] == independent[1]["verification_object_sha256"], "double verifier byte identity")
    attacks = verify_attacks()
    for name, pin in SOURCE_PINS.items():
        source = ROOT / name
        capture(source, (source.stat().st_size, pin))

    value = {
        "schema": "cm2.round306c27r1d.strict-volume-provisional-overlay-independent-evidence-bundle.v1",
        "status": "PASS_APPEND_ONLY_STRICT_VOLUME_PROVISIONAL_OVERLAY_EVIDENCE__ZERO_FORMAL_CREDIT",
        "authority": "PROVISIONAL_STRICT_VOLUME_PARTITION_UPPER_BOUND_ONLY__NOT_A_FORMAL_C27_C28_C29_SEAL",
        "formal_credit": 0,
        "input_authority": {
            "strict_volume_subgate_receipt_file_sha256": PINS[STRICT_RECEIPT][1],
            "strict_volume_subgate_receipt_object_sha256": strict_receipt["receipt_sha256"],
            "sealed_component_edge_ledger": {"row_count": 14772, "size": PINS[EDGE][0], "sha256": PINS[EDGE][1]},
            "C15_member_assignment_ledger": {"row_count": 502204, "size": PINS[C15][0], "sha256": PINS[C15][1]},
            "producer_input_capture": "EACH_INPUT_HASHED_AND_PARSED_FROM_ONE_STABLE_O_NOFOLLOW_FD__FSTAT_BEFORE_HASH_AFTER_HASH_AFTER_PARSE",
        },
        "producer_replay": {
            "implementation": "CUSTOM_DSU__REAL_RANDOMIZED_EDGE_APPLICATION_ORDER__CANONICAL_OUTPUT",
            "real_materializations": 2, "seeds": [seed for seed, _ in PRODUCER_RUNS],
            "all_five_outputs_byte_identical": True, "runs": producer_replay,
        },
        "independent_verification": {
            "implementation": "ADJACENCY_LIST_AND_RANDOMIZED_BFS__NO_DSU_IMPORT_OR_REUSE",
            "real_reconstructions": 2, "seeds": [seed for seed, _ in VERIFIER_RUNS],
            "byte_identical_verification_outputs": True, "runs": independent,
        },
        "coherent_attacks": attacks,
        "partition_census": {
            "members": 502204, "old_C15_components": 57876, "strict_volume_component_edges": 14772,
            "affected_old_component_vertices": 14409, "affected_connected_clusters": 305,
            "forced_rank_reduction": 14104, "provisional_components": 43772,
            "old_within_component_unordered_member_pairs": 487702036,
            "newly_internalized_unordered_member_pairs": 24956788,
            "provisional_cross_component_pair_denominator": 125591518882,
        },
        "candidate_files": producer_replay[0]["candidate_files"],
        "append_only_governance": {
            "old_C27R1BC_overlay_receipt_file_sha256": PINS[OLD_OVERLAY_RECEIPT][1],
            "old_C27R1BC_overlay_receipt_object_sha256": old_overlay["receipt_object_sha256"],
            "old_C27R1BC_provisional_component_count": 57684,
            "old_overlay_or_formal_files_modified": False,
            "failed_strict_volume_predecessor": {"status": "PRESERVED_FAILED_RUN_ONLY", "diagnosis_sha256": PINS[FAILED_PREDECESSOR][1], "cause": failed["cause"]},
            "failed_local_attack_predecessor": {"status": "PRESERVED_FAILED_RUN_ONLY", "run": str(LOCAL_FAILED_ATTACK_RUN.relative_to(WORKSPACE)), "numeric_exit": 2, "stderr": local_failed_meta, "cause": "COMPACT_MODEL_NONEMPTY_LIST_BOOLEAN_GUARD_REJECTED_BEFORE_ATTACKS"},
            "superseded_local_replay": {"status": "PRESERVED_ZERO_AUTHORITY", "run": str(SUPERSEDED_LOCAL_RUN.relative_to(WORKSPACE)), "reason": "REPLACED_BY_SINGLE_CAPTURE_DOUBLE_REPLAY"},
        },
        "qualification": {
            "component_count": "43772_IS_AN_UPPER_BOUND_ONLY",
            "dim1_dim2_closure_contacts": "OPEN", "endpoint_ownership": "OPEN",
            "C26_transition_handle_routing": "OPEN", "other_support_terminals": "OPEN",
            "twenty_family_physical_totality_and_unique_assignment": "OPEN",
            "C27": "UNAUTHORIZED", "C28": "UNAUTHORIZED", "C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM",
        },
        "source_sha256": {**SOURCE_PINS, Path(__file__).name: hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
    }
    value["bundle_object_sha256"] = digest(value)
    payload = canonical(value) + b"\n"
    need(not OUT.exists(), "no clobber evidence bundle")
    fd = os.open(OUT, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try:
        os.write(fd, payload)
        os.fsync(fd)
    finally:
        os.close(fd)
    sys.stdout.buffer.write(payload)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Failure, OSError, KeyError, ValueError, TypeError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "FAIL_CLOSED", "error": str(error)}, sort_keys=True), file=sys.stderr)
        raise SystemExit(2)
