#!/usr/bin/env python3
"""Cold no-import replay of the sealed actual-v2 dual-real-seed evidence."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import stat
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
SELF = Path(__file__).resolve()
RUNNER_SHA256 = "c0f2c29d03aad122762ba0b3dad5885418c17872dab3da665eb764dad9cab245"
ASSEMBLER_SHA256 = "038c6a661438f9253fb00a29b9f41941bea33a3a8769a258d8dfa5763880b561"
WATCHER_SHA256 = "3e5f874230c9faf809975808a2bd7284acf32c6e2b771e36a86d532a1a22c386"


class Reject(RuntimeError):
    pass


def require(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def encode(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(encode(value)).hexdigest()


def fingerprint(info: os.stat_result) -> tuple[int, ...]:
    return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns,
            info.st_ctime_ns, info.st_mode, info.st_uid, info.st_gid)


@dataclass
class Capture:
    label: str
    path: Path
    fd: int
    initial: tuple[int, ...]
    sha256: str

    @classmethod
    def open(cls, label: str, path: Path, expected: str) -> "Capture":
        require(type(expected) is str and len(expected) == 64,
                label + ":expected SHA256")
        resolved = path.resolve()
        require(resolved == ROOT or ROOT in resolved.parents,
                label + ":inside workspace")
        descriptor = os.open(resolved, os.O_RDONLY
                             | getattr(os, "O_CLOEXEC", 0)
                             | getattr(os, "O_NOFOLLOW", 0))
        try:
            before = os.fstat(descriptor)
            require(stat.S_ISREG(before.st_mode) and before.st_nlink == 1,
                    label + ":regular single-link")
            state = hashlib.sha256()
            while block := os.read(descriptor, 4 << 20):
                state.update(block)
            observed = state.hexdigest()
            require(observed == expected, label + ":SHA256")
            require(fingerprint(os.fstat(descriptor)) == fingerprint(before),
                    label + ":stable hash fstat")
            return cls(label, resolved, descriptor, fingerprint(before),
                       observed)
        except BaseException:
            os.close(descriptor)
            raise

    def raw(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        chunks: list[bytes] = []
        while block := os.read(self.fd, 4 << 20):
            chunks.append(block)
        require(fingerprint(os.fstat(self.fd)) == self.initial,
                self.label + ":stable reread fstat")
        return b"".join(chunks)

    def document(self, closure: str | None = None) -> Any:
        raw = self.raw()
        value = json.loads(raw)
        require(raw == encode(value) + b"\n", self.label + ":canonical JSON")
        if closure is not None:
            require(type(value) is dict, self.label + ":object")
            body = dict(value)
            claim = body.pop(closure, None)
            require(type(claim) is str and claim == digest(body),
                    self.label + ":object closure")
        return value

    def attestation(self) -> dict[str, Any]:
        require(fingerprint(os.fstat(self.fd)) == self.initial,
                self.label + ":terminal fstat")
        return {"path": str(self.path.relative_to(ROOT)),
                "sha256": self.sha256, "size": self.initial[2],
                "stat_fingerprint": list(self.initial),
                "O_NOFOLLOW": True,
                "single_open_file_description_hash_parse_fstat": True}

    def close(self) -> None:
        os.close(self.fd)


def manifest(raw: bytes, label: str) -> dict[str, str]:
    require(raw.endswith(b"\n")
            and raw.decode("ascii").encode("ascii") == raw,
            label + ":ASCII newline")
    rows = raw.decode("ascii").splitlines()
    require(rows == sorted(rows) and len(rows) == len(set(rows)),
            label + ":sorted unique")
    result: dict[str, str] = {}
    for ordinal, row in enumerate(rows):
        pieces = row.split("  ", 1)
        require(len(pieces) == 2 and len(pieces[0]) == 64
                and pieces[1] not in result,
                f"{label}:row:{ordinal}")
        result[pieces[1]] = pieces[0]
    return result


def resolve(rendered: str) -> Path:
    value = Path(rendered)
    return value.resolve() if value.is_absolute() else (ROOT / value).resolve()


def replay(args: argparse.Namespace) -> dict[str, Any]:
    require(hashlib.sha256(SELF.read_bytes()).hexdigest()
            == args.expect_replay_sha256, "terminal replay self pin")
    output = Path(args.out_file).resolve()
    require(ROOT in output.parents and not output.exists(),
            "fresh replay output inside workspace")
    roots = {
        "receipt": Capture.open("receipt", Path(args.receipt),
                                args.receipt_sha256),
        "payload_manifest": Capture.open(
            "payload_manifest", Path(args.payload_manifest),
            args.payload_manifest_sha256),
        "root_manifest": Capture.open("root_manifest", Path(args.root_manifest),
                                      args.root_manifest_sha256),
    }
    payload: dict[str, Capture] = {}
    try:
        receipt = roots["receipt"].document("receipt_sha256")
        payload_rows = manifest(roots["payload_manifest"].raw(),
                                "payload manifest")
        root_rows = manifest(roots["root_manifest"].raw(), "root manifest")
        require(root_rows == {
            "payload_manifest.sha256": roots["payload_manifest"].sha256,
            "receipt.json": roots["receipt"].sha256,
        }, "two-entry root closure")
        require(receipt["schema"]
                == "cm2.c27-independent.primitive-twenty-family-gate-v5-actual-v2-dual-seed-zero-credit-seal.v1"
                and receipt["status"]
                    == "PASS_SEALED_TWO_REAL_SEEDS_NATIVE_AND_INDEPENDENT_REPLAY_PLUS_24_ATTACKS__PENDING_COLD_REPLAY__ZERO_CREDIT"
                and receipt["execution_seeds"] == [30660101, 30660991]
                and receipt["payload_manifest"]["entry_count"]
                    == len(payload_rows)
                and receipt["payload_manifest"]["file_sha256"]
                    == roots["payload_manifest"].sha256
                and receipt["formal_credit"] == 0
                and receipt["manifest_authorized"] is False
                and receipt["C27R2_C28_C29"]
                    == "UNAUTHORIZED_PENDING_ACTUAL_V2_COLD_REPLAY"
                and receipt["CM2"] == "NO-GO_FOR_CLAIM",
                "base receipt terminal state")
        attestations = receipt["root_input_capture"]["attestations"]
        require(receipt["root_input_capture"]
                    ["all_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat"]
                is True
                and set(payload_rows)
                    == {item["path"] for item in attestations.values()},
                "payload/attestation universe")
        for label, item in sorted(attestations.items()):
            require(payload_rows[item["path"]] == item["sha256"],
                    label + ":manifest binding")
            payload[label] = Capture.open(label, resolve(item["path"]),
                                          item["sha256"])
            require(payload[label].attestation() == item,
                    label + ":current stat attestation")

        require(payload["terminal_replay_source"].path == SELF
                and payload["terminal_replay_source"].sha256
                    == args.expect_replay_sha256,
                "cold replay source self binding")
        pins = receipt["source_pins"]
        require(pins["runner"] == RUNNER_SHA256
                and pins["assembler"] == ASSEMBLER_SHA256
                and pins["seed2_handoff_watcher"] == WATCHER_SHA256
                and pins["independent_verifier"]
                    == payload["independent_verifier_source"].sha256
                and pins["coherent_attack_harness"]
                    == payload["attack_harness_source"].sha256
                and pins["terminal_replay"]
                    == payload["terminal_replay_source"].sha256
                and pins["finalizer_watcher"]
                    == payload["finalizer_source"].sha256,
                "all source pins")

        verification = payload["independent_verification"].document(
            "verification_sha256")
        require(verification["status"]
                == "PASS_TWO_REAL_SEEDS_NATIVE_FULL_PASS_INDEPENDENT_GLOBAL_REPLAY_AND_EXACT_SEED_INVARIANCE__ZERO_CREDIT"
                and verification["execution_seeds"] == [30660101, 30660991]
                and verification["exact_census"] == receipt["exact_census"]
                and verification["source_pins"]["runner"] == RUNNER_SHA256
                and verification["source_pins"]["assembler"]
                    == ASSEMBLER_SHA256
                and verification["source_pins"]["seed2_handoff_watcher"]
                    == WATCHER_SHA256
                and verification["formal_credit"] == 0
                and verification["manifest_authorized"] is False,
                "independent verification replay")
        attacks = payload["coherent_attacks"].document(
            "attack_result_sha256")
        require(attacks["status"]
                == "PASS_CONTROL_AND_24_OF_24_COHERENT_RESIGNED_ATTACKS_REJECTED__ZERO_CREDIT"
                and attacks["control_passed"] is True
                and attacks["attack_count"] == 24
                and attacks["rejected_attack_count"] == 24
                and attacks["accepted_attack_count"] == 0
                and attacks["pins"]["verification_file_sha256"]
                    == payload["independent_verification"].sha256
                and attacks["pins"]["independent_verifier_source_sha256"]
                    == payload["independent_verifier_source"].sha256
                and attacks["pins"]["attack_harness_source_sha256"]
                    == payload["attack_harness_source"].sha256
                and attacks["formal_credit"] == 0
                and attacks["manifest_authorized"] is False,
                "coherent attack replay")
        handoff = payload["seed2_handoff_receipt"].document(
            "handoff_receipt_sha256")
        require(handoff["status"]
                == "PASS_SEED1_FULL_TRANSACTION_AND_CURRENT_HASHES__EXEC_SEED2_ZERO_CREDIT"
                and handoff["seed1"] == 30660101
                and handoff["seed2"] == 30660991
                and handoff["runner_source_sha256"] == RUNNER_SHA256
                and handoff["watcher_source_sha256"] == WATCHER_SHA256
                and handoff["formal_credit"] == 0
                and handoff["manifest_authorized"] is False,
                "seed2 handoff replay")
        for label, seed in (("seed1", 30660101), ("seed2", 30660991)):
            attestation = payload[label + "_run_attestation"].document(
                "run_attestation_sha256")
            validation = payload[label + "_output_validation"].document()
            signal_value = payload[label + "_signal"].document()
            require(attestation["execution_seed"] == seed
                    and attestation["numeric_exit_code"] == 0
                    and attestation["signal"] is None
                    and attestation["stderr_empty"] is True
                    and attestation["pre_post_sha256_identical"] is True
                    and attestation["pre_post_stat_identical"] is True
                    and attestation["formal_credit"] == 0
                    and attestation["manifest_authorized"] is False
                    and digest(validation)
                        == attestation["output_validation_sha256"]
                    and validation["output_file_count"] == 7
                    and signal_value is None
                    and payload[label + "_exit"].raw() == b"0\n"
                    and payload[label + "_stderr"].raw() == b""
                    and payload[label + "_pass_lock"].raw()
                        == b"PASS_TRANSACTION_COMPLETE__ZERO_CREDIT\n",
                    label + ":native terminal replay")
        require(receipt["independent_verification"] == {
            "file_sha256": payload["independent_verification"].sha256,
            "object_sha256": verification["verification_sha256"],
            "semantic_projection_sha256":
                verification["semantic_projection_sha256"],
        } and receipt["coherent_attacks"] == {
            "file_sha256": payload["coherent_attacks"].sha256,
            "object_sha256": attacks["attack_result_sha256"],
            "attack_count": 24, "rejected": 24, "accepted": 0,
        }, "receipt verifier/attack object binding")

        body = {
            "schema": "cm2.c27-independent.primitive-twenty-family-gate-v5-actual-v2-dual-seed-terminal-replay.v1",
            "status": "PASS_COLD_ROOT_PAYLOAD_CURRENT_SHA_STAT_NATIVE_DUAL_SEED_INDEPENDENT_REPLAY_AND_24_ATTACKS__ZERO_CREDIT",
            "replay_seed": args.replay_seed,
            "base_receipt_file_sha256": roots["receipt"].sha256,
            "base_receipt_object_sha256": receipt["receipt_sha256"],
            "payload_manifest_file_sha256": roots["payload_manifest"].sha256,
            "root_manifest_file_sha256": roots["root_manifest"].sha256,
            "payload_entry_count": len(payload_rows),
            "execution_seeds": [30660101, 30660991],
            "seed_invariant_mathematical_projection_sha256":
                verification["seed_invariant_mathematical_projection_sha256"],
            "exact_census": verification["exact_census"],
            "independent_verification_object_sha256":
                verification["verification_sha256"],
            "coherent_attack_object_sha256": attacks["attack_result_sha256"],
            "actual_v2_terminal_gate": "PASS_COLD_REPLAY_READY_FOR_TERMINAL_RECEIPT",
            "formal_credit": 0,
            "manifest_authorized": False,
            "C27R2_C28_C29": "UNAUTHORIZED_PENDING_TERMINAL_RECEIPT",
            "CM2": "NO-GO_FOR_CLAIM",
            "implementation_independence": {
                "receipt_builder_verifier_attack_or_assembler_module_imported": False,
                "stdlib_only": True,
                "terminal_replay_source_sha256": args.expect_replay_sha256,
            },
            "root_input_capture": {
                "all_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat": True,
                "attestations": {key: value.attestation()
                                 for key, value in sorted(roots.items())},
            },
        }
        result = dict(body)
        result["semantic_projection_sha256"] = digest({
            key: value for key, value in body.items()
            if key not in {"replay_seed", "root_input_capture"}
        })
        result["result_sha256"] = digest(result)
        output.parent.mkdir(parents=True, exist_ok=True)
        descriptor = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL
                             | getattr(os, "O_NOFOLLOW", 0), 0o600)
        try:
            os.write(descriptor, encode(result) + b"\n")
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
        return result
    finally:
        for capture in payload.values():
            capture.close()
        for capture in roots.values():
            capture.close()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--receipt-sha256", required=True)
    parser.add_argument("--payload-manifest", required=True)
    parser.add_argument("--payload-manifest-sha256", required=True)
    parser.add_argument("--root-manifest", required=True)
    parser.add_argument("--root-manifest-sha256", required=True)
    parser.add_argument("--expect-replay-sha256", required=True)
    parser.add_argument("--replay-seed", type=int, required=True)
    parser.add_argument("--out-file", required=True)
    args = parser.parse_args()
    try:
        result = replay(args)
    except (Reject, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError) as error:
        print("REJECT:" + str(error))
        return 2
    print(encode({"status": result["status"],
                  "result_sha256": result["result_sha256"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
