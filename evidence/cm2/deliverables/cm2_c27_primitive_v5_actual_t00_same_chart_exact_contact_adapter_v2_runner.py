#!/usr/bin/env python3
"""Subprocess runner with pre/post input identity for a T00 producer run."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
PRODUCER = ROOT / "deliverables/cm2_c27_primitive_v5_actual_t00_same_chart_exact_contact_adapter_v2.py"
PRODUCER_SHA256 = "27b1a0e0eef9d71070a5925a40b3a2d4e33608437545fde2e4ec2ad9013f4e66"
INPUTS = {
    "interface_v2": (".cm2-runtime/audit/c27r2-fresh-actual-v5-rebuild-interface-correction-v2/preflight.json", "6873b33d7b131a4bde0c4dbcf99873e6826cf2190fde6dfdf6640ee47d53c9d6"),
    "C15": ("deliverables/cm2_round306c15_source_g_502204_member_fresh_dsu_freeze_member_component_ledger.jsonl.gz", "e70c667fd8f14cb3c3d6444bb752dfc86244e61be292a9f884889d53951ff25a"),
    "C25": ("deliverables/cm2_round306c25_source_g_502204_member_549616_representation_typed_global_support_ledger_member_ledger.jsonl.gz", "66111f5d432eaa762e7043f06a45766e26fd71cc106ed65f3e0866ec4893c5b6"),
    "C19A": ("deliverables/cm2_round306c19a_source_g_5596_legacy_nongraph_exact_box_support_kernel_ledger.jsonl.gz", "9da9f54fc21ae59be3e9ea0ec3eb636f37c1445ecf759dbe6e2eea358cb262b3"),
    "C19B": ("deliverables/cm2_round306c19b_source_g_12232_r248_exact_positive_box_support_kernel_ledger.jsonl.gz", "ee23ebba0e90728ad7b16bccd34d90ba0c2ce701db240c63ba50cbc04e896798"),
    "C19C": ("deliverables/cm2_round306c19c_source_g_33344_empty_graph_surviving_side_support_kernel_ledger.jsonl.gz", "1f0f3f89cac5b10881b4b31a56b86d168ef901ca29bda6ad9eda87fc5f48ff84"),
    "C20A": ("deliverables/cm2_round306c20a_source_g_126468_preserved_direct_box_support_kernel_ledger.jsonl.gz", "bab9dcb7482d439b937c151823926c7339cafcd62edc7816c523126c20b4e922"),
    "C22A": ("deliverables/cm2_round306c22a_source_g_295340_r2_source_free_predicate_cell_kernel_ledger.jsonl.gz", "e8e17beacaef380c22656da0506eb779fd0927d9160bb9d90eb85ee2a84738bb"),
    "C23A": ("deliverables/cm2_round306c23a_source_g_10252_r292_source_free_t2ps_cell_kernel_ledger.jsonl.gz", "230d8081c31c200e1adc1d74f57724b4767380fcaa0ab09c00bca9d20444c528"),
    "R179": ("deliverables/cm2_round179_source_g_residual_tube_arrangement_rows.json", "f20b42c1fed781779b537b4d45bf44233eae1ed3ee620b95177a80f0eb2b5e42"),
    "R234": ("deliverables/cm2_round234_source_g_wall_endpoint_order_depth6_materialization_certificate.json", "6098032cf429855e816190e9345fa531f70e460eca60d75766e7108fc32c6fac"),
    "R236": ("deliverables/cm2_round236_source_g_wall_residual_closure_and_root_key_partition_certificate.json", "b5b9ec358b4837a02218756a034440d8fbc2aa706ca421bedb28aaf785de0217"),
    "C5": ("deliverables/cm2_round306c5_source_g_corrected_g2_graph_semantic_classification_row_ledger.jsonl.gz", "8f28efab9465440a0d6549f99a91d9b3997266f98a9c2eb06eda61ecdc42f333"),
    "C19C_manifest": ("deliverables/cm2_c19c_endpoint_ownership_v3_manifest.sha256", "14643e303aee7a3bac27342204ee92f2420ae855a5df66916307680721c82929"),
    "C19C_receipt": ("deliverables/cm2_c19c_endpoint_ownership_v3_terminal_receipt.json", "c620034783676f20d99e3f9a600cfe9b3e22a48129cd2f0555479d5b6c25e63b"),
    "C19C_authority": ("deliverables/cm2_c19c_endpoint_ownership_v3_authority_ledger.jsonl.gz", "77b220d803b64066a09a0172e06f53f0ddc7a229d208cb7248c2293f493f3166"),
    "C19C_cold": ("deliverables/cm2_c19c_endpoint_ownership_v3_postpublication_cold_replay_receipt.json", "17236dac0b9cf04d0d4e50bba1072fc90b2e87f732cdfa6d802f411facc6930d"),
    "C26_receipt": (".cm2-runtime/audit/c26-no-new-geometry-from-feature-rows-v1-zero-credit-seal-final/receipt.json", "be0cc715427bd9ee4792ad536a1bfab1f23db8de204ddf9fb9a24c745aa05cb7"),
    "C26_replay": (".cm2-runtime/audit/c26-no-new-geometry-from-feature-rows-v1-zero-credit-seal-final-terminal-replay/terminal_replay.json", "94bdcb59bbeba4d894a80c00345a27e9cf236354905ca40505336498726b4ad2"),
    "G2A_receipt": (".cm2-runtime/audit/g2a-relative2d-v2-zero-credit-seal-final-v2/receipt.json", "acb9b25d309efbf52026bacbb5208aa2775b4e4c5c98fcca30c7ed7ce42585b5"),
    "G2A_replay": (".cm2-runtime/audit/g2a-relative2d-v2-zero-credit-seal-final-v2-terminal-replay/terminal_replay.json", "aa95ca037c16d444a3e51e815afb9028489266b444da0582405029dc43cce2d7"),
}
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


def fsha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def snapshot() -> dict[str, Any]:
    result = {}
    paths = {"producer": (str(PRODUCER.relative_to(ROOT)), PRODUCER_SHA256),
             **INPUTS}
    for label, (relative, pin) in paths.items():
        path = ROOT / relative
        info = path.stat()
        observed = fsha(path)
        need(observed == pin, "snapshot pin:" + label)
        result[label] = {"path": relative, "sha256": observed,
                         "stat": [info.st_dev, info.st_ino, info.st_size,
                                  info.st_mtime_ns, info.st_ctime_ns,
                                  info.st_mode, info.st_uid, info.st_gid]}
    return result


def run(seed: int, out_dir: Path, run_dir: Path) -> dict[str, Any]:
    need(type(seed) is int and seed > 0, "positive seed")
    need(not out_dir.exists() and not run_dir.exists(), "fresh paths")
    pre = snapshot()
    run_dir.mkdir(parents=True)
    command = ["python", "-B", str(PRODUCER), "--out-dir", str(out_dir),
               "--seed", str(seed)]
    (run_dir / "command.json").write_bytes(canonical(command) + b"\n")
    completed = subprocess.run(command, cwd=ROOT, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, check=False)
    (run_dir / "stdout.log").write_bytes(completed.stdout)
    (run_dir / "stderr.log").write_bytes(completed.stderr)
    (run_dir / "exit_code.txt").write_text(str(completed.returncode) + "\n",
                                            encoding="ascii")
    need(completed.returncode == 0 and completed.stderr == b"",
         "producer exit0/stderr empty")
    stdout_lines = completed.stdout.splitlines()
    need(len(stdout_lines) == 1, "single final stdout JSON")
    summary = json.loads(stdout_lines[0])
    receipt_path = out_dir / "adapter_receipt.json"
    receipt = json.loads(receipt_path.read_bytes())
    body = dict(receipt)
    claim = body.pop("receipt_sha256", None)
    need(claim == digest(body) == summary["receipt_sha256"], "receipt closure")
    need(receipt["execution_seed"] == seed
         and receipt["producer_source_sha256"] == PRODUCER_SHA256
         and receipt["exact_census"]["candidate_count"] == 5_970_840
         and receipt["exact_census"]["lower_cross_component_candidate_count"] == 2_598_666,
         "receipt exact run")
    post = snapshot()
    need(pre == post, "pre/post input SHA/stat identity")
    stable = {"execution_seed": seed, "numeric_exit_code": 0,
              "signal": None, "stdout_line_count": 1,
              "stderr_empty": True, "pre_post_sha256_identical": True,
              "pre_post_stat_identical": True,
              "receipt_file_sha256": fsha(receipt_path),
              "receipt_object_sha256": receipt["receipt_sha256"]}
    body = {
        "schema": "cm2.c27-independent.primitive-v5-actual-t00-same-chart-exact-contact-adapter-run-attestation.v1",
        "status": "PASS_NUMERIC_EXIT0_SIGNAL_NULL_STDERR_EMPTY_PRE_POST_INPUT_IDENTITY__ZERO_CREDIT",
        "run": stable, "input_pre": pre, "input_post": post,
        "formal_credit": 0, "manifest_authorized": False,
        "C27_C28_C29": "UNAUTHORIZED", "CM2": "NO-GO_FOR_CLAIM",
        "runner_source_sha256": fsha(Path(__file__).resolve()),
    }
    result = dict(body)
    result["run_attestation_sha256"] = digest(result)
    (run_dir / "run_attestation.json").write_bytes(canonical(result) + b"\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", required=True, type=int)
    parser.add_argument("--out-dir", required=True)
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    try:
        result = run(args.seed, Path(args.out_dir).resolve(),
                     Path(args.run_dir).resolve())
    except (Failure, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError) as error:
        print("FAIL:" + str(error))
        return 2
    print(canonical({"status": result["status"],
                     "run": result["run"],
                     "run_attestation_sha256":
                         result["run_attestation_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
