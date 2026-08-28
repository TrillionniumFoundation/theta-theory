#!/usr/bin/env python3
"""Cold no-import replay of the sealed truthful-reject v2 preflight receipt."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import gzip
import hashlib
import json
import os
from pathlib import Path
import stat
from typing import Any, Iterator


ROOT = Path(__file__).resolve().parent.parent


class Reject(RuntimeError):
    pass


def require(value: bool, label: str) -> None:
    if type(value) is not bool or not value:
        raise Reject(label)


def encode(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def object_hash(value: Any) -> str:
    return hashlib.sha256(encode(value)).hexdigest()


def fingerprint(value: os.stat_result) -> tuple[int, ...]:
    return (value.st_dev, value.st_ino, value.st_size, value.st_mtime_ns,
            value.st_ctime_ns, value.st_mode, value.st_uid, value.st_gid)


@dataclass
class Capture:
    label: str
    path: Path
    fd: int
    initial: tuple[int, ...]
    sha256: str

    @classmethod
    def open(cls, label: str, path: Path, expected: str) -> "Capture":
        require(type(expected) is str and len(expected) == 64, label + ":expected sha")
        resolved = path.resolve()
        fd = os.open(resolved, os.O_RDONLY | getattr(os, "O_CLOEXEC", 0)
                     | getattr(os, "O_NOFOLLOW", 0))
        try:
            before = os.fstat(fd)
            require(stat.S_ISREG(before.st_mode), label + ":regular")
            state = hashlib.sha256()
            while block := os.read(fd, 4 << 20):
                state.update(block)
            observed = state.hexdigest()
            require(observed == expected, label + ":sha256")
            require(fingerprint(os.fstat(fd)) == fingerprint(before),
                    label + ":hash fstat")
            return cls(label, resolved, fd, fingerprint(before), observed)
        except BaseException:
            os.close(fd)
            raise

    def stable(self, phase: str) -> None:
        require(fingerprint(os.fstat(self.fd)) == self.initial,
                self.label + ":" + phase + ":fstat")

    def raw(self) -> bytes:
        os.lseek(self.fd, 0, os.SEEK_SET)
        chunks: list[bytes] = []
        while block := os.read(self.fd, 4 << 20):
            chunks.append(block)
        self.stable("raw")
        return b"".join(chunks)

    def document(self, closure_key: str | None,
                 canonical_file: bool = True) -> dict[str, Any]:
        raw = self.raw()
        value = json.loads(raw)
        require(type(value) is dict, self.label + ":document")
        if canonical_file:
            require(encode(value) + b"\n" == raw, self.label + ":canonical")
        if closure_key is not None:
            body = dict(value)
            claim = body.pop(closure_key, None)
            require(type(claim) is str and claim == object_hash(body),
                    self.label + ":closure")
        return value

    def rows(self) -> Iterator[dict[str, Any]]:
        os.lseek(self.fd, 0, os.SEEK_SET)
        duplicate = os.dup(self.fd)
        with os.fdopen(duplicate, "rb") as raw:
            with gzip.GzipFile(fileobj=raw, mode="rb") as stream:
                for ordinal, line in enumerate(stream):
                    require(line.endswith(b"\n"), f"{self.label}:{ordinal}:newline")
                    payload = line[:-1]
                    row = json.loads(payload)
                    require(type(row) is dict and encode(row) == payload,
                            f"{self.label}:{ordinal}:canonical")
                    body = dict(row)
                    claim = body.pop("row_sha256", None)
                    require(type(claim) is str and claim == object_hash(body),
                            f"{self.label}:{ordinal}:closure")
                    yield row
        self.stable("rows")

    def attestation(self) -> dict[str, Any]:
        self.stable("attestation")
        try:
            rendered = str(self.path.relative_to(ROOT))
        except ValueError:
            rendered = str(self.path)
        return {"path": rendered, "sha256": self.sha256, "size": self.initial[2],
                "stat_fingerprint": list(self.initial), "O_NOFOLLOW": True,
                "single_open_file_description_hash_parse_fstat": True}

    def close(self) -> None:
        os.close(self.fd)


def file_sha(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(4 << 20):
            state.update(block)
    return state.hexdigest()


def manifest_entries(raw: bytes, label: str) -> dict[str, str]:
    entries: dict[str, str] = {}
    for ordinal, line in enumerate(raw.decode("ascii").splitlines()):
        parts = line.split("  ", 1)
        require(len(parts) == 2 and len(parts[0]) == 64,
                f"{label}:{ordinal}:line")
        sha, path = parts
        require(path not in entries, f"{label}:{ordinal}:duplicate")
        entries[path] = sha
    return entries


def resolve(path: str) -> Path:
    value = Path(path)
    return value.resolve() if value.is_absolute() else (ROOT / value).resolve()


def replay(args: argparse.Namespace) -> dict[str, Any]:
    output = Path(args.out_file)
    require(not output.exists(), "fresh replay output")
    roots = {
        "receipt": Capture.open("receipt", Path(args.receipt), args.receipt_sha256),
        "payload_manifest": Capture.open("payload_manifest",
                                         Path(args.payload_manifest),
                                         args.payload_manifest_sha256),
        "root_manifest": Capture.open("root_manifest", Path(args.root_manifest),
                                      args.root_manifest_sha256),
    }
    payload: dict[str, Capture] = {}
    try:
        receipt = roots["receipt"].document("result_sha256")
        payload_entries = manifest_entries(roots["payload_manifest"].raw(),
                                           "payload manifest")
        root_entries = manifest_entries(roots["root_manifest"].raw(),
                                        "root manifest")
        require(root_entries == {
            "payload_manifest.sha256": roots["payload_manifest"].sha256,
            "receipt.json": roots["receipt"].sha256,
        }, "two-entry root closure")
        require(receipt["schema"]
                == "cm2.c27-independent.primitive-twenty-family-gate-v5-preflight-v2-zero-credit-receipt.v1"
                and receipt["status"]
                == "PASS_SEALED_TRUTHFUL_REJECT_PREFLIGHT_VERIFIER_AND_18_ATTACKS__ZERO_CREDIT"
                and receipt["formal_credit"] == 0
                and receipt["manifest_authorized"] is False
                and receipt["preflight_execution"] == {
                    "decision": "REJECT", "intended_exit_code": 2,
                    "observed_exit_code": 2, "observed_matches_intended": True,
                    "truthful_reject": True}
                and receipt["payload_manifest"]["entry_count"] == len(payload_entries)
                and receipt["payload_manifest"]["file_sha256"]
                    == roots["payload_manifest"].sha256,
                "receipt terminal state")
        attestations = receipt["root_input_capture"]["attestations"]
        require(len(payload_entries) == 22 and len(attestations) == 22,
                "22 sealed payloads")
        require(set(payload_entries) == {item["path"] for item in attestations.values()},
                "manifest/attestation path universe")
        for label, item in sorted(attestations.items()):
            require(payload_entries[item["path"]] == item["sha256"],
                    label + ":manifest binding")
            payload[label] = Capture.open(label, resolve(item["path"]), item["sha256"])
        require(payload["terminal_replay_source"].path == Path(__file__).resolve()
                and payload["terminal_replay_source"].sha256
                    == file_sha(Path(__file__).resolve()), "replay source self pin")

        preflight = payload["preflight_result"].document("result_sha256")
        verification = payload["independent_verification"].document(
            "verification_sha256")
        attacks = payload["coherent_attacks"].document("attack_result_sha256")
        require(preflight["result_sha256"]
                    == receipt["sealed_artifacts"]["preflight_result"]["object_sha256"]
                and payload["preflight_result"].sha256
                    == receipt["sealed_artifacts"]["preflight_result"]["file_sha256"]
                and preflight["status"]
                    == "REJECT_MISSING_FULL_ATOM_AND_OR_C26_FORMAL_RECEIPT__ZERO_CREDIT"
                and preflight["decision"] == "REJECT"
                and preflight["intended_process_exit_code"] == 2
                and preflight["formal_credit"] == 0
                and preflight["manifest_authorized"] is False,
                "preflight truthful reject replay")
        expected_blockers = {
            "FULL_101080_TO_483232_ATOM_INCIDENCE_FORMAL_RECEIPT",
            "C26_PRIMITIVE_EXACT_CONTACT_ABSENCE_FORMAL_RECEIPT",
        }
        require(set(preflight["blocking_authority_slots"]) == expected_blockers
                and preflight["global_gate"]["primitive_twenty_family_totality_proved"]
                    is False
                and preflight["global_gate"]["decision"] == "FAIL_CLOSED_REJECT"
                and preflight["authority_hardening"]
                    ["G2A_final_v2_receipt_bound"] is True
                and preflight["authority_hardening"]
                    ["G2A_payload_and_root_manifests_bound"] is True
                and preflight["authority_hardening"]
                    ["G2A_terminal_replay_bound"] is True
                and preflight["authority_hardening"]
                    ["G2A_old_invalidated_seal_rejected"] is True
                and preflight["authority_hardening"]
                    ["pair_union_terminal_receipt_bound"] is True
                and preflight["authority_hardening"]
                    ["pair_union_no_import_verification_bound"] is True
                and preflight["authority_hardening"]
                    ["pair_union_18_of_18_attacks_bound"] is True,
                "strong authority replay")
        sequence = hashlib.sha256()
        gaps: dict[str, dict[str, Any]] = {}
        for row in payload["gap_ledger"].rows():
            slot = row["authority_slot"]
            require(slot not in gaps, "unique authority slot")
            gaps[slot] = row
            sequence.update(bytes.fromhex(row["row_sha256"]))
        require(len(gaps) == 9
                and set(slot for slot, row in gaps.items() if row["gate_blocking"])
                    == expected_blockers
                and preflight["gap_ledger"]["file_sha256"]
                    == payload["gap_ledger"].sha256
                and preflight["gap_ledger"]["row_sequence_sha256"]
                    == sequence.hexdigest(), "cold gap replay")
        require(verification["status"]
                    == "PASS_INDEPENDENT_AUTHORITY_BOUND_TRUTHFUL_REJECT__ZERO_CREDIT"
                and verification["decision"] == "VERIFY_REJECT"
                and verification["formal_credit"] == 0
                and verification["manifest_authorized"] is False
                and verification["implementation_independence"]
                    ["preflight_or_workspace_module_imported"] is False
                and verification["implementation_independence"]
                    ["verifier_source_sha256"]
                    == payload["independent_verifier_source"].sha256
                and verification["verification_sha256"]
                    == receipt["sealed_artifacts"]["independent_verification"]
                        ["object_sha256"], "independent verification replay")
        require(attacks["status"]
                    == "PASS_CONTROL_AND_18_OF_18_COHERENT_RESIGNED_ATTACKS_REJECTED__ZERO_CREDIT"
                and attacks["attack_count"] == 18
                and attacks["rejected_attack_count"] == 18
                and attacks["accepted_attack_count"] == 0
                and attacks["control"]["verifier_exit_code"] == 0
                and attacks["formal_credit"] == 0
                and attacks["manifest_authorized"] is False
                and attacks["pins"]["verifier_source_sha256"]
                    == payload["independent_verifier_source"].sha256
                and attacks["pins"]["baseline_result_file_sha256"]
                    == payload["preflight_result"].sha256
                and attacks["pins"]["baseline_gap_file_sha256"]
                    == payload["gap_ledger"].sha256
                and attacks["attack_result_sha256"]
                    == receipt["sealed_artifacts"]["coherent_attacks"]
                        ["object_sha256"], "coherent attacks replay")
        require(receipt["global_gate"] == {
            "decision": "FAIL_CLOSED_REJECT",
            "primitive_twenty_family_totality_proved": False,
            "full_atom_formal_receipt_present": False,
            "C26_formal_receipt_present": False,
            "future_closure_requires_fresh_actual_gate_run": True,
            "sealed_preflight_may_not_be_rewritten": True,
        }, "append-only gate semantics")

        body = {
            "schema": "cm2.c27-independent.primitive-twenty-family-gate-v5-preflight-v2-terminal-replay.v1",
            "status": "PASS_COLD_ROOT_PAYLOAD_AND_TRUTHFUL_REJECT_REPLAY__ZERO_CREDIT",
            "replay_seed": args.seed,
            "receipt_file_sha256": roots["receipt"].sha256,
            "receipt_result_sha256": receipt["result_sha256"],
            "payload_manifest_file_sha256": roots["payload_manifest"].sha256,
            "root_manifest_file_sha256": roots["root_manifest"].sha256,
            "payload_entry_count": len(payload_entries),
            "preflight_intended_and_observed_exit_code": 2,
            "decision": "VERIFY_TRUTHFUL_REJECT",
            "blocking_authority_slots": sorted(expected_blockers),
            "future_closure_requires_fresh_actual_gate_run": True,
            "formal_credit": 0,
            "manifest_authorized": False,
            "CM2": "NO-GO_FOR_CLAIM",
            "implementation_independence": {
                "receipt_builder_or_preflight_module_imported": False,
                "stdlib_only": True,
                "terminal_replay_source_sha256": file_sha(Path(__file__).resolve()),
            },
            "root_input_capture": {
                "all_inputs_single_stable_O_NOFOLLOW_FD_hash_parse_fstat": True,
                "attestations": {label: capture.attestation()
                                 for label, capture in sorted(roots.items())},
            },
        }
        result = dict(body)
        result["semantic_projection_sha256"] = object_hash({
            key: value for key, value in body.items()
            if key not in {"replay_seed", "root_input_capture"}})
        result["result_sha256"] = object_hash(result)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(encode(result) + b"\n")
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
    parser.add_argument("--out-file", required=True)
    parser.add_argument("--seed", required=True, type=int)
    args = parser.parse_args()
    try:
        result = replay(args)
    except (Reject, KeyError, TypeError, ValueError, OSError,
            json.JSONDecodeError) as error:
        print("REJECT:" + str(error))
        return 2
    print(encode({"status": result["status"],
                  "result_sha256": result["result_sha256"],
                  "blocking_authority_slots":
                      result["blocking_authority_slots"]}).decode("ascii"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
